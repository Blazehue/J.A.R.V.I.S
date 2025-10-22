"""
System Controller for Jarvis V2
Handles system-level operations (volume, power, system info, etc.)
"""

import os
import psutil
import subprocess
from typing import Dict, Optional
from utils.logger import get_logger
from utils.config_manager import get_config
from utils.helpers import format_file_size

logger = get_logger()
config = get_config()


class SystemController:
    """Controls system-level operations"""
    
    def __init__(self):
        pass
    
    def set_volume(self, level: int) -> Dict[str, any]:
        """
        Set system volume (0-100)
        """
        try:
            if not 0 <= level <= 100:
                return {
                    'success': False,
                    'message': "Volume must be between 0 and 100"
                }
            
            logger.info(f"Setting volume to {level}%")
            
            try:
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                from comtypes import CLSCTX_ALL
                
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(
                    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = interface.QueryInterface(IAudioEndpointVolume)
                
                # Set volume (0.0 to 1.0)
                volume.SetMasterVolumeLevelScalar(level / 100, None)
                
                return {
                    'success': True,
                    'message': f"Volume set to {level}%"
                }
                
            except ImportError:
                # Fallback using nircmd (if available)
                try:
                    # nircmd setsysvolume 65535 = 100%
                    volume_value = int((level / 100) * 65535)
                    subprocess.run(['nircmd', 'setsysvolume', str(volume_value)], 
                                 check=True, capture_output=True)
                    return {
                        'success': True,
                        'message': f"Volume set to {level}%"
                    }
                except:
                    return {
                        'success': False,
                        'message': "Volume control requires pycaw library or nircmd utility"
                    }
            
        except Exception as e:
            logger.error(f"Error setting volume: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}"
            }
    
    def adjust_volume(self, direction: str, step: int = 10) -> Dict[str, any]:
        """
        Adjust volume up or down
        """
        try:
            current_volume = self.get_volume()
            
            if direction.lower() == 'up':
                new_volume = min(100, current_volume + step)
            elif direction.lower() == 'down':
                new_volume = max(0, current_volume - step)
            else:
                return {
                    'success': False,
                    'message': "Direction must be 'up' or 'down'"
                }
            
            return self.set_volume(new_volume)
            
        except Exception as e:
            logger.error(f"Error adjusting volume: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}"
            }
    
    def mute(self) -> Dict[str, any]:
        """
        Mute/unmute system audio
        """
        try:
            logger.info("Toggling mute")
            
            try:
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                from comtypes import CLSCTX_ALL
                
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(
                    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = interface.QueryInterface(IAudioEndpointVolume)
                
                # Toggle mute
                current_mute = volume.GetMute()
                volume.SetMute(not current_mute, None)
                
                state = "muted" if not current_mute else "unmuted"
                return {
                    'success': True,
                    'message': f"System {state}"
                }
                
            except ImportError:
                # Fallback using nircmd
                try:
                    subprocess.run(['nircmd', 'mutesysvolume', '2'], 
                                 check=True, capture_output=True)
                    return {
                        'success': True,
                        'message': "Audio toggled"
                    }
                except:
                    return {
                        'success': False,
                        'message': "Mute control requires pycaw library or nircmd utility"
                    }
            
        except Exception as e:
            logger.error(f"Error toggling mute: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}"
            }
    
    def get_volume(self) -> int:
        """Get current system volume (0-100)"""
        try:
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            from comtypes import CLSCTX_ALL
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = interface.QueryInterface(IAudioEndpointVolume)
            
            return int(volume.GetMasterVolumeLevelScalar() * 100)
        except:
            return 50  # Default fallback
    
    def get_system_info(self) -> Dict[str, any]:
        """
        Get comprehensive system information
        """
        try:
            logger.info("Gathering system information")
            
            # CPU information
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Memory information
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used = format_file_size(memory.used)
            memory_total = format_file_size(memory.total)
            
            # Disk information
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_free = format_file_size(disk.free)
            disk_total = format_file_size(disk.total)
            
            # Battery information (if available)
            battery_info = None
            try:
                battery = psutil.sensors_battery()
                if battery:
                    battery_info = {
                        'percent': battery.percent,
                        'plugged_in': battery.power_plugged,
                        'time_left': battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None
                    }
            except:
                pass
            
            info = {
                'success': True,
                'cpu': {
                    'percent': cpu_percent,
                    'count': cpu_count
                },
                'memory': {
                    'percent': memory_percent,
                    'used': memory_used,
                    'total': memory_total
                },
                'disk': {
                    'percent': disk_percent,
                    'free': disk_free,
                    'total': disk_total
                },
                'battery': battery_info
            }
            
            logger.debug(f"System info: CPU {cpu_percent}%, RAM {memory_percent}%")
            return info
            
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}"
            }
    
    def lock_screen(self) -> Dict[str, any]:
        """
        Lock the workstation
        """
        try:
            logger.info("Locking workstation")
            
            # Windows lock
            subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'], 
                         check=True)
            
            return {
                'success': True,
                'message': "Workstation locked"
            }
            
        except Exception as e:
            logger.error(f"Error locking screen: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}"
            }
    
    def shutdown(self, force: bool = False) -> Dict[str, any]:
        """
        Shutdown the system
        """
        try:
            logger.warning("Initiating system shutdown")
            
            if force:
                subprocess.run(['shutdown', '/s', '/f', '/t', '0'], check=True)
            else:
                subprocess.run(['shutdown', '/s', '/t', '0'], check=True)
            
            return {
                'success': True,
                'message': "Shutdown initiated"
            }
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}"
            }
    
    def restart(self, force: bool = False) -> Dict[str, any]:
        """
        Restart the system
        """
        try:
            logger.warning("Initiating system restart")
            
            if force:
                subprocess.run(['shutdown', '/r', '/f', '/t', '0'], check=True)
            else:
                subprocess.run(['shutdown', '/r', '/t', '0'], check=True)
            
            return {
                'success': True,
                'message': "Restart initiated"
            }
            
        except Exception as e:
            logger.error(f"Error during restart: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}"
            }
    
    def sleep(self) -> Dict[str, any]:
        """
        Put system to sleep
        """
        try:
            logger.info("Putting system to sleep")
            
            subprocess.run(['rundll32.exe', 'powrprof.dll,SetSuspendState', '0,1,0'], 
                         check=True)
            
            return {
                'success': True,
                'message': "System going to sleep"
            }
            
        except Exception as e:
            logger.error(f"Error putting system to sleep: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}"
            }
