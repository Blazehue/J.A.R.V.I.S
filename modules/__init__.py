"""
Modules package for Jarvis V2
Desktop control modules
"""

from .application_manager import ApplicationManager
from .screenshot_manager import ScreenshotManager
from .system_controller import SystemController
from .file_manager import FileManager
from .window_manager import WindowManager

__all__ = [
    'ApplicationManager',
    'ScreenshotManager',
    'SystemController',
    'FileManager',
    'WindowManager'
]
