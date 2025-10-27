"""
Command Processor for Jarvis V2
Processes commands and routes them to appropriate modules
"""

from typing import Dict, Any, Optional
from utils.logger import get_logger
from core.intent_recognizer import IntentRecognizer
from core.validator import Validator
from personality.response_generator import ResponseGenerator
from modules import (
    ApplicationManager,
    ScreenshotManager,
    SystemController,
    FileManager,
    WindowManager
)
from datetime import datetime

logger = get_logger()


class CommandProcessor:
    """Processes and executes commands"""
    
    def __init__(self):
        self.intent_recognizer = IntentRecognizer()
        self.validator = Validator()
        self.response_generator = ResponseGenerator()
        
        # Initialize modules
        self.app_manager = ApplicationManager()
        self.screenshot_manager = ScreenshotManager()
        self.system_controller = SystemController()
        self.file_manager = FileManager()
        self.window_manager = WindowManager()
        
        logger.info("Command processor initialized")
    
    def process(self, command: str) -> Dict[str, Any]:
        """
        Process a command and return response
        
        Returns dict with:
        - success: bool
        - response: str (message to user)
        - data: any (additional data)
        - requires_confirmation: bool
        """
        logger.command(command)
        
        # Recognize intent
        intent_result = self.intent_recognizer.recognize(command)
        intent = intent_result['intent']
        confidence = intent_result['confidence']
        parameters = intent_result['parameters']
        
        logger.debug(f"Intent: {intent}, Confidence: {confidence:.2f}, Params: {parameters}")
        
        # Handle unknown intent
        if intent == 'unknown' or confidence < 0.3:
            response = self.response_generator.generate('unknown')
            return {
                'success': False,
                'response': response,
                'intent': 'unknown'
            }
        
        # Validate command
        is_valid, error, warning = self.validator.validate(intent, parameters)
        
        if not is_valid:
            response = self.response_generator.generate('error', intent=intent, error=error)
            return {
                'success': False,
                'response': response,
                'intent': intent
            }
        
        # Check if confirmation is required
        if warning and self.validator.requires_confirmation(intent):
            return {
                'success': False,
                'requires_confirmation': True,
                'intent': intent,
                'parameters': parameters,
                'warning': warning,
                'response': self.response_generator.generate('confirmation', 
                                                            intent=intent, 
                                                            details=warning)
            }
        
        # Execute command
        return self._execute_command(intent, parameters)
    
    def _execute_command(self, intent: str, parameters: Dict) -> Dict[str, Any]:
        """Execute a command based on intent"""
        
        # Get execution method
        executor = getattr(self, f'_execute_{intent}', None)
        
        if not executor:
            # Try generic execution
            return self._execute_generic(intent, parameters)
        
        try:
            result = executor(parameters)
            return result
        except Exception as e:
            logger.error(f"Error executing command {intent}: {e}")
            response = self.response_generator.generate('error', 
                                                       intent=intent, 
                                                       error=str(e))
            return {
                'success': False,
                'response': response,
                'intent': intent
            }
    
    # Application Control
    def _execute_launch_app(self, params: Dict) -> Dict:
        target = params.get('target', '')
        result = self.app_manager.launch(target)
        
        if result['success']:
            response = self.response_generator.generate(
                'success',
                intent='launch_app',
                details=target
            )
        else:
            response = self.response_generator.generate(
                'error',
                intent='launch_app',
                error=result['message']
            )
        
        return {
            'success': result['success'],
            'response': response,
            'intent': 'launch_app'
        }
    
    def _execute_close_app(self, params: Dict) -> Dict:
        target = params.get('target', '')
        
        # Check for "all"
        if 'all' in target.lower():
            # Extract type (e.g., "all browsers")
            app_type = target.lower().replace('all', '').strip()
            if app_type:
                result = self.app_manager.close_all(app_type)
            else:
                result = {'success': False, 'message': 'Please specify what to close'}
        else:
            result = self.app_manager.close(target)
        
        if result['success']:
            response = self.response_generator.generate(
                'success',
                intent='close_app',
                details=result.get('message', target)
            )
        else:
            response = self.response_generator.generate(
                'error',
                intent='close_app',
                error=result.get('message', 'Failed to close application')
            )
        
        return {
            'success': result['success'],
            'response': response,
            'intent': 'close_app'
        }
    
    def _execute_switch_app(self, params: Dict) -> Dict:
        target = params.get('target', '')
        result = self.app_manager.switch_to(target)
        
        if result['success']:
            response = self.response_generator.generate(
                'success',
                intent='switch_app',
                details=result.get('message', '')
            )
        else:
            response = self.response_generator.generate(
                'error',
                intent='switch_app',
                error=result.get('message', 'Failed to switch application')
            )
        
        return {
            'success': result['success'],
            'response': response,
            'intent': 'switch_app'
        }
    
    def _execute_list_apps(self, params: Dict) -> Dict:
        result = self.app_manager.list_running()
        
        if result['success']:
            apps = result['apps'][:10]  # Top 10
            app_list = '\n'.join([f"- {app['name']} ({app['memory_mb']} MB)" 
                                 for app in apps])
            details = f"Running {result['count']} applications:\n{app_list}"
            response = self.response_generator.generate(
                'success',
                intent='list_apps',
                details=details
            )
        else:
            response = self.response_generator.generate(
                'error',
                intent='list_apps',
                error=result.get('message', 'Failed to list applications')
            )
        
        return {
            'success': result['success'],
            'response': response,
            'intent': 'list_apps',
            'data': result.get('apps', [])
        }
    
    # Screenshot Operations
    def _execute_screenshot(self, params: Dict) -> Dict:
        result = self.screenshot_manager.capture_full_screen()
        
        if result['success']:
            response = self.response_generator.generate(
                'success',
                intent='screenshot',
                details=result.get('message', '')
            )
        else:
            response = self.response_generator.generate(
                'error',
                intent='screenshot',
                error=result.get('message', 'Failed to capture screenshot')
            )
        
        return {
            'success': result['success'],
            'response': response,
            'intent': 'screenshot',
            'filepath': result.get('filepath')
        }
    
    def _execute_screenshot_window(self, params: Dict) -> Dict:
        result = self.screenshot_manager.capture_window()
        
        if result['success']:
            response = self.response_generator.generate(
                'success',
                intent='screenshot',
                details=result.get('message', '')
            )
        else:
            response = self.response_generator.generate(
                'error',
                intent='screenshot',
                error=result.get('message', 'Failed to capture window screenshot')
            )
        
        return {
            'success': result['success'],
            'response': response,
            'intent': 'screenshot_window',
            'filepath': result.get('filepath')
        }
    
    # System Control
    def _execute_volume(self, params: Dict) -> Dict:
        if 'value' in params:
            result = self.system_controller.set_volume(params['value'])
        elif 'direction' in params:
            result = self.system_controller.adjust_volume(params['direction'])
        else:
            result = {'success': False, 'message': 'No volume value or direction specified'}
        
        if result['success']:
            response = self.response_generator.generate(
                'success',
                intent='volume',
                details=result.get('message', '')
            )
        else:
            response = self.response_generator.generate(
                'error',
                intent='volume',
                error=result.get('message', 'Failed to adjust volume')
            )
        
        return {
            'success': result['success'],
            'response': response,
            'intent': 'volume'
        }
    
    def _execute_mute(self, params: Dict) -> Dict:
        result = self.system_controller.mute()
        
        if result['success']:
            response = self.response_generator.generate(
                'success',
                intent='mute',
                details=result.get('message', '')
            )
        else:
            response = self.response_generator.generate(
                'error',
                intent='mute',
                error=result.get('message', 'Failed to mute')
            )
        
        return {
            'success': result['success'],
            'response': response,
            'intent': 'mute'
        }
    
    def _execute_system_info(self, params: Dict) -> Dict:
        result = self.system_controller.get_system_info()
        
        if result['success']:
            cpu = result['cpu']
            memory = result['memory']
            disk = result['disk']
            battery = result.get('battery')
            
            details = f"All systems nominal, sir. "
            details += f"CPU at {cpu['percent']:.0f}%, "
            details += f"RAM usage {memory['percent']:.0f}%, "
            
            if battery:
                details += f"battery at {battery['percent']:.0f}%. "
            
            details += f"You have {disk['free']} of free storage remaining."
            
            response = self.response_generator.generate(
                'success',
                intent='system_info',
                details=details
            )
        else:
            response = self.response_generator.generate(
                'error',
                intent='system_info',
                error=result.get('message', 'Failed to get system info')
            )
        
        return {
            'success': result['success'],
            'response': response,
            'intent': 'system_info',
            'data': result if result['success'] else None
        }
    
    def _execute_lock_screen(self, params: Dict) -> Dict:
        result = self.system_controller.lock_screen()
        
        response = self.response_generator.generate(
            'success',
            intent='lock_screen'
        )
        
        return {
            'success': result['success'],
            'response': response,
            'intent': 'lock_screen'
        }
    
    def _execute_shutdown(self, params: Dict) -> Dict:
        result = self.system_controller.shutdown()
        
        return {
            'success': result['success'],
            'response': "Shutting down now, sir.",
            'intent': 'shutdown'
        }
    
    def _execute_restart(self, params: Dict) -> Dict:
        result = self.system_controller.restart()
        
        return {
            'success': result['success'],
            'response': "Restarting now, sir.",
            'intent': 'restart'
        }
    
    def _execute_sleep(self, params: Dict) -> Dict:
        result = self.system_controller.sleep()
        
        return {
            'success': result['success'],
            'response': "Putting system to sleep, sir.",
            'intent': 'sleep'
        }
    
    # File Operations
    def _execute_open_file(self, params: Dict) -> Dict:
        target = params.get('target', '')
        result = self.file_manager.open_file(target)
        
        if result['success']:
            response = self.response_generator.generate(
                'success',
                intent='open_file',
                details=result.get('message', '')
            )
        else:
            response = self.response_generator.generate(
                'error',
                intent='open_file',
                error=result.get('message', 'Failed to open file')
            )
        
        return {
            'success': result['success'],
            'response': response,
            'intent': 'open_file'
        }
    
    def _execute_find_files(self, params: Dict) -> Dict:
        query = params.get('query', '')
        result = self.file_manager.find_files(query)
        
        if result['success']:
            count = result['count']
            if count > 0:
                files = result['files'][:5]  # Show first 5
                file_list = '\n'.join([f"- {f['name']} ({f['size']})" 
                                      for f in files])
                details = f"I found {count} file(s):\n{file_list}"
                if result.get('truncated'):
                    details += "\n(Showing first 5 results)"
            else:
                details = f"I couldn't find any files matching '{query}'"
            
            response = self.response_generator.generate(
                'success',
                intent='find_files',
                details=details
            )
        else:
            response = self.response_generator.generate(
                'error',
                intent='find_files',
                error=result.get('message', 'Failed to search for files')
            )
        
        return {
            'success': result['success'],
            'response': response,
            'intent': 'find_files',
            'data': result.get('files', [])
        }
    
    def _execute_create_folder(self, params: Dict) -> Dict:
        name = params.get('name', '')
        result = self.file_manager.create_folder(name)
        
        if result['success']:
            response = self.response_generator.generate(
                'success',
                intent='create_folder',
                details=result.get('message', '')
            )
        else:
            response = self.response_generator.generate(
                'error',
                intent='create_folder',
                error=result.get('message', 'Failed to create folder')
            )
        
        return {
            'success': result['success'],
            'response': response,
            'intent': 'create_folder'
        }
    
    def _execute_delete_file(self, params: Dict) -> Dict:
        target = params.get('target', '')
        result = self.file_manager.delete_file(target)
        
        if result['success']:
            response = self.response_generator.generate(
                'success',
                intent='delete_file',
                details=result.get('message', '')
            )
        else:
            response = self.response_generator.generate(
                'error',
                intent='delete_file',
                error=result.get('message', 'Failed to delete file')
            )
        
        return {
            'success': result['success'],
            'response': response,
            'intent': 'delete_file'
        }
    
    # Window Management
    def _execute_maximize(self, params: Dict) -> Dict:
        result = self.window_manager.maximize_window()
        
        if result['success']:
            response = self.response_generator.generate(
                'success',
                intent='maximize',
                details=result.get('message', '')
            )
        else:
            response = self.response_generator.generate(
                'error',
                intent='maximize',
                error=result.get('message', 'Failed to maximize window')
            )
        
        return {
            'success': result['success'],
            'response': response,
            'intent': 'maximize'
        }
    
    def _execute_minimize(self, params: Dict) -> Dict:
        result = self.window_manager.minimize_window()
        
        if result['success']:
            response = self.response_generator.generate(
                'success',
                intent='minimize',
                details=result.get('message', '')
            )
        else:
            response = self.response_generator.generate(
                'error',
                intent='minimize',
                error=result.get('message', 'Failed to minimize window')
            )
        
        return {
            'success': result['success'],
            'response': response,
            'intent': 'minimize'
        }
    
    # Information Queries
    def _execute_time(self, params: Dict) -> Dict:
        current_time = datetime.now().strftime("%I:%M %p")
        response = f"It's {current_time}, sir."
        
        return {
            'success': True,
            'response': response,
            'intent': 'time'
        }
    
    def _execute_date(self, params: Dict) -> Dict:
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        response = f"Today is {current_date}, sir."
        
        return {
            'success': True,
            'response': response,
            'intent': 'date'
        }
    
    # General Responses
    def _execute_greeting(self, params: Dict) -> Dict:
        response = self.response_generator.generate('greeting')
        return {
            'success': True,
            'response': response,
            'intent': 'greeting'
        }
    
    def _execute_status(self, params: Dict) -> Dict:
        response = self.response_generator.generate('status')
        return {
            'success': True,
            'response': response,
            'intent': 'status'
        }
    
    def _execute_help(self, params: Dict) -> Dict:
        response = self.response_generator.generate('help')
        return {
            'success': True,
            'response': response,
            'intent': 'help'
        }
    
    def _execute_thank(self, params: Dict) -> Dict:
        response = self.response_generator.generate('thank')
        return {
            'success': True,
            'response': response,
            'intent': 'thank'
        }
    
    def _execute_generic(self, intent: str, parameters: Dict) -> Dict:
        """Generic execution for unhandled intents"""
        response = f"I understand you want to {intent.replace('_', ' ')}, but I haven't implemented that yet, sir."
        return {
            'success': False,
            'response': response,
            'intent': intent
        }
