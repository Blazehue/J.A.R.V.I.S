"""
File Manager for Jarvis V2
Handles file and folder operations
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict, Optional
import subprocess
from utils.logger import get_logger
from utils.config_manager import get_config
from utils.helpers import format_file_size, get_desktop_path, get_documents_path, get_downloads_path

logger = get_logger()
config = get_config()


class FileManager:
    """Manages file and folder operations"""
    
    def __init__(self):
        self.search_locations = config.get('files.search_locations', [
            str(get_documents_path()),
            str(get_downloads_path()),
            str(get_desktop_path())
        ])
        self.max_results = config.get('files.max_search_results', 50)
        self.search_timeout = config.get('files.search_timeout', 30)
    
    def open_file(self, filepath: str) -> Dict[str, any]:
        """
        Open a file or folder with default application
        """
        try:
            path = Path(filepath)
            
            if not path.exists():
                # Try to resolve common locations
                resolved_path = self._resolve_path(filepath)
                if resolved_path:
                    path = resolved_path
                else:
                    return {
                        'success': False,
                        'message': f"File or folder not found: {filepath}"
                    }
            
            logger.info(f"Opening: {path}")
            
            # Open with default application
            os.startfile(str(path))
            
            return {
                'success': True,
                'message': f"Opened {path.name}"
            }
            
        except Exception as e:
            logger.error(f"Error opening file: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}"
            }
    
    def find_files(self, query: str, location: Optional[str] = None,
                  file_type: Optional[str] = None) -> Dict[str, any]:
        """
        Search for files matching query
        """
        try:
            logger.info(f"Searching for files: {query}")
            
            search_paths = [location] if location else self.search_locations
            results = []
            
            for search_path in search_paths:
                if not os.path.exists(search_path):
                    continue
                
                # Search recursively
                for root, dirs, files in os.walk(search_path):
                    # Check files
                    for file in files:
                        if self._matches_query(file, query, file_type):
                            filepath = Path(root) / file
                            results.append({
                                'name': file,
                                'path': str(filepath),
                                'size': format_file_size(filepath.stat().st_size),
                                'modified': filepath.stat().st_mtime
                            })
                            
                            if len(results) >= self.max_results:
                                break
                    
                    if len(results) >= self.max_results:
                        break
            
            # Sort by modified date (newest first)
            results.sort(key=lambda x: x['modified'], reverse=True)
            
            logger.info(f"Found {len(results)} file(s)")
            return {
                'success': True,
                'files': results,
                'count': len(results),
                'truncated': len(results) >= self.max_results
            }
            
        except Exception as e:
            logger.error(f"Error searching files: {e}")
            return {
                'success': False,
                'files': [],
                'message': f"Error: {str(e)}"
            }
    
    def create_folder(self, name: str, location: Optional[str] = None) -> Dict[str, any]:
        """
        Create a new folder
        """
        try:
            if location:
                folder_path = Path(location) / name
            else:
                # Default to Documents
                folder_path = get_documents_path() / name
            
            logger.info(f"Creating folder: {folder_path}")
            
            if folder_path.exists():
                return {
                    'success': False,
                    'message': f"Folder already exists: {name}"
                }
            
            folder_path.mkdir(parents=True, exist_ok=False)
            
            return {
                'success': True,
                'path': str(folder_path),
                'message': f"Folder created: {name}"
            }
            
        except Exception as e:
            logger.error(f"Error creating folder: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}"
            }
    
    def delete_file(self, filepath: str) -> Dict[str, any]:
        """
        Delete a file or folder
        """
        try:
            path = Path(filepath)
            
            if not path.exists():
                return {
                    'success': False,
                    'message': f"File or folder not found: {filepath}"
                }
            
            logger.info(f"Deleting: {path}")
            
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            
            return {
                'success': True,
                'message': f"Deleted: {path.name}"
            }
            
        except Exception as e:
            logger.error(f"Error deleting: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}"
            }
    
    def move_file(self, source: str, destination: str) -> Dict[str, any]:
        """
        Move a file or folder
        """
        try:
            src_path = Path(source)
            dst_path = Path(destination)
            
            if not src_path.exists():
                return {
                    'success': False,
                    'message': f"Source not found: {source}"
                }
            
            logger.info(f"Moving {src_path} to {dst_path}")
            
            shutil.move(str(src_path), str(dst_path))
            
            return {
                'success': True,
                'message': f"Moved {src_path.name} to {dst_path}"
            }
            
        except Exception as e:
            logger.error(f"Error moving file: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}"
            }
    
    def copy_file(self, source: str, destination: str) -> Dict[str, any]:
        """
        Copy a file or folder
        """
        try:
            src_path = Path(source)
            dst_path = Path(destination)
            
            if not src_path.exists():
                return {
                    'success': False,
                    'message': f"Source not found: {source}"
                }
            
            logger.info(f"Copying {src_path} to {dst_path}")
            
            if src_path.is_dir():
                shutil.copytree(str(src_path), str(dst_path))
            else:
                shutil.copy2(str(src_path), str(dst_path))
            
            return {
                'success': True,
                'message': f"Copied {src_path.name} to {dst_path}"
            }
            
        except Exception as e:
            logger.error(f"Error copying file: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}"
            }
    
    def get_file_info(self, filepath: str) -> Dict[str, any]:
        """
        Get detailed information about a file
        """
        try:
            path = Path(filepath)
            
            if not path.exists():
                return {
                    'success': False,
                    'message': f"File not found: {filepath}"
                }
            
            stat = path.stat()
            
            info = {
                'success': True,
                'name': path.name,
                'path': str(path.absolute()),
                'size': format_file_size(stat.st_size),
                'size_bytes': stat.st_size,
                'created': stat.st_ctime,
                'modified': stat.st_mtime,
                'accessed': stat.st_atime,
                'is_directory': path.is_dir(),
                'extension': path.suffix
            }
            
            return info
            
        except Exception as e:
            logger.error(f"Error getting file info: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}"
            }
    
    def _matches_query(self, filename: str, query: str, file_type: Optional[str]) -> bool:
        """Check if filename matches search query"""
        filename_lower = filename.lower()
        query_lower = query.lower()
        
        # Check file type
        if file_type:
            if not filename_lower.endswith(f'.{file_type.lower()}'):
                return False
        
        # Check if query is in filename
        return query_lower in filename_lower
    
    def _resolve_path(self, path_str: str) -> Optional[Path]:
        """Resolve common path shortcuts"""
        path_lower = path_str.lower()
        
        # Common shortcuts
        shortcuts = {
            'desktop': get_desktop_path(),
            'documents': get_documents_path(),
            'downloads': get_downloads_path(),
            'my documents': get_documents_path(),
        }
        
        for shortcut, actual_path in shortcuts.items():
            if shortcut in path_lower:
                # Replace shortcut with actual path
                resolved = str(actual_path) + path_str[len(shortcut):]
                resolved_path = Path(resolved)
                if resolved_path.exists():
                    return resolved_path
        
        return None
