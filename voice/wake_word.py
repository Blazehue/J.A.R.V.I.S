"""
Wake Word Detection for Jarvis V2
Listens for wake word to activate voice commands
"""

import struct
import pyaudio
from threading import Thread, Event
from typing import Optional, Callable
from utils.logger import get_logger
from utils.config_manager import get_config

logger = get_logger()
config = get_config()


class WakeWordDetector:
    """Detects wake word to activate Jarvis"""
    
    def __init__(self, wake_word: Optional[str] = None):
        self.wake_word = wake_word or config.get('voice.wake_word', 'jarvis')
        self.is_listening = False
        self.stop_event = Event()
        self.listen_thread = None
        self.porcupine = None
        self.audio_stream = None
        self.pa = None
        
        # Try to initialize Porcupine
        self._init_porcupine()
    
    def _init_porcupine(self):
        """Initialize Porcupine wake word engine"""
        try:
            import pvporcupine
            
            # Initialize Porcupine with built-in wake word
            # Note: This requires a Picovoice access key
            access_key = config.get('advanced.api_keys.picovoice_key', '')
            
            if not access_key:
                logger.warning("Picovoice access key not found. Wake word detection disabled.")
                logger.info("Get a free key at: https://console.picovoice.ai/")
                return
            
            # Available built-in wake words: 'alexa', 'americano', 'blueberry', 
            # 'bumblebee', 'computer', 'grapefruit', 'grasshopper', 'hey google',
            # 'hey siri', 'jarvis', 'ok google', 'picovoice', 'porcupine', 'terminator'
            
            wake_words = ['jarvis'] if self.wake_word.lower() == 'jarvis' else ['computer']
            
            self.porcupine = pvporcupine.create(
                access_key=access_key,
                keywords=wake_words
            )
            
            logger.info(f"Wake word detector initialized for: {wake_words}")
            
        except ImportError:
            logger.warning("pvporcupine not installed. Wake word detection disabled.")
            logger.info("Install with: pip install pvporcupine")
        except Exception as e:
            logger.error(f"Error initializing wake word detector: {e}")
    
    def start(self, callback: Callable):
        """
        Start listening for wake word
        
        Args:
            callback: Function to call when wake word is detected
        """
        if self.is_listening:
            logger.warning("Wake word detector already running")
            return
        
        if not self.porcupine:
            logger.warning("Wake word detector not available")
            return
        
        self.is_listening = True
        self.stop_event.clear()
        self.listen_thread = Thread(target=self._listen_loop, args=(callback,))
        self.listen_thread.daemon = True
        self.listen_thread.start()
        
        logger.info(f"Wake word detection started. Listening for '{self.wake_word}'...")
    
    def stop(self):
        """Stop listening for wake word"""
        if not self.is_listening:
            return
        
        logger.info("Stopping wake word detection")
        self.is_listening = False
        self.stop_event.set()
        
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
        
        self._cleanup()
    
    def _listen_loop(self, callback: Callable):
        """Main listening loop"""
        try:
            self.pa = pyaudio.PyAudio()
            
            self.audio_stream = self.pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )
            
            logger.debug("Audio stream opened for wake word detection")
            
            while self.is_listening and not self.stop_event.is_set():
                try:
                    pcm = self.audio_stream.read(self.porcupine.frame_length, 
                                                exception_on_overflow=False)
                    pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                    
                    keyword_index = self.porcupine.process(pcm)
                    
                    if keyword_index >= 0:
                        logger.info(f"Wake word '{self.wake_word}' detected!")
                        if callback:
                            callback()
                    
                except Exception as e:
                    if self.is_listening:
                        logger.error(f"Error in wake word detection loop: {e}")
                    break
            
        except Exception as e:
            logger.error(f"Error setting up wake word detection: {e}")
        finally:
            self._cleanup()
    
    def _cleanup(self):
        """Clean up audio resources"""
        try:
            if self.audio_stream:
                self.audio_stream.close()
                self.audio_stream = None
            
            if self.pa:
                self.pa.terminate()
                self.pa = None
            
            logger.debug("Wake word detector cleaned up")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def __del__(self):
        """Destructor"""
        self.stop()
        if self.porcupine:
            self.porcupine.delete()


# Fallback simple wake word detector using speech recognition
class SimpleWakeWordDetector:
    """Simple wake word detection using speech recognition"""
    
    def __init__(self, wake_word: Optional[str] = None):
        self.wake_word = wake_word or config.get('voice.wake_word', 'jarvis')
        self.is_listening = False
        self.stop_event = Event()
        self.listen_thread = None
    
    def start(self, callback: Callable):
        """Start listening for wake word"""
        if self.is_listening:
            return
        
        from voice.speech_recognition import SpeechRecognizer
        
        self.is_listening = True
        self.stop_event.clear()
        
        recognizer = SpeechRecognizer()
        
        def listen_loop():
            logger.info(f"Simple wake word detection started for '{self.wake_word}'")
            
            while self.is_listening and not self.stop_event.is_set():
                result = recognizer.listen(timeout=2)
                
                if result['success']:
                    text = result['text'].lower()
                    if self.wake_word.lower() in text:
                        logger.info(f"Wake word '{self.wake_word}' detected!")
                        if callback:
                            callback()
        
        self.listen_thread = Thread(target=listen_loop)
        self.listen_thread.daemon = True
        self.listen_thread.start()
    
    def stop(self):
        """Stop listening"""
        self.is_listening = False
        self.stop_event.set()
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
        logger.info("Simple wake word detection stopped")
