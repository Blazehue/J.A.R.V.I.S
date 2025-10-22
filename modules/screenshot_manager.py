"""
Screenshot Manager for Jarvis V2
Handles taking and saving screenshots
"""

import pyautogui
from PIL import Image
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Tuple
from utils.logger import get_logger
from utils.config_manager import get_config
from utils.helpers import ensure_directory, sanitize_filename

logger = get_logger()
config = get_config()


class ScreenshotManager:
    """Manages screenshot operations"""
    
    def __init__(self):
        self.default_format = config.get('screenshots.default_format', 'png')
        self.default_path = config.get('screenshots.default_save_path', 
                                      str(Path.home() / 'Pictures' / 'Jarvis Screenshots'))
        self.auto_filename = config.get('screenshots.auto_filename', True)
        self.filename_pattern = config.get('screenshots.filename_pattern', 
                                          'screenshot_%Y_%m_%d_%H_%M_%S')
        self.quality = config.get('screenshots.quality', 95)
        
        # Ensure screenshot directory exists
        ensure_directory(self.default_path)
    
    def capture_full_screen(self, save_path: Optional[str] = None, 
                          filename: Optional[str] = None) -> Dict[str, any]:
        """
        Capture full screen screenshot
        Returns dict with success status and file path
        """
        try:
            logger.info("Capturing full screen screenshot")
            
            # Take screenshot
            screenshot = pyautogui.screenshot()
            
            # Generate filename and path
            filepath = self._get_save_path(save_path, filename)
            
            # Save screenshot
            screenshot.save(filepath, quality=self.quality)
            
            logger.info(f"Screenshot saved to: {filepath}")
            return {
                'success': True,
                'filepath': str(filepath),
                'message': f"Screenshot saved to {filepath.name}"
            }
            
        except Exception as e:
            logger.error(f"Error capturing screenshot: {e}")
            return {
                'success': False,
                'message': f"Screenshot failed: {str(e)}"
            }
    
    def capture_window(self, save_path: Optional[str] = None,
                      filename: Optional[str] = None) -> Dict[str, any]:
        """
        Capture active window screenshot
        """
        try:
            logger.info("Capturing active window screenshot")
            
            try:
                import win32gui
                import win32ui
                import win32con
                from ctypes import windll
                
                # Get active window
                hwnd = win32gui.GetForegroundWindow()
                
                # Get window dimensions
                left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                width = right - left
                height = bottom - top
                
                # Capture window
                hwndDC = win32gui.GetWindowDC(hwnd)
                mfcDC = win32ui.CreateDCFromHandle(hwndDC)
                saveDC = mfcDC.CreateCompatibleDC()
                
                saveBitMap = win32ui.CreateBitmap()
                saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
                saveDC.SelectObject(saveBitMap)
                
                # Copy window to bitmap
                result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)
                
                if result == 0:
                    # Fallback to full screen region capture
                    return self.capture_region(left, top, width, height, save_path, filename)
                
                # Convert to PIL Image
                bmpinfo = saveBitMap.GetInfo()
                bmpstr = saveBitMap.GetBitmapBits(True)
                screenshot = Image.frombuffer(
                    'RGB',
                    (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                    bmpstr, 'raw', 'BGRX', 0, 1
                )
                
                # Cleanup
                win32gui.DeleteObject(saveBitMap.GetHandle())
                saveDC.DeleteDC()
                mfcDC.DeleteDC()
                win32gui.ReleaseDC(hwnd, hwndDC)
                
            except ImportError:
                # Fallback: capture full screen and crop to active window
                logger.warning("pywin32 not available, using fallback method")
                try:
                    import pygetwindow as gw
                    active_window = gw.getActiveWindow()
                    if active_window:
                        return self.capture_region(
                            active_window.left,
                            active_window.top,
                            active_window.width,
                            active_window.height,
                            save_path,
                            filename
                        )
                except:
                    pass
                
                # Ultimate fallback
                return self.capture_full_screen(save_path, filename)
            
            # Generate filename and path
            filepath = self._get_save_path(save_path, filename)
            
            # Save screenshot
            screenshot.save(filepath, quality=self.quality)
            
            logger.info(f"Window screenshot saved to: {filepath}")
            return {
                'success': True,
                'filepath': str(filepath),
                'message': f"Window screenshot saved to {filepath.name}"
            }
            
        except Exception as e:
            logger.error(f"Error capturing window: {e}")
            return {
                'success': False,
                'message': f"Window capture failed: {str(e)}"
            }
    
    def capture_region(self, x: int, y: int, width: int, height: int,
                      save_path: Optional[str] = None,
                      filename: Optional[str] = None) -> Dict[str, any]:
        """
        Capture specific region of screen
        """
        try:
            logger.info(f"Capturing region: ({x}, {y}, {width}, {height})")
            
            # Ensure positive dimensions
            if width <= 0 or height <= 0:
                return {
                    'success': False,
                    'message': "Invalid region dimensions"
                }
            
            # Capture region
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            
            # Generate filename and path
            filepath = self._get_save_path(save_path, filename)
            
            # Save screenshot
            screenshot.save(filepath, quality=self.quality)
            
            logger.info(f"Region screenshot saved to: {filepath}")
            return {
                'success': True,
                'filepath': str(filepath),
                'message': f"Region screenshot saved to {filepath.name}"
            }
            
        except Exception as e:
            logger.error(f"Error capturing region: {e}")
            return {
                'success': False,
                'message': f"Region capture failed: {str(e)}"
            }
    
    def capture_with_delay(self, delay: int = 3, 
                          capture_type: str = 'full',
                          **kwargs) -> Dict[str, any]:
        """
        Capture screenshot after a delay
        """
        import time
        
        logger.info(f"Screenshot scheduled in {delay} seconds")
        time.sleep(delay)
        
        if capture_type == 'window':
            return self.capture_window(**kwargs)
        elif capture_type == 'region':
            return self.capture_region(**kwargs)
        else:
            return self.capture_full_screen(**kwargs)
    
    def _get_save_path(self, save_path: Optional[str] = None,
                      filename: Optional[str] = None) -> Path:
        """Generate save path for screenshot"""
        
        # Determine directory
        if save_path:
            directory = Path(save_path)
            if directory.is_file():
                # If a full path with filename was provided
                return directory
        else:
            directory = Path(self.default_path)
        
        # Ensure directory exists
        ensure_directory(directory)
        
        # Generate filename if not provided
        if not filename:
            if self.auto_filename:
                timestamp = datetime.now().strftime(self.filename_pattern)
                filename = f"{timestamp}.{self.default_format}"
            else:
                filename = f"screenshot.{self.default_format}"
        
        # Ensure proper extension
        if not filename.endswith(f'.{self.default_format}'):
            filename = f"{filename}.{self.default_format}"
        
        # Sanitize filename
        filename = sanitize_filename(filename)
        
        return directory / filename
    
    def get_screen_size(self) -> Tuple[int, int]:
        """Get screen dimensions"""
        return pyautogui.size()
