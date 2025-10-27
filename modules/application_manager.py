"""
Application Manager for Jarvis V2
Handles launching, closing, and managing applications
"""

import psutil
import subprocess
import time
from typing import List, Optional, Dict
from pathlib import Path
from utils.logger import get_logger
from utils.config_manager import get_config
from utils.helpers import find_executable, normalize_app_name, similarity_score

logger = get_logger()
config = get_config()


class ApplicationManager:
    """Manages desktop applications"""
    
    def __init__(self):
        self.common_apps = config.get('applications.common_apps', {})
    
    def launch(self, app_name: str) -> Dict[str, any]:
        """
        Launch an application
        Returns dict with success status and message
        """
        try:
            logger.info(f"Attempting to launch: {app_name}")
            
            # Check common apps first
            executable = self._resolve_app_name(app_name)
            
            if not executable:
                # Try to find it using Windows search
                executable = find_executable(app_name)
            
            # If still not found, try using Windows start command with app name
            if not executable:
                # Try launching directly with start command (works for UWP apps and installed apps)
                try:
                    # Normalize app name for Windows start command
                    normalized_name = normalize_app_name(app_name).lower()
                    
                    # Map common names to Windows protocol/package names
                    windows_apps = {
                        'camera': 'microsoft.windows.camera:',
                        'calculator': 'calculator:',
                        'calc': 'calculator:',
                        'settings': 'ms-settings:',
                        'store': 'ms-windows-store:',
                        'mail': 'outlookmail:',
                        'calendar': 'outlookcal:',
                        'photos': 'ms-photos:',
                        'maps': 'bingmaps:',
                        'weather': 'bingweather:',
                        'chrome': 'chrome',
                        'firefox': 'firefox',
                        'edge': 'msedge',
                        'notepad': 'notepad',
                        'wordpad': 'write',
                        'paint': 'mspaint',
                        'explorer': 'explorer',
                        'cmd': 'cmd',
                        'powershell': 'powershell',
                    }
                    
                    # Check if it's a known Windows app
                    if normalized_name in windows_apps:
                        app_to_launch = windows_apps[normalized_name]
                        subprocess.Popen(f'start {app_to_launch}', shell=True)
                        time.sleep(0.5)
                        logger.info(f"Successfully launched: {app_name}")
                        return {
                            'success': True,
                            'message': f"{app_name} launched successfully"
                        }
                    
                    # Try launching with 'start' command anyway
                    subprocess.Popen(f'start {app_name}', shell=True)
                    time.sleep(0.5)
                    logger.info(f"Successfully launched: {app_name}")
                    return {
                        'success': True,
                        'message': f"{app_name} launched successfully"
                    }
                    
                except Exception as launch_error:
                    logger.error(f"Failed to launch {app_name}: {launch_error}")
                    return {
                        'success': False,
                        'message': f"Could not locate '{app_name}'. Please check if it's installed."
                    }
            
            # Launch the application using the found executable
            if executable.endswith('.exe'):
                subprocess.Popen(executable, shell=True)
            else:
                subprocess.Popen(['start', executable], shell=True)
            
            time.sleep(0.5)  # Give it a moment to start
            
            logger.info(f"Successfully launched: {app_name}")
            return {
                'success': True,
                'message': f"{app_name} launched successfully"
            }
            
        except Exception as e:
            logger.error(f"Error launching {app_name}: {e}")
            return {
                'success': False,
                'message': f"Error launching application: {str(e)}"
            }
    
    def close(self, app_name: str) -> Dict[str, any]:
        """
        Close an application
        Returns dict with success status and message
        """
        try:
            logger.info(f"Attempting to close: {app_name}")
            
            # Find running processes matching the app name
            processes = self._find_processes(app_name)
            
            if not processes:
                return {
                    'success': False,
                    'message': f"'{app_name}' is not currently running"
                }
            
            # Terminate all matching processes
            terminated = []
            for proc in processes:
                try:
                    proc.terminate()
                    terminated.append(proc.name())
                    logger.debug(f"Terminated process: {proc.name()} (PID: {proc.pid})")
                except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                    logger.warning(f"Could not terminate {proc.name()}: {e}")
            
            if terminated:
                return {
                    'success': True,
                    'message': f"Closed {len(terminated)} instance(s) of {app_name}"
                }
            else:
                return {
                    'success': False,
                    'message': f"Could not close {app_name}"
                }
            
        except Exception as e:
            logger.error(f"Error closing {app_name}: {e}")
            return {
                'success': False,
                'message': f"Error closing application: {str(e)}"
            }
    
    def close_all(self, app_type: str) -> Dict[str, any]:
        """
        Close all applications of a certain type (e.g., "browsers")
        """
        try:
            browser_names = ['chrome', 'firefox', 'edge', 'opera', 'brave']
            
            if app_type.lower() in ['browser', 'browsers']:
                targets = browser_names
            else:
                return {
                    'success': False,
                    'message': f"Unknown application type: {app_type}"
                }
            
            closed = []
            for target in targets:
                result = self.close(target)
                if result['success']:
                    closed.append(target)
            
            if closed:
                return {
                    'success': True,
                    'message': f"Closed {len(closed)} {app_type}: {', '.join(closed)}"
                }
            else:
                return {
                    'success': False,
                    'message': f"No {app_type} were running"
                }
            
        except Exception as e:
            logger.error(f"Error closing all {app_type}: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}"
            }
    
    def list_running(self) -> Dict[str, any]:
        """
        Get list of running applications
        Returns dict with success status and list of apps
        """
        try:
            apps = []
            seen = set()
            
            for proc in psutil.process_iter(['name', 'pid', 'memory_info']):
                try:
                    proc_name = proc.info['name']
                    
                    # Filter out system processes
                    if not proc_name.endswith('.exe'):
                        continue
                    
                    # Remove .exe extension
                    app_name = proc_name[:-4]
                    
                    # Skip duplicates
                    if app_name.lower() in seen:
                        continue
                    
                    seen.add(app_name.lower())
                    
                    # Get memory usage
                    mem_mb = proc.info['memory_info'].rss / 1024 / 1024
                    
                    apps.append({
                        'name': app_name,
                        'pid': proc.info['pid'],
                        'memory_mb': round(mem_mb, 1)
                    })
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort by memory usage
            apps.sort(key=lambda x: x['memory_mb'], reverse=True)
            
            return {
                'success': True,
                'apps': apps,
                'count': len(apps)
            }
            
        except Exception as e:
            logger.error(f"Error listing running apps: {e}")
            return {
                'success': False,
                'apps': [],
                'message': f"Error: {str(e)}"
            }
    
    def switch_to(self, app_name: str) -> Dict[str, any]:
        """
        Switch focus to an application
        (This requires pywin32 and window management)
        """
        try:
            import win32gui
            import win32con
            
            # Find window with matching title
            target_normalized = normalize_app_name(app_name).lower()
            
            def callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    if title:
                        title_normalized = normalize_app_name(title).lower()
                        if target_normalized in title_normalized or \
                           similarity_score(target_normalized, title_normalized) > 0.6:
                            windows.append((hwnd, title))
                return True
            
            windows = []
            win32gui.EnumWindows(callback, windows)
            
            if not windows:
                return {
                    'success': False,
                    'message': f"Could not find window for '{app_name}'"
                }
            
            # Focus the first matching window
            hwnd, title = windows[0]
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            
            logger.info(f"Switched to: {title}")
            return {
                'success': True,
                'message': f"Switched to {title}"
            }
            
        except ImportError:
            return {
                'success': False,
                'message': "Window switching requires pywin32 library"
            }
        except Exception as e:
            logger.error(f"Error switching to {app_name}: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}"
            }
    
    def _resolve_app_name(self, app_name: str) -> Optional[str]:
        """Resolve app name to executable path"""
        # Normalize the name
        normalized = normalize_app_name(app_name)
        
        # Check common apps
        for key, exe in self.common_apps.items():
            if normalized.lower() == key.lower() or \
               normalized.lower() in key.lower() or \
               key.lower() in normalized.lower():
                return exe
        
        # Try direct name
        if app_name.endswith('.exe'):
            return app_name
        
        return None
    
    def _find_processes(self, app_name: str) -> List[psutil.Process]:
        """Find all processes matching an app name"""
        normalized_target = normalize_app_name(app_name)
        matching_processes = []
        
        for proc in psutil.process_iter(['name']):
            try:
                proc_name = proc.info['name']
                normalized_proc = normalize_app_name(proc_name)
                
                # Check for match
                if normalized_target.lower() in normalized_proc.lower() or \
                   similarity_score(normalized_target, normalized_proc) > 0.7:
                    matching_processes.append(proc)
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return matching_processes
    
    def is_running(self, app_name: str) -> bool:
        """Check if an application is currently running"""
        return len(self._find_processes(app_name)) > 0
