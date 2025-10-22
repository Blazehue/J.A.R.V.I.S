"""
Validator for Jarvis V2
Validates commands before execution for safety and correctness
"""

import os
from pathlib import Path
from typing import Dict, Tuple, Optional
from utils.logger import get_logger
from utils.config_manager import get_config

logger = get_logger()
config = get_config()


class Validator:
    """Validates commands before execution"""
    
    def __init__(self):
        self.security_config = config.get('security', {})
        self.require_confirmation = self.security_config.get('require_confirmation', {})
        self.allowed_operations = self.security_config.get('allowed_operations', {})
    
    def validate(self, intent: str, parameters: Dict) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validate a command
        Returns: (is_valid, error_message, warning_message)
        """
        
        # Get the validator method for this intent
        validator_method = getattr(self, f'_validate_{intent}', None)
        
        if validator_method:
            return validator_method(parameters)
        
        # Default: allow if no specific validator
        return True, None, None
    
    def _validate_launch_app(self, params: Dict) -> Tuple[bool, Optional[str], Optional[str]]:
        """Validate app launch command"""
        if 'target' not in params or not params['target']:
            return False, "No application specified", None
        
        return True, None, None
    
    def _validate_close_app(self, params: Dict) -> Tuple[bool, Optional[str], Optional[str]]:
        """Validate app close command"""
        if 'target' not in params or not params['target']:
            return False, "No application specified", None
        
        # Check if confirmation is required
        if self.require_confirmation.get('app_close', False):
            warning = "This will close the application. Unsaved work may be lost."
            return True, None, warning
        
        return True, None, None
    
    def _validate_screenshot(self, params: Dict) -> Tuple[bool, Optional[str], Optional[str]]:
        """Validate screenshot command"""
        # Check if save path is valid
        save_path = params.get('save_path')
        if save_path:
            try:
                path = Path(save_path)
                if not path.parent.exists():
                    return False, f"Save directory does not exist: {path.parent}", None
            except Exception as e:
                return False, f"Invalid save path: {e}", None
        
        return True, None, None
    
    def _validate_delete_file(self, params: Dict) -> Tuple[bool, Optional[str], Optional[str]]:
        """Validate file deletion command"""
        if not self.allowed_operations.get('file_deletion', True):
            return False, "File deletion is disabled in security settings", None
        
        target = params.get('target')
        if not target:
            return False, "No file or folder specified", None
        
        # Check if it's a system file or directory
        if self._is_system_path(target):
            return False, "Cannot delete system files or directories", None
        
        # Always require confirmation for deletion
        warning = f"This will permanently delete: {target}"
        return True, None, warning
    
    def _validate_shutdown(self, params: Dict) -> Tuple[bool, Optional[str], Optional[str]]:
        """Validate shutdown command"""
        if self.require_confirmation.get('system_shutdown', True):
            warning = "This will shutdown the system. All applications will be closed."
            return True, None, warning
        
        return True, None, None
    
    def _validate_restart(self, params: Dict) -> Tuple[bool, Optional[str], Optional[str]]:
        """Validate restart command"""
        if self.require_confirmation.get('system_shutdown', True):
            warning = "This will restart the system. All applications will be closed."
            return True, None, warning
        
        return True, None, None
    
    def _validate_open_file(self, params: Dict) -> Tuple[bool, Optional[str], Optional[str]]:
        """Validate file open command"""
        target = params.get('target')
        if not target:
            return False, "No file or folder specified", None
        
        # Check if path exists
        if os.path.exists(target):
            return True, None, None
        
        # Path doesn't exist - not necessarily an error, might need to search
        return True, None, None
    
    def _validate_volume(self, params: Dict) -> Tuple[bool, Optional[str], Optional[str]]:
        """Validate volume command"""
        if 'value' in params:
            value = params['value']
            if not 0 <= value <= 100:
                return False, "Volume must be between 0 and 100", None
        
        return True, None, None
    
    def _validate_brightness(self, params: Dict) -> Tuple[bool, Optional[str], Optional[str]]:
        """Validate brightness command"""
        if 'value' in params:
            value = params['value']
            if not 0 <= value <= 100:
                return False, "Brightness must be between 0 and 100", None
        
        return True, None, None
    
    def _validate_create_folder(self, params: Dict) -> Tuple[bool, Optional[str], Optional[str]]:
        """Validate create folder command"""
        name = params.get('name')
        if not name:
            return False, "No folder name specified", None
        
        # Check for invalid characters
        invalid_chars = '<>:"/\\|?*'
        if any(char in name for char in invalid_chars):
            return False, f"Folder name contains invalid characters: {invalid_chars}", None
        
        return True, None, None
    
    def _is_system_path(self, path: str) -> bool:
        """Check if path is a system directory"""
        system_paths = [
            'C:\\Windows',
            'C:\\Program Files',
            'C:\\Program Files (x86)',
            os.environ.get('SYSTEMROOT', ''),
            os.environ.get('PROGRAMFILES', ''),
            os.environ.get('PROGRAMFILES(X86)', ''),
        ]
        
        abs_path = os.path.abspath(path).lower()
        
        for sys_path in system_paths:
            if sys_path and abs_path.startswith(sys_path.lower()):
                return True
        
        return False
    
    def is_safe_operation(self, intent: str) -> bool:
        """Check if an operation is generally safe to execute"""
        # Operations that are always safe
        safe_operations = [
            'greeting', 'status', 'help', 'thank',
            'time', 'date', 'weather', 'system_info',
            'list_apps', 'screenshot', 'screenshot_window'
        ]
        
        return intent in safe_operations
    
    def requires_confirmation(self, intent: str) -> bool:
        """Check if an intent requires user confirmation"""
        confirmation_intents = [
            'shutdown', 'restart', 'delete_file',
            'close_app'  # if configured
        ]
        
        if intent in ['close_app'] and not self.require_confirmation.get('app_close', False):
            return False
        
        return intent in confirmation_intents
