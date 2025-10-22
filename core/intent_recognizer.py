"""
Intent Recognizer for Jarvis V2
Identifies user intent from natural language commands
"""

import re
from typing import Dict, List, Optional, Tuple
from utils.logger import get_logger

logger = get_logger()


class IntentRecognizer:
    """Recognizes user intent from commands"""
    
    def __init__(self):
        self.intent_patterns = self._build_patterns()
    
    def _build_patterns(self) -> Dict[str, List[Tuple[re.Pattern, Dict]]]:
        """Build regex patterns for intent recognition"""
        
        patterns = {
            # Application Control
            'launch_app': [
                (re.compile(r'\b(open|launch|start|run)\s+(.+)', re.I), {'target_group': 2}),
                (re.compile(r'\bi need\s+(.+)', re.I), {'target_group': 1}),
                (re.compile(r'\bshow me\s+(.+)', re.I), {'target_group': 1}),
            ],
            
            'close_app': [
                (re.compile(r'\b(close|quit|exit|kill|terminate|end)\s+(.+)', re.I), {'target_group': 2}),
                (re.compile(r'\bstop\s+(.+)', re.I), {'target_group': 1}),
            ],
            
            'switch_app': [
                (re.compile(r'\b(switch to|go to|focus|bring up)\s+(.+)', re.I), {'target_group': 2}),
            ],
            
            'list_apps': [
                (re.compile(r'\b(list|show|what).*?(running|open|active).*?(apps|applications|programs)', re.I), {}),
            ],
            
            # Screenshot Operations
            'screenshot': [
                (re.compile(r'\b(take|capture|grab|screenshot|screencap)\s+(a\s+)?(screenshot|screen|capture)', re.I), {}),
                (re.compile(r'\bscreenshot\b', re.I), {}),
            ],
            
            'screenshot_window': [
                (re.compile(r'\bscreenshot\s+(this|the|active)?\s*window', re.I), {}),
                (re.compile(r'\bcapture\s+(this|the|active)?\s*window', re.I), {}),
            ],
            
            'screenshot_region': [
                (re.compile(r'\bscreenshot\s+(this|an?)?\s*area', re.I), {}),
                (re.compile(r'\bcapture\s+region', re.I), {}),
            ],
            
            # System Control
            'volume': [
                (re.compile(r'\b(set|change|adjust)?\s*volume\s+(to\s+)?(\d+)\s*%?', re.I), {'value_group': 3}),
                (re.compile(r'\bvolume\s+(up|down)', re.I), {'direction_group': 1}),
            ],
            
            'mute': [
                (re.compile(r'\b(mute|unmute|silence)', re.I), {}),
            ],
            
            'brightness': [
                (re.compile(r'\b(set|change|adjust)?\s*brightness\s+(to\s+)?(\d+)\s*%?', re.I), {'value_group': 3}),
                (re.compile(r'\bbrightness\s+(up|down)', re.I), {'direction_group': 1}),
            ],
            
            'system_info': [
                (re.compile(r'\bhow.?s\s+(the\s+)?(system|computer|pc)', re.I), {}),
                (re.compile(r'\b(system|computer)\s+(status|info|information)', re.I), {}),
                (re.compile(r'\ball systems', re.I), {}),
            ],
            
            'lock_screen': [
                (re.compile(r'\block\s+(my\s+)?(computer|screen|workstation|pc)', re.I), {}),
            ],
            
            'shutdown': [
                (re.compile(r'\b(shutdown|shut down|power off|turn off)', re.I), {}),
            ],
            
            'restart': [
                (re.compile(r'\b(restart|reboot)', re.I), {}),
            ],
            
            'sleep': [
                (re.compile(r'\b(sleep|hibernate)', re.I), {}),
            ],
            
            # File Operations
            'open_file': [
                (re.compile(r'\bopen\s+(file|folder|directory)?\s*(.+)', re.I), {'target_group': 2}),
            ],
            
            'find_files': [
                (re.compile(r'\b(find|search|locate)\s+(all\s+)?(.+?)\s+(files?|in)', re.I), {'query_group': 3}),
                (re.compile(r'\bwhere\s+(is|are)\s+(.+)', re.I), {'query_group': 2}),
            ],
            
            'create_folder': [
                (re.compile(r'\bcreate\s+(a\s+)?(new\s+)?(folder|directory)\s+(.+)', re.I), {'name_group': 4}),
                (re.compile(r'\bnew\s+folder\s+(.+)', re.I), {'name_group': 1}),
            ],
            
            'delete_file': [
                (re.compile(r'\bdelete\s+(.+)', re.I), {'target_group': 1}),
                (re.compile(r'\bremove\s+(.+)', re.I), {'target_group': 1}),
            ],
            
            # Window Management
            'maximize': [
                (re.compile(r'\bmaximize', re.I), {}),
            ],
            
            'minimize': [
                (re.compile(r'\bminimize', re.I), {}),
            ],
            
            'split_screen': [
                (re.compile(r'\bsplit\s+screen', re.I), {}),
                (re.compile(r'\bside\s+by\s+side', re.I), {}),
            ],
            
            # Information Queries
            'time': [
                (re.compile(r'\b(what.?s\s+the\s+time|what time|current time)', re.I), {}),
            ],
            
            'date': [
                (re.compile(r'\b(what.?s\s+the\s+date|what date|today.?s date)', re.I), {}),
            ],
            
            'weather': [
                (re.compile(r'\b(what.?s\s+the\s+weather|weather|forecast)', re.I), {}),
            ],
            
            # General
            'greeting': [
                (re.compile(r'\b(hello|hi|hey|greetings)', re.I), {}),
            ],
            
            'status': [
                (re.compile(r'\b(status|are you (there|online|working))', re.I), {}),
            ],
            
            'help': [
                (re.compile(r'\b(help|what can you do|commands|capabilities)', re.I), {}),
            ],
            
            'thank': [
                (re.compile(r'\b(thank you|thanks|thx)', re.I), {}),
            ],
        }
        
        return patterns
    
    def recognize(self, command: str) -> Dict:
        """
        Recognize intent from command
        Returns dict with: intent, confidence, parameters
        """
        command = command.strip()
        
        if not command:
            return {
                'intent': 'unknown',
                'confidence': 0.0,
                'parameters': {},
                'raw_command': command
            }
        
        # Try to match against all patterns
        best_match = {
            'intent': 'unknown',
            'confidence': 0.0,
            'parameters': {},
            'raw_command': command
        }
        
        for intent, patterns in self.intent_patterns.items():
            for pattern, config in patterns:
                match = pattern.search(command)
                if match:
                    confidence = self._calculate_confidence(match, command)
                    
                    if confidence > best_match['confidence']:
                        parameters = self._extract_parameters(match, config, command)
                        best_match = {
                            'intent': intent,
                            'confidence': confidence,
                            'parameters': parameters,
                            'raw_command': command
                        }
        
        logger.debug(f"Intent recognized: {best_match['intent']} (confidence: {best_match['confidence']:.2f})")
        return best_match
    
    def _calculate_confidence(self, match: re.Match, command: str) -> float:
        """Calculate confidence score for a match"""
        # Base confidence on how much of the command was matched
        matched_length = len(match.group(0))
        command_length = len(command)
        
        if command_length == 0:
            return 0.0
        
        coverage = matched_length / command_length
        
        # Higher confidence if match is at the start
        if match.start() == 0:
            coverage *= 1.2
        
        # Cap at 1.0
        return min(coverage, 1.0)
    
    def _extract_parameters(self, match: re.Match, config: Dict, command: str) -> Dict:
        """Extract parameters from matched pattern"""
        parameters = {}
        
        # Extract target (app name, file, etc.)
        if 'target_group' in config:
            target = match.group(config['target_group']).strip()
            parameters['target'] = self._clean_target(target)
        
        # Extract value (for volume, brightness, etc.)
        if 'value_group' in config:
            try:
                value = int(match.group(config['value_group']))
                parameters['value'] = value
            except (ValueError, IndexError):
                pass
        
        # Extract direction (up/down)
        if 'direction_group' in config:
            direction = match.group(config['direction_group']).lower()
            parameters['direction'] = direction
        
        # Extract query string
        if 'query_group' in config:
            query = match.group(config['query_group']).strip()
            parameters['query'] = query
        
        # Extract name
        if 'name_group' in config:
            name = match.group(config['name_group']).strip()
            parameters['name'] = name
        
        return parameters
    
    def _clean_target(self, target: str) -> str:
        """Clean up target string"""
        # Remove articles
        target = re.sub(r'\b(a|an|the)\b', '', target, flags=re.I)
        
        # Remove trailing words like "application", "program"
        target = re.sub(r'\s+(application|program|app)$', '', target, flags=re.I)
        
        # Clean whitespace
        target = ' '.join(target.split())
        
        return target.strip()
    
    def get_possible_intents(self) -> List[str]:
        """Get list of all possible intents"""
        return list(self.intent_patterns.keys())
