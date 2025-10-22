"""
Response templates and personality framework for Jarvis V2
"""

from typing import Dict, Any, Optional
import random
from datetime import datetime
from utils.config_manager import get_config
from utils.helpers import get_time_greeting

config = get_config()


class ResponseTemplates:
    """Response templates for various situations"""
    
    def __init__(self):
        self.personality_config = config.get('personality', {})
        self.formality = self.personality_config.get('formality_level', 'professional')
        self.wit_enabled = self.personality_config.get('wit_enabled', True)
        self.address_as = self.personality_config.get('address_user_as', 'sir')
    
    def get_greeting(self) -> str:
        """Get greeting message"""
        time_greeting = get_time_greeting()
        greetings = [
            f"{time_greeting}, {self.address_as}. Jarvis online and ready.",
            f"{time_greeting}, {self.address_as}. All systems operational. How may I assist you today?",
            f"{time_greeting}, {self.address_as}. At your service.",
        ]
        return random.choice(greetings)
    
    def get_acknowledgment(self, intent: str) -> Optional[str]:
        """Get quick acknowledgment for command"""
        acknowledgments = {
            'launch_app': [
                "Opening now, {sir}.",
                "Launching {sir}.",
                "Right away, {sir}.",
            ],
            'close_app': [
                "Closing now, {sir}.",
                "Terminating application, {sir}.",
            ],
            'screenshot': [
                "Taking screenshot, {sir}.",
                "Capturing screen, {sir}.",
            ],
            'volume': [
                "Adjusting volume, {sir}.",
            ],
            'lock_screen': [
                "Locking workstation now, {sir}.",
            ],
            'shutdown': [
                "Initiating shutdown sequence, {sir}.",
            ],
            'restart': [
                "Initiating restart, {sir}.",
            ],
        }
        
        templates = acknowledgments.get(intent, [])
        if templates:
            template = random.choice(templates)
            return template.replace('{sir}', self.address_as)
        return None
    
    def format_success(self, intent: str, details: Optional[str] = None) -> str:
        """Format success message"""
        
        success_templates = {
            'launch_app': [
                "Application launched successfully{details}.",
                "{details} is now running, {sir}.",
            ],
            'close_app': [
                "Application closed{details}.",
                "{details} terminated, {sir}.",
            ],
            'screenshot': [
                "Screenshot captured{details}.",
                "Screen captured successfully{details}, {sir}.",
            ],
            'volume': [
                "Volume adjusted{details}.",
            ],
            'mute': [
                "System muted, {sir}.",
                "Audio muted.",
            ],
            'system_info': [
                "{details}",
            ],
            'create_folder': [
                "Folder created{details}.",
            ],
            'delete_file': [
                "Deleted{details}.",
            ],
            'lock_screen': [
                "Workstation locked. Have a good break, {sir}.",
            ],
            'find_files': [
                "{details}",
            ],
        }
        
        templates = success_templates.get(intent, ["Task completed{details}."])
        template = random.choice(templates)
        
        # Format details
        if details:
            details_str = f": {details}" if not details.startswith(':') else details
        else:
            details_str = ""
        
        message = template.replace('{details}', details_str)
        message = message.replace('{sir}', self.address_as)
        
        return message
    
    def format_error(self, intent: str, error: str) -> str:
        """Format error message"""
        
        polite_errors = {
            'launch_app': [
                "I couldn't locate that application, {sir}. {error}",
                "Unable to launch the application. {error}",
            ],
            'close_app': [
                "I couldn't close that application, {sir}. {error}",
            ],
            'screenshot': [
                "Screenshot failed, {sir}. {error}",
            ],
            'find_files': [
                "I couldn't find any files matching that criteria, {sir}. {error}",
            ],
            'delete_file': [
                "I couldn't delete that file, {sir}. {error}",
            ],
        }
        
        templates = polite_errors.get(intent, ["I encountered an issue, {sir}. {error}"])
        template = random.choice(templates)
        
        message = template.replace('{error}', error)
        message = message.replace('{sir}', self.address_as)
        
        return message
    
    def format_confirmation_request(self, intent: str, details: str) -> str:
        """Format confirmation request"""
        
        templates = {
            'shutdown': "Are you sure you want to shutdown? {details}",
            'restart': "Are you sure you want to restart? {details}",
            'delete_file': "Are you sure you want to delete {details}?",
            'close_app': "Close {details}? Any unsaved work may be lost.",
        }
        
        template = templates.get(intent, "Proceed with {details}?")
        return template.replace('{details}', details)
    
    def format_clarification_request(self, intent: str, context: Optional[str] = None) -> str:
        """Format request for clarification"""
        
        clarifications = {
            'screenshot': [
                "Full screen or specific window, {sir}?",
                "Would you like to capture the entire screen or just the active window?",
            ],
            'launch_app': [
                "Which application would you like me to open, {sir}?",
            ],
            'close_app': [
                "Which application should I close, {sir}?",
            ],
            'find_files': [
                "What type of files are you looking for, {sir}?",
            ],
        }
        
        templates = clarifications.get(intent, ["Could you provide more details, {sir}?"])
        template = random.choice(templates)
        
        message = template.replace('{sir}', self.address_as)
        
        if context:
            message += f" {context}"
        
        return message
    
    def format_suggestion(self, suggestions: list) -> str:
        """Format proactive suggestions"""
        if not suggestions:
            return ""
        
        if len(suggestions) == 1:
            return f"Suggestion: {suggestions[0]}"
        
        suggestion_str = "\n".join(f"- {s}" for s in suggestions)
        return f"Suggestions:\n{suggestion_str}"
    
    def get_witty_response(self, context: str) -> Optional[str]:
        """Get witty response based on context"""
        if not self.wit_enabled:
            return None
        
        witty_responses = {
            'open_everything': [
                "I appreciate your enthusiasm, {sir}, but opening all applications might test even my capabilities. Perhaps you could narrow that down?",
                "Opening everything simultaneously would be... ambitious. Could you be more specific, {sir}?",
            ],
            'close_everything': [
                "Closing all applications would be rather dramatic, {sir}. Are you sure?",
            ],
            'impossible_task': [
                "I'm afraid that's beyond my current capabilities, {sir}.",
                "Even I have my limits, {sir}. That's not something I can do.",
            ],
            'make_coffee': [
                "I'm afraid my skill set is limited to the digital realm, {sir}. However, I can guide you to the nearest coffee shop or help you set a reminder to brew some.",
            ],
        }
        
        for key, responses in witty_responses.items():
            if key in context.lower():
                response = random.choice(responses)
                return response.replace('{sir}', self.address_as)
        
        return None
    
    def get_status_response(self) -> str:
        """Get system status response"""
        responses = [
            f"All systems nominal, {self.address_as}. Ready to assist.",
            f"Online and operational, {self.address_as}.",
            f"Fully functional and at your service, {self.address_as}.",
        ]
        return random.choice(responses)
    
    def get_help_response(self) -> str:
        """Get help message"""
        return f"""I can assist you with various tasks, {self.address_as}:

**Application Control:**
- "Open Chrome" / "Close Firefox" / "Switch to VSCode"

**Screenshots:**
- "Take a screenshot" / "Screenshot this window"

**System Control:**
- "Volume to 50%" / "Mute" / "Lock screen"
- "How's the system doing?"

**File Operations:**
- "Open Documents folder" / "Find PDFs in Downloads"
- "Create folder Projects"

**Window Management:**
- "Maximize" / "Split screen"

Just speak naturally, and I'll understand what you need."""
    
    def get_thank_response(self) -> str:
        """Get response to thank you"""
        responses = [
            f"You're welcome, {self.address_as}.",
            f"Always a pleasure, {self.address_as}.",
            f"Happy to help, {self.address_as}.",
            f"At your service, {self.address_as}.",
        ]
        return random.choice(responses)
    
    def get_unknown_intent_response(self) -> str:
        """Get response for unknown intent"""
        responses = [
            f"I'm not sure I understand, {self.address_as}. Could you rephrase that?",
            f"I didn't quite catch that, {self.address_as}. Could you try again?",
            f"I'm afraid I don't understand that command, {self.address_as}.",
        ]
        return random.choice(responses)


