"""
Main Jarvis Controller
Central control system for Jarvis V2
"""

from threading import Thread, Event
from typing import Optional, Callable
from utils.logger import get_logger, log_startup
from utils.config_manager import get_config
from utils.helpers import get_time_greeting
from core.command_processor import CommandProcessor
from voice import SpeechRecognizer, TextToSpeech, WakeWordDetector, SimpleWakeWordDetector
from personality.response_generator import ResponseGenerator

logger = get_logger()
config = get_config()


class Jarvis:
    """Main Jarvis AI Assistant Controller"""
    
    def __init__(self):
        log_startup()
        logger.info("Initializing Jarvis V2...")
        
        # Core components
        self.command_processor = CommandProcessor()
        self.response_generator = ResponseGenerator()
        
        # Voice components
        self.voice_enabled = config.get('voice.enabled', True)
        if self.voice_enabled:
            self.speech_recognizer = SpeechRecognizer()
            self.text_to_speech = TextToSpeech()
            
            # Wake word detection
            self.wake_word_enabled = config.get('voice.wake_word_enabled', False)
            if self.wake_word_enabled:
                try:
                    self.wake_word_detector = WakeWordDetector()
                except:
                    self.wake_word_detector = SimpleWakeWordDetector()
            else:
                self.wake_word_detector = None
        else:
            self.speech_recognizer = None
            self.text_to_speech = None
            self.wake_word_detector = None
        
        # State
        self.is_running = False
        self.listening_continuously = False
        self.stop_event = Event()
        
        # Callbacks
        self.on_command_callback: Optional[Callable] = None
        self.on_response_callback: Optional[Callable] = None
        
        logger.info("Jarvis V2 initialized successfully")
    
    def start(self):
        """Start Jarvis"""
        if self.is_running:
            logger.warning("Jarvis is already running")
            return
        
        self.is_running = True
        self.stop_event.clear()
        
        # Greet user
        greeting = self.response_generator.generate('greeting')
        self.speak(greeting)
        
        logger.info("Jarvis V2 started")
    
    def stop(self):
        """Stop Jarvis"""
        if not self.is_running:
            return
        
        logger.info("Stopping Jarvis...")
        
        self.is_running = False
        self.stop_event.set()
        
        if self.listening_continuously:
            self.stop_listening()
        
        if self.wake_word_detector:
            self.wake_word_detector.stop()
        
        logger.info("Jarvis stopped")
    
    def process_command(self, command: str, speak_response: bool = True) -> dict:
        """
        Process a text command
        
        Args:
            command: The command text
            speak_response: Whether to speak the response
            
        Returns:
            dict with processing result
        """
        if not self.is_running:
            return {
                'success': False,
                'response': 'Jarvis is not running'
            }
        
        # Trigger callback
        if self.on_command_callback:
            self.on_command_callback(command)
        
        # Process command
        result = self.command_processor.process(command)
        
        # Handle confirmation required
        if result.get('requires_confirmation'):
            logger.info("Command requires confirmation")
            return result
        
        # Speak response
        if speak_response and self.text_to_speech:
            self.speak(result['response'])
        
        # Trigger callback
        if self.on_response_callback:
            self.on_response_callback(result)
        
        logger.response(result['response'])
        
        return result
    
    def process_voice_command(self) -> dict:
        """
        Listen for and process a voice command
        
        Returns:
            dict with processing result
        """
        if not self.voice_enabled or not self.speech_recognizer:
            return {
                'success': False,
                'response': 'Voice commands are not enabled'
            }
        
        logger.info("Listening for voice command...")
        
        # Listen
        listen_result = self.speech_recognizer.listen()
        
        if not listen_result['success']:
            error = listen_result.get('error', 'unknown')
            if error == 'timeout':
                logger.debug("No speech detected")
                return listen_result
            else:
                logger.warning(f"Speech recognition error: {listen_result.get('message')}")
                return listen_result
        
        # Process command
        command = listen_result['text']
        return self.process_command(command, speak_response=True)
    
    def start_listening(self):
        """Start continuous voice listening"""
        if not self.voice_enabled:
            logger.warning("Voice is not enabled")
            return
        
        if self.listening_continuously:
            logger.warning("Already listening continuously")
            return
        
        self.listening_continuously = True
        
        def listening_loop():
            logger.info("Started continuous listening")
            
            while self.listening_continuously and not self.stop_event.is_set():
                try:
                    self.process_voice_command()
                except Exception as e:
                    logger.error(f"Error in listening loop: {e}")
            
            logger.info("Stopped continuous listening")
        
        listen_thread = Thread(target=listening_loop)
        listen_thread.daemon = True
        listen_thread.start()
    
    def stop_listening(self):
        """Stop continuous voice listening"""
        self.listening_continuously = False
        logger.info("Stopping continuous listening...")
    
    def start_wake_word_detection(self):
        """Start wake word detection"""
        if not self.wake_word_detector:
            logger.warning("Wake word detection not available")
            return
        
        def on_wake_word():
            logger.info("Wake word detected - processing command")
            self.speak("Yes, sir?")
            self.process_voice_command()
        
        self.wake_word_detector.start(on_wake_word)
    
    def speak(self, text: str, wait: bool = True):
        """Speak text using text-to-speech"""
        if self.text_to_speech and self.text_to_speech.available:
            self.text_to_speech.speak(text, wait)
        else:
            logger.debug(f"[JARVIS WOULD SAY]: {text}")
    
    def set_voice_rate(self, rate: int):
        """Set speech rate"""
        if self.text_to_speech:
            self.text_to_speech.set_rate(rate)
    
    def set_voice_volume(self, volume: float):
        """Set speech volume"""
        if self.text_to_speech:
            self.text_to_speech.set_volume(volume)
    
    def test_microphone(self) -> dict:
        """Test microphone"""
        if self.speech_recognizer:
            return self.speech_recognizer.test_microphone()
        return {
            'success': False,
            'message': 'Speech recognition not available'
        }
    
    def get_available_voices(self) -> list:
        """Get available TTS voices"""
        if self.text_to_speech:
            return self.text_to_speech.get_voices()
        return []
    
    def set_voice(self, voice_id: str) -> bool:
        """Set TTS voice"""
        if self.text_to_speech:
            return self.text_to_speech.set_voice(voice_id)
        return False
    
    def on_command(self, callback: Callable):
        """Register callback for when command is received"""
        self.on_command_callback = callback
    
    def on_response(self, callback: Callable):
        """Register callback for when response is generated"""
        self.on_response_callback = callback


# Global Jarvis instance
_jarvis_instance = None


def get_jarvis() -> Jarvis:
    """Get or create the global Jarvis instance"""
    global _jarvis_instance
    if _jarvis_instance is None:
        _jarvis_instance = Jarvis()
    return _jarvis_instance
