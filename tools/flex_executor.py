"""
Flex Executor Tool for running Flex code via CLI.

This module provides async subprocess execution of Flex programs with
proper error handling, timeout management, and resource control.
"""

import asyncio
import os
import tempfile
import signal
import psutil
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
from agents.models import FlexExecutionRequest, FlexExecutionResult
from config.settings import Settings, get_settings
from .file_manager import FileManager


class FlexExecutorError(Exception):
    """Custom exception for Flex executor errors."""
    pass


class FlexExecutor:
    """Executes Flex programs via CLI with proper resource management."""
    
    def __init__(self, settings: Optional[Settings] = None):
        """Initialize Flex executor with settings."""
        self.settings = settings or get_settings()
        self.flex_cli_path = self.settings.flex.cli_path
        self.default_timeout = self.settings.app.execution_timeout
        self.file_manager = FileManager(settings)
        
        # Resource limits
        self.max_memory_mb = 512  # Maximum memory usage in MB
        self.max_cpu_percent = 50  # Maximum CPU usage percentage
        
        # Process tracking
        self.running_processes: Dict[str, asyncio.subprocess.Process] = {}
    
    async def execute(self, request: FlexExecutionRequest) -> FlexExecutionResult:
        """
        Execute Flex code with proper error handling and resource management.
        
        Args:
            request: Execution request with code and options
            
        Returns:
            Execution result with output, errors, and metadata
        """
        start_time = datetime.now()
        process_id = None
        temp_file = None
        
        try:
            # Save code to temporary file if needed
            if request.save_to_file:
                if request.filename:
                    # Use provided filename
                    filepath = Path(request.filename)
                    if not filepath.suffix:
                        filepath = filepath.with_suffix('.flex')
                    
                    # Save to file manager
                    save_result = await self.file_manager.save_flex_code(
                        request.code,
                        filepath.name
                    )
                    
                    if not save_result.success:
                        return FlexExecutionResult(
                            success=False,
                            output="",
                            error=f"Failed to save code: {save_result.message}",
                            execution_time=0.0,
                            filename=request.filename
                        )
                    
                    temp_file = Path(save_result.filepath)
                else:
                    # Create temporary file
                    temp_file = await self.file_manager.create_temp_file(
                        request.code,
                        "execution"
                    )
            else:
                # Create temporary file for execution
                temp_file = await self.file_manager.create_temp_file(
                    request.code,
                    "temp_exec"
                )
            
            # Execute the Flex program
            result = await self._execute_flex_file(
                str(temp_file),
                request.timeout
            )
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return FlexExecutionResult(
                success=result['success'],
                output=result['stdout'],
                error=result['stderr'] if not result['success'] else None,
                execution_time=execution_time,
                filename=str(temp_file) if temp_file else None,
                exit_code=result['exit_code']
            )
            
        except asyncio.TimeoutError:
            return FlexExecutionResult(
                success=False,
                output="",
                error=f"Execution timed out after {request.timeout} seconds",
                execution_time=request.timeout,
                filename=str(temp_file) if temp_file else None,
                exit_code=-1
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return FlexExecutionResult(
                success=False,
                output="",
                error=f"Execution failed: {str(e)}",
                execution_time=execution_time,
                filename=str(temp_file) if temp_file else None,
                exit_code=-1
            )
        
        finally:
            # Clean up process if still running
            if process_id and process_id in self.running_processes:
                await self._cleanup_process(process_id)
    
    async def _execute_flex_file(
        self, 
        filepath: str, 
        timeout: int
    ) -> Dict[str, Any]:
        """
        Execute a Flex file via CLI.
        
        Args:
            filepath: Path to Flex file
            timeout: Execution timeout in seconds
            
        Returns:
            Dictionary with execution results
        """
        # Check if Flex CLI is available
        if not await self._check_flex_cli():
            raise FlexExecutorError("Flex CLI not found or not accessible")
        
        # Generate unique process ID
        process_id = f"flex_{datetime.now().timestamp()}"
        
        try:
            # Create process with resource limits
            process = await asyncio.create_subprocess_exec(
                self.flex_cli_path,
                filepath,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                preexec_fn=self._set_process_limits
            )
            
            # Track the process
            self.running_processes[process_id] = process
            
            # Wait for completion with timeout and resource monitoring
            stdout, stderr = await asyncio.wait_for(
                self._monitor_process_execution(process),
                timeout=timeout
            )
            
            # Get exit code
            exit_code = process.returncode
            
            return {
                'success': exit_code == 0,
                'stdout': stdout.decode('utf-8', errors='replace').strip(),
                'stderr': stderr.decode('utf-8', errors='replace').strip(),
                'exit_code': exit_code
            }
            
        except asyncio.TimeoutError:
            # Kill the process if it times out
            if process_id in self.running_processes:
                await self._force_kill_process(self.running_processes[process_id])
            raise
            
        finally:
            # Clean up process tracking
            if process_id in self.running_processes:
                del self.running_processes[process_id]
    
    async def _monitor_process_execution(
        self, 
        process: asyncio.subprocess.Process
    ) -> tuple[bytes, bytes]:
        """
        Monitor process execution with resource usage checks.
        
        Args:
            process: The subprocess to monitor
            
        Returns:
            Tuple of (stdout, stderr)
        """
        monitor_task = asyncio.create_task(
            self._monitor_resource_usage(process.pid)
        )
        
        try:
            # Wait for process completion
            stdout, stderr = await process.communicate()
            return stdout, stderr
            
        finally:
            # Cancel monitoring
            monitor_task.cancel()
            try:
                await monitor_task
            except asyncio.CancelledError:
                pass
    
    async def _monitor_resource_usage(self, pid: int) -> None:
        """
        Monitor resource usage of a process and kill if exceeded.
        
        Args:
            pid: Process ID to monitor
        """
        try:
            proc = psutil.Process(pid)
            
            while proc.is_running():
                # Check memory usage
                memory_mb = proc.memory_info().rss / 1024 / 1024
                if memory_mb > self.max_memory_mb:
                    proc.kill()
                    raise FlexExecutorError(
                        f"Process killed: exceeded memory limit ({memory_mb:.1f}MB > {self.max_memory_mb}MB)"
                    )
                
                # Check CPU usage (averaged over 1 second)
                cpu_percent = proc.cpu_percent(interval=1.0)
                if cpu_percent > self.max_cpu_percent:
                    proc.kill()
                    raise FlexExecutorError(
                        f"Process killed: exceeded CPU limit ({cpu_percent:.1f}% > {self.max_cpu_percent}%)"
                    )
                
                # Wait before next check
                await asyncio.sleep(0.5)
                
        except psutil.NoSuchProcess:
            # Process ended naturally
            return
        except Exception as e:
            # Log error but don't fail the execution
            print(f"Warning: Resource monitoring failed: {e}")
    
    def _set_process_limits(self) -> None:
        """Set resource limits for child processes."""
        try:
            import resource
            
            # Set memory limit (in bytes)
            memory_limit = self.max_memory_mb * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
            
            # Set CPU time limit (in seconds)
            cpu_limit = self.default_timeout * 2  # Allow 2x timeout for CPU time
            resource.setrlimit(resource.RLIMIT_CPU, (cpu_limit, cpu_limit))
            
            # Set file size limit (10MB)
            file_limit = 10 * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_FSIZE, (file_limit, file_limit))
            
            # Set process group to allow clean killing
            os.setpgrp()
            
        except ImportError:
            # resource module not available (e.g., on Windows)
            pass
        except Exception as e:
            print(f"Warning: Failed to set process limits: {e}")
    
    async def _check_flex_cli(self) -> bool:
        """Check if Flex CLI is available and working."""
        try:
            process = await asyncio.create_subprocess_exec(
                self.flex_cli_path,
                '--version',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=5.0
            )
            
            return process.returncode == 0
            
        except (asyncio.TimeoutError, FileNotFoundError, Exception):
            return False
    
    async def _force_kill_process(self, process: asyncio.subprocess.Process) -> None:
        """Force kill a process and its children."""
        try:
            # Try graceful termination first
            process.terminate()
            
            # Wait briefly for graceful shutdown
            try:
                await asyncio.wait_for(process.wait(), timeout=2.0)
                return
            except asyncio.TimeoutError:
                pass
            
            # Force kill if still running
            process.kill()
            await process.wait()
            
        except Exception as e:
            print(f"Warning: Failed to kill process: {e}")
    
    async def _cleanup_process(self, process_id: str) -> None:
        """Clean up a tracked process."""
        if process_id in self.running_processes:
            process = self.running_processes[process_id]
            if process.returncode is None:  # Still running
                await self._force_kill_process(process)
            del self.running_processes[process_id]
    
    async def execute_code_string(
        self, 
        code: str, 
        timeout: Optional[int] = None
    ) -> FlexExecutionResult:
        """
        Execute Flex code from a string.
        
        Args:
            code: Flex code to execute
            timeout: Optional timeout (uses default if not provided)
            
        Returns:
            Execution result
        """
        request = FlexExecutionRequest(
            code=code,
            timeout=timeout or self.default_timeout,
            save_to_file=False
        )
        
        return await self.execute(request)
    
    async def execute_file(
        self, 
        filepath: str, 
        timeout: Optional[int] = None
    ) -> FlexExecutionResult:
        """
        Execute a Flex file.
        
        Args:
            filepath: Path to Flex file
            timeout: Optional timeout
            
        Returns:
            Execution result
        """
        # Read the file
        file_result = await self.file_manager.load_flex_code(filepath)
        
        if not file_result.success:
            return FlexExecutionResult(
                success=False,
                output="",
                error=f"Failed to read file: {file_result.message}",
                execution_time=0.0,
                filename=filepath
            )
        
        # Execute the code
        request = FlexExecutionRequest(
            code=file_result.content,
            filename=filepath,
            timeout=timeout or self.default_timeout,
            save_to_file=False
        )
        
        return await self.execute(request)
    
    async def get_running_processes(self) -> List[Dict[str, Any]]:
        """Get list of currently running Flex processes."""
        running = []
        
        for process_id, process in self.running_processes.items():
            if process.returncode is None:  # Still running
                try:
                    # Get process info
                    proc = psutil.Process(process.pid)
                    info = {
                        'process_id': process_id,
                        'pid': process.pid,
                        'memory_mb': proc.memory_info().rss / 1024 / 1024,
                        'cpu_percent': proc.cpu_percent(),
                        'status': proc.status(),
                        'create_time': datetime.fromtimestamp(proc.create_time())
                    }
                    running.append(info)
                except psutil.NoSuchProcess:
                    # Process ended, will be cleaned up
                    continue
        
        return running
    
    async def kill_all_processes(self) -> int:
        """Kill all running Flex processes."""
        killed = 0
        
        for process_id in list(self.running_processes.keys()):
            await self._cleanup_process(process_id)
            killed += 1
        
        return killed
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """Get execution statistics."""
        return {
            'cli_path': self.flex_cli_path,
            'default_timeout': self.default_timeout,
            'max_memory_mb': self.max_memory_mb,
            'max_cpu_percent': self.max_cpu_percent,
            'running_processes': len(self.running_processes),
            'cli_available': asyncio.run(self._check_flex_cli())
        }