class ResponseGenerator:
    """Generates natural language responses"""
    
    def __init__(self):
        self.templates = ResponseTemplates()
    
    def generate(self, response_type: str, **kwargs) -> str:
        """
        Generate a response based on type
        
        Types:
        - greeting
        - acknowledgment
        - success
        - error
        - confirmation
        - clarification
        - suggestion
        - status
        - help
        - thank
        - unknown
        """
        
        method = getattr(self, f'_generate_{response_type}', None)
        if method:
            return method(**kwargs)
        
        return self.templates.get_unknown_intent_response()
    
    def _generate_greeting(self, **kwargs) -> str:
        return self.templates.get_greeting()
    
    def _generate_acknowledgment(self, intent: str, **kwargs) -> str:
        return self.templates.get_acknowledgment(intent) or ""
    
    def _generate_success(self, intent: str, details: Optional[str] = None, **kwargs) -> str:
        return self.templates.format_success(intent, details)
    
    def _generate_error(self, intent: str, error: str, **kwargs) -> str:
        return self.templates.format_error(intent, error)
    
    def _generate_confirmation(self, intent: str, details: str, **kwargs) -> str:
        return self.templates.format_confirmation_request(intent, details)
    
    def _generate_clarification(self, intent: str, context: Optional[str] = None, **kwargs) -> str:
        return self.templates.format_clarification_request(intent, context)
    
    def _generate_suggestion(self, suggestions: list, **kwargs) -> str:
        return self.templates.format_suggestion(suggestions)
    
    def _generate_status(self, **kwargs) -> str:
        return self.templates.get_status_response()
    
    def _generate_help(self, **kwargs) -> str:
        return self.templates.get_help_response()
    
    def _generate_thank(self, **kwargs) -> str:
        return self.templates.get_thank_response()
    
    def _generate_unknown(self, **kwargs) -> str:
        return self.templates.get_unknown_intent_response()
