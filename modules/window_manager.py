"""
Window Manager for Jarvis V2
Handles window positioning and management
"""

from typing import Dict, Optional, Tuple
from utils.logger import get_logger

logger = get_logger()


class WindowManager:
    """Manages window positioning and layout"""
    
    def __init__(self):
        try:
            import win32gui
            import win32con
            self.win32gui = win32gui
            self.win32con = win32con
            self.available = True
        except ImportError:
            logger.warning("pywin32 not available - window management disabled")
            self.available = False
    
    def maximize_window(self) -> Dict[str, any]:
        """Maximize the active window"""
        if not self.available:
            return {'success': False, 'message': "Window management requires pywin32"}
        
        try:
            hwnd = self.win32gui.GetForegroundWindow()
            self.win32gui.ShowWindow(hwnd, self.win32con.SW_MAXIMIZE)
            
            logger.info("Window maximized")
            return {'success': True, 'message': "Window maximized"}
            
        except Exception as e:
            logger.error(f"Error maximizing window: {e}")
            return {'success': False, 'message': f"Error: {str(e)}"}
    
    def minimize_window(self) -> Dict[str, any]:
        """Minimize the active window"""
        if not self.available:
            return {'success': False, 'message': "Window management requires pywin32"}
        
        try:
            hwnd = self.win32gui.GetForegroundWindow()
            self.win32gui.ShowWindow(hwnd, self.win32con.SW_MINIMIZE)
            
            logger.info("Window minimized")
            return {'success': True, 'message': "Window minimized"}
            
        except Exception as e:
            logger.error(f"Error minimizing window: {e}")
            return {'success': False, 'message': f"Error: {str(e)}"}
    
    def restore_window(self) -> Dict[str, any]:
        """Restore the active window to normal size"""
        if not self.available:
            return {'success': False, 'message': "Window management requires pywin32"}
        
        try:
            hwnd = self.win32gui.GetForegroundWindow()
            self.win32gui.ShowWindow(hwnd, self.win32con.SW_RESTORE)
            
            logger.info("Window restored")
            return {'success': True, 'message': "Window restored"}
            
        except Exception as e:
            logger.error(f"Error restoring window: {e}")
            return {'success': False, 'message': f"Error: {str(e)}"}
    
    def move_window(self, x: int, y: int, width: int, height: int) -> Dict[str, any]:
        """Move and resize the active window"""
        if not self.available:
            return {'success': False, 'message': "Window management requires pywin32"}
        
        try:
            hwnd = self.win32gui.GetForegroundWindow()
            self.win32gui.MoveWindow(hwnd, x, y, width, height, True)
            
            logger.info(f"Window moved to ({x}, {y}, {width}, {height})")
            return {'success': True, 'message': "Window moved"}
            
        except Exception as e:
            logger.error(f"Error moving window: {e}")
            return {'success': False, 'message': f"Error: {str(e)}"}
    
    def snap_left(self) -> Dict[str, any]:
        """Snap active window to left half of screen"""
        if not self.available:
            return {'success': False, 'message': "Window management requires pywin32"}
        
        try:
            import win32api
            
            # Get screen dimensions
            screen_width = win32api.GetSystemMetrics(0)
            screen_height = win32api.GetSystemMetrics(1)
            
            # Move to left half
            self.move_window(0, 0, screen_width // 2, screen_height)
            
            logger.info("Window snapped to left")
            return {'success': True, 'message': "Window snapped to left"}
            
        except Exception as e:
            logger.error(f"Error snapping window: {e}")
            return {'success': False, 'message': f"Error: {str(e)}"}
    
    def snap_right(self) -> Dict[str, any]:
        """Snap active window to right half of screen"""
        if not self.available:
            return {'success': False, 'message': "Window management requires pywin32"}
        
        try:
            import win32api
            
            # Get screen dimensions
            screen_width = win32api.GetSystemMetrics(0)
            screen_height = win32api.GetSystemMetrics(1)
            
            # Move to right half
            self.move_window(screen_width // 2, 0, screen_width // 2, screen_height)
            
            logger.info("Window snapped to right")
            return {'success': True, 'message': "Window snapped to right"}
            
        except Exception as e:
            logger.error(f"Error snapping window: {e}")
            return {'success': False, 'message': f"Error: {str(e)}"}
    
    def center_window(self) -> Dict[str, any]:
        """Center the active window on screen"""
        if not self.available:
            return {'success': False, 'message': "Window management requires pywin32"}
        
        try:
            import win32api
            
            hwnd = self.win32gui.GetForegroundWindow()
            rect = self.win32gui.GetWindowRect(hwnd)
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]
            
            # Get screen dimensions
            screen_width = win32api.GetSystemMetrics(0)
            screen_height = win32api.GetSystemMetrics(1)
            
            # Calculate center position
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
            
            self.move_window(x, y, width, height)
            
            logger.info("Window centered")
            return {'success': True, 'message': "Window centered"}
            
        except Exception as e:
            logger.error(f"Error centering window: {e}")
            return {'success': False, 'message': f"Error: {str(e)}"}
    
    def get_window_info(self) -> Dict[str, any]:
        """Get information about the active window"""
        if not self.available:
            return {'success': False, 'message': "Window management requires pywin32"}
        
        try:
            hwnd = self.win32gui.GetForegroundWindow()
            title = self.win32gui.GetWindowText(hwnd)
            rect = self.win32gui.GetWindowRect(hwnd)
            
            info = {
                'success': True,
                'title': title,
                'hwnd': hwnd,
                'position': {
                    'left': rect[0],
                    'top': rect[1],
                    'right': rect[2],
                    'bottom': rect[3],
                    'width': rect[2] - rect[0],
                    'height': rect[3] - rect[1]
                }
            }
            
            return info
            
        except Exception as e:
            logger.error(f"Error getting window info: {e}")
            return {'success': False, 'message': f"Error: {str(e)}"}


# Module exports
__all__ = ['WindowManager']
