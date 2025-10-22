"""
Example: Custom command handler
"""

from core import get_jarvis, CommandProcessor

# Extend command processor with custom commands
class CustomCommandProcessor(CommandProcessor):
    """Custom command processor with additional commands"""
    
    def _execute_custom_greeting(self, params):
        """Custom greeting command"""
        return {
            'success': True,
            'response': "Hello! This is a custom command, sir.",
            'intent': 'custom_greeting'
        }
    
    def _execute_open_project(self, params):
        """Open specific project"""
        project_name = params.get('name', 'default')
        
        # Custom logic to open project
        # For example, open VSCode with specific folder
        
        return {
            'success': True,
            'response': f"Opening project {project_name}, sir.",
            'intent': 'open_project'
        }


# Use custom processor
jarvis = get_jarvis()
jarvis.command_processor = CustomCommandProcessor()

jarvis.start()

# Test custom commands
jarvis.process_command("custom greeting")
jarvis.process_command("open project MyApp")

jarvis.stop()
