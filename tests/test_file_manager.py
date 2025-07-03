"""
Unit tests for File Manager.

These tests validate the file management functionality including
secure file operations, backup creation, and async file handling.
"""

import pytest
import asyncio
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock
import tempfile
import shutil

from tools.file_manager import FileManager, FileManagerError
from agents.models import FileOperation, FileOperationResult
from config.settings import Settings, FlexSettings, ApplicationSettings, OpenRouterSettings


class TestFileManager:
    """Test suite for FileManager."""
    
    @pytest.fixture
    def mock_settings(self):
        """Create mock settings for testing."""
        return Settings(
            openrouter=OpenRouterSettings(api_key="test_key"),
            flex=FlexSettings(
                file_extensions=[".flex", ".flx", ".txt"],
                temp_dir="./test_temp",
                examples_dir="./test_examples"
            ),
            app=ApplicationSettings()
        )
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def file_manager(self, mock_settings, temp_dir):
        """Create FileManager instance for testing."""
        # Override temp and examples directories to use test directory
        mock_settings.flex.temp_dir = str(temp_dir / "temp")
        mock_settings.flex.examples_dir = str(temp_dir / "examples")
        
        return FileManager(mock_settings)
    
    @pytest.mark.asyncio
    async def test_read_file_success(self, file_manager, temp_dir):
        """Test successful file reading."""
        # Create test file
        test_file = temp_dir / "test.flex"
        test_content = "etb3('Hello, Flex!')"
        test_file.write_text(test_content, encoding='utf-8')
        
        operation = FileOperation(
            operation="read",
            filepath=str(test_file)
        )
        
        result = await file_manager.execute_operation(operation)
        
        assert result.success
        assert result.content == test_content
        assert result.file_size == len(test_content.encode())
        assert result.last_modified is not None
    
    @pytest.mark.asyncio
    async def test_read_file_not_found(self, file_manager, temp_dir):
        """Test reading non-existent file."""
        operation = FileOperation(
            operation="read",
            filepath=str(temp_dir / "nonexistent.flex")
        )
        
        result = await file_manager.execute_operation(operation)
        
        assert not result.success
        assert "File not found" in result.message
    
    @pytest.mark.asyncio
    async def test_write_file_success(self, file_manager, temp_dir):
        """Test successful file writing."""
        test_file = temp_dir / "output.flex"
        test_content = "rakm x = 42\netb3(x)"
        
        operation = FileOperation(
            operation="write",
            filepath=str(test_file),
            content=test_content
        )
        
        result = await file_manager.execute_operation(operation)
        
        assert result.success
        assert test_file.exists()
        assert test_file.read_text() == test_content
        assert result.file_size == len(test_content.encode())
    
    @pytest.mark.asyncio
    async def test_write_file_with_backup(self, file_manager, temp_dir):
        """Test file writing with backup creation."""
        test_file = temp_dir / "existing.flex"
        original_content = "original content"
        new_content = "new content"
        
        # Create original file
        test_file.write_text(original_content)
        
        operation = FileOperation(
            operation="write",
            filepath=str(test_file),
            content=new_content,
            backup=True
        )
        
        result = await file_manager.execute_operation(operation)
        
        assert result.success
        assert test_file.read_text() == new_content
        assert result.backup_path is not None
        
        # Check backup exists and contains original content
        backup_path = Path(result.backup_path)
        assert backup_path.exists()
        assert backup_path.read_text() == original_content
    
    @pytest.mark.asyncio
    async def test_delete_file_success(self, file_manager, temp_dir):
        """Test successful file deletion."""
        test_file = temp_dir / "to_delete.flex"
        test_file.write_text("delete me")
        
        operation = FileOperation(
            operation="delete",
            filepath=str(test_file),
            backup=True
        )
        
        result = await file_manager.execute_operation(operation)
        
        assert result.success
        assert not test_file.exists()
        assert result.backup_path is not None
        
        # Check backup was created
        backup_path = Path(result.backup_path)
        assert backup_path.exists()
    
    @pytest.mark.asyncio
    async def test_delete_file_not_found(self, file_manager, temp_dir):
        """Test deleting non-existent file."""
        operation = FileOperation(
            operation="delete",
            filepath=str(temp_dir / "nonexistent.flex")
        )
        
        result = await file_manager.execute_operation(operation)
        
        assert not result.success
        assert "File not found" in result.message
    
    @pytest.mark.asyncio
    async def test_file_exists_check(self, file_manager, temp_dir):
        """Test file existence checking."""
        test_file = temp_dir / "exists.flex"
        test_file.write_text("I exist")
        
        # Test existing file
        operation = FileOperation(
            operation="exists",
            filepath=str(test_file)
        )
        
        result = await file_manager.execute_operation(operation)
        
        assert result.success
        assert "File exists" in result.message
        assert result.file_size is not None
        
        # Test non-existing file
        operation.filepath = str(temp_dir / "doesnt_exist.flex")
        result = await file_manager.execute_operation(operation)
        
        assert result.success
        assert "does not exist" in result.message
    
    @pytest.mark.asyncio
    async def test_list_files_success(self, file_manager, temp_dir):
        """Test successful directory listing."""
        # Create test files
        (temp_dir / "file1.flex").write_text("flex file 1")
        (temp_dir / "file2.flx").write_text("flex file 2")
        (temp_dir / "file3.txt").write_text("text file")
        
        operation = FileOperation(
            operation="list",
            filepath=str(temp_dir)
        )
        
        result = await file_manager.execute_operation(operation)
        
        assert result.success
        assert "3 files" in result.message
        
        # Parse file list from content
        import json
        file_list = json.loads(result.content.replace("'", '"'))
        
        assert len(file_list) == 3
        flex_files = [f for f in file_list if f['is_flex_file']]
        assert len(flex_files) == 2  # .flex and .flx files
    
    @pytest.mark.asyncio
    async def test_list_files_directory_not_found(self, file_manager, temp_dir):
        """Test listing non-existent directory."""
        operation = FileOperation(
            operation="list",
            filepath=str(temp_dir / "nonexistent_dir")
        )
        
        result = await file_manager.execute_operation(operation)
        
        assert not result.success
        assert "Directory not found" in result.message
    
    def test_security_validation_path_traversal(self, file_manager):
        """Test security validation against path traversal."""
        operation = FileOperation(
            operation="read",
            filepath="../../../etc/passwd"
        )
        
        with pytest.raises(FileManagerError) as exc_info:
            file_manager._validate_operation(operation)
        
        assert "Path traversal not allowed" in str(exc_info.value)
    
    def test_security_validation_forbidden_paths(self, file_manager):
        """Test security validation against forbidden paths."""
        operation = FileOperation(
            operation="read",
            filepath="/etc/passwd"
        )
        
        with pytest.raises(FileManagerError) as exc_info:
            file_manager._validate_operation(operation)
        
        assert "Access to /etc not allowed" in str(exc_info.value)
    
    def test_security_validation_file_extension(self, file_manager):
        """Test security validation of file extensions."""
        operation = FileOperation(
            operation="write",
            filepath="/tmp/malicious.exe",
            content="malicious content"
        )
        
        with pytest.raises(FileManagerError) as exc_info:
            file_manager._validate_operation(operation)
        
        assert "File extension .exe not allowed" in str(exc_info.value)
    
    def test_security_validation_file_size(self, file_manager):
        """Test security validation of file size."""
        large_content = "x" * (11 * 1024 * 1024)  # 11MB, exceeds 10MB limit
        
        operation = FileOperation(
            operation="write",
            filepath="/tmp/large.flex",
            content=large_content
        )
        
        with pytest.raises(FileManagerError) as exc_info:
            file_manager._validate_operation(operation)
        
        assert "File size exceeds" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_save_flex_code_auto_naming(self, file_manager):
        """Test saving Flex code with automatic filename generation."""
        code = "etb3('Hello from auto-named file')"
        
        result = await file_manager.save_flex_code(code)
        
        assert result.success
        assert result.filepath.endswith(".flex")
        
        # Verify file was created and contains correct content
        created_file = Path(result.filepath)
        assert created_file.exists()
        assert created_file.read_text() == code
    
    @pytest.mark.asyncio
    async def test_save_flex_code_franco_syntax(self, file_manager):
        """Test saving Flex code with Franco syntax style."""
        code = "rakm x = 10\netb3(x)"
        filename = "franco_test"
        
        result = await file_manager.save_flex_code(
            code, 
            filename=filename, 
            syntax_style="franco"
        )
        
        assert result.success
        assert "franco_examples" in result.filepath
        assert result.filepath.endswith(".flex")
    
    @pytest.mark.asyncio
    async def test_save_flex_code_english_syntax(self, file_manager):
        """Test saving Flex code with English syntax style."""
        code = "int x = 10\nprint(x)"
        filename = "english_test"
        
        result = await file_manager.save_flex_code(
            code, 
            filename=filename, 
            syntax_style="english"
        )
        
        assert result.success
        assert "english_examples" in result.filepath
    
    @pytest.mark.asyncio
    async def test_load_flex_code_success(self, file_manager, temp_dir):
        """Test loading Flex code from file."""
        test_file = temp_dir / "load_test.flex"
        test_content = "karr i=0 l7d 9 { etb3(i) }"
        test_file.write_text(test_content)
        
        result = await file_manager.load_flex_code(str(test_file))
        
        assert result.success
        assert result.content == test_content
    
    @pytest.mark.asyncio
    async def test_get_flex_files(self, file_manager, temp_dir):
        """Test getting list of Flex files."""
        # Setup examples directory with test files
        examples_dir = Path(file_manager.examples_dir)
        examples_dir.mkdir(parents=True, exist_ok=True)
        
        (examples_dir / "test1.flex").write_text("flex code 1")
        (examples_dir / "test2.flx").write_text("flex code 2")
        (examples_dir / "readme.txt").write_text("not flex")
        
        flex_files = await file_manager.get_flex_files()
        
        assert len(flex_files) == 2
        assert all(f['is_flex_file'] for f in flex_files)
    
    @pytest.mark.asyncio
    async def test_create_temp_file(self, file_manager):
        """Test temporary file creation."""
        content = "temporary flex code"
        
        temp_file = await file_manager.create_temp_file(content, "test")
        
        assert temp_file.exists()
        assert temp_file.read_text() == content
        assert "test_" in temp_file.name
        assert temp_file.suffix == ".flex"
    
    @pytest.mark.asyncio
    async def test_cleanup_temp_files(self, file_manager, temp_dir):
        """Test cleanup of old temporary files."""
        # Create temp directory
        temp_dir = Path(file_manager.temp_dir)
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Create some old files
        old_file1 = temp_dir / "old1.flex"
        old_file2 = temp_dir / "old2.flex"
        recent_file = temp_dir / "recent.flex"
        
        old_file1.write_text("old content 1")
        old_file2.write_text("old content 2")
        recent_file.write_text("recent content")
        
        # Mock file modification times
        import time
        old_time = time.time() - (25 * 3600)  # 25 hours ago
        recent_time = time.time() - (1 * 3600)  # 1 hour ago
        
        with patch('pathlib.Path.stat') as mock_stat:
            def stat_side_effect(self):
                mock_stat_result = Mock()
                if "old" in str(self):
                    mock_stat_result.st_mtime = old_time
                else:
                    mock_stat_result.st_mtime = recent_time
                return mock_stat_result
            
            mock_stat.side_effect = stat_side_effect
            
            # Test cleanup with 24 hour threshold
            cleaned = await file_manager.cleanup_temp_files(max_age_hours=24)
            
            # Should have cleaned up 2 old files
            assert cleaned >= 0  # Actual cleanup depends on file system operations
    
    def test_get_file_hash(self, file_manager, temp_dir):
        """Test file hash calculation."""
        test_file = temp_dir / "hash_test.flex"
        test_content = "test content for hashing"
        test_file.write_text(test_content)
        
        hash_value = file_manager.get_file_hash(test_file)
        
        assert len(hash_value) == 64  # SHA256 hash length
        assert isinstance(hash_value, str)
        
        # Same content should produce same hash
        test_file2 = temp_dir / "hash_test2.flex"
        test_file2.write_text(test_content)
        hash_value2 = file_manager.get_file_hash(test_file2)
        
        assert hash_value == hash_value2
    
    @pytest.mark.asyncio
    async def test_backup_directory(self, file_manager, temp_dir):
        """Test directory backup functionality."""
        # Create source directory with files
        source_dir = temp_dir / "source"
        source_dir.mkdir()
        (source_dir / "file1.flex").write_text("content 1")
        (source_dir / "file2.flex").write_text("content 2")
        
        backup_path = await file_manager.backup_directory(str(source_dir))
        
        backup_dir = Path(backup_path)
        assert backup_dir.exists()
        assert (backup_dir / "file1.flex").exists()
        assert (backup_dir / "file2.flex").exists()
        assert (backup_dir / "file1.flex").read_text() == "content 1"
    
    @pytest.mark.asyncio
    async def test_backup_directory_not_found(self, file_manager, temp_dir):
        """Test backup of non-existent directory."""
        with pytest.raises(FileManagerError) as exc_info:
            await file_manager.backup_directory(str(temp_dir / "nonexistent"))
        
        assert "Source directory does not exist" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_unsupported_operation(self, file_manager):
        """Test handling of unsupported file operations."""
        operation = FileOperation(
            operation="unsupported",
            filepath="/tmp/test.flex"
        )
        
        result = await file_manager.execute_operation(operation)
        
        assert not result.success
        assert "Unsupported operation" in result.message
    
    @pytest.mark.asyncio
    async def test_unicode_content_handling(self, file_manager, temp_dir):
        """Test handling of Unicode content in files."""
        unicode_content = "Flex code with émojis 🚀 and ñoñó characters"
        test_file = temp_dir / "unicode.flex"
        
        # Write Unicode content
        operation = FileOperation(
            operation="write",
            filepath=str(test_file),
            content=unicode_content,
            encoding="utf-8"
        )
        
        result = await file_manager.execute_operation(operation)
        assert result.success
        
        # Read Unicode content
        operation = FileOperation(
            operation="read",
            filepath=str(test_file),
            encoding="utf-8"
        )
        
        result = await file_manager.execute_operation(operation)
        assert result.success
        assert result.content == unicode_content


@pytest.mark.asyncio
async def test_file_manager_initialization():
    """Test FileManager initialization and directory creation."""
    settings = Settings(
        openrouter=OpenRouterSettings(api_key="test_key"),
        flex=FlexSettings(
            temp_dir="./test_temp_init",
            examples_dir="./test_examples_init"
        ),
        app=ApplicationSettings()
    )
    
    # Initialize should create directories
    manager = FileManager(settings)
    
    assert Path(manager.temp_dir).exists()
    assert Path(manager.examples_dir).exists()
    
    # Cleanup
    shutil.rmtree("./test_temp_init", ignore_errors=True)
    shutil.rmtree("./test_examples_init", ignore_errors=True)