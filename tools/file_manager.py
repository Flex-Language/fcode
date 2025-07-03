"""
File Management Tool for Flex AI Agent.

This module provides secure async file operations for Flex code files (.flex, .flx)
with backup functionality and proper error handling.
"""

import os
import aiofiles
import asyncio
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
import shutil
import hashlib
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))

from agents.models import FileOperation, FileOperationResult
from config.settings import Settings, get_settings


class FileManagerError(Exception):
    """Custom exception for file manager errors."""
    pass


class FileManager:
    """Manages file operations for Flex code files."""
    
    def __init__(self, settings: Optional[Settings] = None):
        """Initialize file manager with settings."""
        self.settings = settings or get_settings()
        self.flex_extensions = self.settings.flex.file_extensions
        self.temp_dir = Path(self.settings.flex.temp_dir)
        self.examples_dir = Path(self.settings.flex.examples_dir)
        
        # Create directories if they don't exist
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.examples_dir.mkdir(parents=True, exist_ok=True)
        
        # Security settings
        self.max_file_size = 10 * 1024 * 1024  # 10MB max file size
        self.allowed_extensions = {'.flex', '.lx','.txt'}
        self.forbidden_paths = {'/etc', '/usr', '/bin', '/sbin', '/sys', '/proc'}
    
    async def execute_operation(self, operation: FileOperation) -> FileOperationResult:
        """
        Execute a file operation with security checks.
        
        Args:
            operation: File operation to execute
            
        Returns:
            Result of the file operation
        """
        # Security validation
        self._validate_operation(operation)
        
        try:
            if operation.operation == 'read':
                return await self._read_file(operation)
            elif operation.operation == 'write':
                return await self._write_file(operation)
            elif operation.operation == 'delete':
                return await self._delete_file(operation)
            elif operation.operation == 'exists':
                return await self._check_file_exists(operation)
            elif operation.operation == 'list':
                return await self._list_files(operation)
            else:
                raise FileManagerError(f"Unsupported operation: {operation.operation}")
                
        except Exception as e:
            return FileOperationResult(
                success=False,
                message=f"Operation failed: {str(e)}",
                filepath=operation.filepath
            )
    
    def _validate_operation(self, operation: FileOperation) -> None:
        """Validate file operation for security."""
        filepath = Path(operation.filepath).resolve()
        
        # Check for path traversal attacks
        if '..' in str(filepath):
            raise FileManagerError("Path traversal not allowed")
        
        # Check forbidden paths
        for forbidden in self.forbidden_paths:
            if str(filepath).startswith(forbidden):
                raise FileManagerError(f"Access to {forbidden} not allowed")
        
        # Check file extension for write operations
        if operation.operation == 'write':
            if filepath.suffix not in self.allowed_extensions:
                raise FileManagerError(f"File extension {filepath.suffix} not allowed")
        
        # Check file size for write operations
        if operation.operation == 'write' and operation.content:
            if len(operation.content.encode()) > self.max_file_size:
                raise FileManagerError(f"File size exceeds {self.max_file_size} bytes")
    
    async def _read_file(self, operation: FileOperation) -> FileOperationResult:
        """Read a file asynchronously."""
        filepath = Path(operation.filepath)
        
        if not filepath.exists():
            return FileOperationResult(
                success=False,
                message=f"File not found: {filepath}",
                filepath=str(filepath)
            )
        
        try:
            async with aiofiles.open(filepath, 'r', encoding=operation.encoding) as f:
                content = await f.read()
            
            # Get file metadata
            stat = filepath.stat()
            
            return FileOperationResult(
                success=True,
                message=f"Successfully read file: {filepath}",
                content=content,
                filepath=str(filepath),
                file_size=stat.st_size,
                last_modified=datetime.fromtimestamp(stat.st_mtime)
            )
            
        except UnicodeDecodeError:
            return FileOperationResult(
                success=False,
                message=f"Could not decode file with encoding {operation.encoding}",
                filepath=str(filepath)
            )
        except Exception as e:
            return FileOperationResult(
                success=False,
                message=f"Error reading file: {str(e)}",
                filepath=str(filepath)
            )
    
    async def _write_file(self, operation: FileOperation) -> FileOperationResult:
        """Write a file asynchronously with backup support."""
        filepath = Path(operation.filepath)
        backup_path = None
        
        # Create parent directories if needed
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Create backup if file exists and backup is requested
        if filepath.exists() and operation.backup:
            backup_path = await self._create_backup(filepath)
        
        try:
            async with aiofiles.open(filepath, 'w', encoding=operation.encoding) as f:
                await f.write(operation.content or "")
            
            # Get file metadata after write
            stat = filepath.stat()
            
            return FileOperationResult(
                success=True,
                message=f"Successfully wrote file: {filepath}",
                filepath=str(filepath),
                backup_path=str(backup_path) if backup_path else None,
                file_size=stat.st_size,
                last_modified=datetime.fromtimestamp(stat.st_mtime)
            )
            
        except Exception as e:
            # Restore backup if write failed and backup exists
            if backup_path and backup_path.exists():
                shutil.copy2(backup_path, filepath)
            
            return FileOperationResult(
                success=False,
                message=f"Error writing file: {str(e)}",
                filepath=str(filepath),
                backup_path=str(backup_path) if backup_path else None
            )
    
    async def _delete_file(self, operation: FileOperation) -> FileOperationResult:
        """Delete a file with backup support."""
        filepath = Path(operation.filepath)
        backup_path = None
        
        if not filepath.exists():
            return FileOperationResult(
                success=False,
                message=f"File not found: {filepath}",
                filepath=str(filepath)
            )
        
        # Create backup if requested
        if operation.backup:
            backup_path = await self._create_backup(filepath)
        
        try:
            filepath.unlink()
            
            return FileOperationResult(
                success=True,
                message=f"Successfully deleted file: {filepath}",
                filepath=str(filepath),
                backup_path=str(backup_path) if backup_path else None
            )
            
        except Exception as e:
            return FileOperationResult(
                success=False,
                message=f"Error deleting file: {str(e)}",
                filepath=str(filepath),
                backup_path=str(backup_path) if backup_path else None
            )
    
    async def _check_file_exists(self, operation: FileOperation) -> FileOperationResult:
        """Check if a file exists."""
        filepath = Path(operation.filepath)
        exists = filepath.exists()
        
        if exists:
            stat = filepath.stat()
            return FileOperationResult(
                success=True,
                message=f"File exists: {filepath}",
                filepath=str(filepath),
                file_size=stat.st_size,
                last_modified=datetime.fromtimestamp(stat.st_mtime)
            )
        else:
            return FileOperationResult(
                success=True,
                message=f"File does not exist: {filepath}",
                filepath=str(filepath)
            )
    
    async def _list_files(self, operation: FileOperation) -> FileOperationResult:
        """List files in a directory."""
        dirpath = Path(operation.filepath)
        
        if not dirpath.exists():
            return FileOperationResult(
                success=False,
                message=f"Directory not found: {dirpath}",
                filepath=str(dirpath)
            )
        
        if not dirpath.is_dir():
            return FileOperationResult(
                success=False,
                message=f"Path is not a directory: {dirpath}",
                filepath=str(dirpath)
            )
        
        try:
            files = []
            for item in dirpath.iterdir():
                if item.is_file():
                    stat = item.stat()
                    files.append({
                        'name': item.name,
                        'path': str(item),
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'is_flex_file': item.suffix in self.flex_extensions
                    })
            
            # Sort by modification time, newest first
            files.sort(key=lambda x: x['modified'], reverse=True)
            
            return FileOperationResult(
                success=True,
                message=f"Listed {len(files)} files in {dirpath}",
                content=str(files),  # JSON string of file list
                filepath=str(dirpath)
            )
            
        except Exception as e:
            return FileOperationResult(
                success=False,
                message=f"Error listing directory: {str(e)}",
                filepath=str(dirpath)
            )
    
    async def _create_backup(self, filepath: Path) -> Path:
        """Create a backup of a file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{filepath.stem}_{timestamp}_backup{filepath.suffix}"
        backup_path = filepath.parent / backup_name
        
        # Use asyncio to run sync copy operation
        await asyncio.get_event_loop().run_in_executor(
            None, shutil.copy2, str(filepath), str(backup_path)
        )
        
        return backup_path
    
    async def save_flex_code(
        self, 
        code: str, 
        filename: Optional[str] = None,
        syntax_style: str = "auto"
    ) -> FileOperationResult:
        """
        Save Flex code with appropriate filename and location.
        
        Args:
            code: Flex code to save
            filename: Optional filename (will generate if not provided)
            syntax_style: Syntax style for directory organization
            
        Returns:
            File operation result
        """
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"flex_code_{timestamp}.flex"
        
        # Ensure proper extension
        if not any(filename.endswith(ext) for ext in self.flex_extensions):
            filename += ".flex"
        
        # Determine save location based on syntax style
        if syntax_style.lower() == "franco":
            save_dir = self.examples_dir / "franco_examples"
        elif syntax_style.lower() == "english":
            save_dir = self.examples_dir / "english_examples"
        else:
            save_dir = self.examples_dir
        
        save_dir.mkdir(parents=True, exist_ok=True)
        filepath = save_dir / filename
        
        # Create operation and execute
        operation = FileOperation(
            operation="write",
            filepath=str(filepath),
            content=code,
            backup=True
        )
        
        return await self.execute_operation(operation)
    
    async def load_flex_code(self, filepath: str) -> FileOperationResult:
        """Load Flex code from a file."""
        operation = FileOperation(
            operation="read",
            filepath=filepath
        )
        
        return await self.execute_operation(operation)
    
    async def get_flex_files(self, directory: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get list of Flex files in a directory.
        
        Args:
            directory: Directory to search (defaults to examples directory)
            
        Returns:
            List of Flex file information
        """
        if directory is None:
            directory = str(self.examples_dir)
        
        operation = FileOperation(
            operation="list",
            filepath=directory
        )
        
        result = await self.execute_operation(operation)
        
        if result.success and result.content:
            try:
                import json
                all_files = json.loads(result.content.replace("'", '"'))
                # Filter for Flex files only
                flex_files = [f for f in all_files if f.get('is_flex_file', False)]
                return flex_files
            except:
                return []
        
        return []
    
    async def create_temp_file(self, content: str, prefix: str = "temp") -> Path:
        """
        Create a temporary file with content.
        
        Args:
            content: File content
            prefix: Filename prefix
            
        Returns:
            Path to created temporary file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{prefix}_{timestamp}.flex"
        filepath = self.temp_dir / filename
        
        operation = FileOperation(
            operation="write",
            filepath=str(filepath),
            content=content,
            backup=False
        )
        
        result = await self.execute_operation(operation)
        
        if result.success:
            return filepath
        else:
            raise FileManagerError(f"Failed to create temp file: {result.message}")
    
    async def cleanup_temp_files(self, max_age_hours: int = 24) -> int:
        """
        Clean up old temporary files.
        
        Args:
            max_age_hours: Maximum age of files to keep
            
        Returns:
            Number of files cleaned up
        """
        if not self.temp_dir.exists():
            return 0
        
        cleaned = 0
        cutoff_time = datetime.now().timestamp() - (max_age_hours * 3600)
        
        for filepath in self.temp_dir.iterdir():
            if filepath.is_file():
                if filepath.stat().st_mtime < cutoff_time:
                    try:
                        filepath.unlink()
                        cleaned += 1
                    except Exception:
                        continue  # Skip files that can't be deleted
        
        return cleaned
    
    def get_file_hash(self, filepath: Path) -> str:
        """Get SHA256 hash of a file."""
        hasher = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    async def backup_directory(self, source_dir: str, backup_name: Optional[str] = None) -> str:
        """
        Create a backup of an entire directory.
        
        Args:
            source_dir: Directory to backup
            backup_name: Optional backup name
            
        Returns:
            Path to backup directory
        """
        source_path = Path(source_dir)
        
        if not source_path.exists():
            raise FileManagerError(f"Source directory does not exist: {source_dir}")
        
        if backup_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{source_path.name}_backup_{timestamp}"
        
        backup_path = source_path.parent / backup_name
        
        # Use asyncio to run sync copy operation
        await asyncio.get_event_loop().run_in_executor(
            None, shutil.copytree, str(source_path), str(backup_path)
        )
        
        return str(backup_path)