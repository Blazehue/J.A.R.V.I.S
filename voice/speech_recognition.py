"""
Speech Recognition for Jarvis V2
Converts speech to text using various engines
"""

import speech_recognition as sr
from typing import Optional, Dict
from utils.logger import get_logger
from utils.config_manager import get_config

logger = get_logger()
config = get_config()


class SpeechRecognizer:
    """Handles speech-to-text conversion"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Load configuration
        self.engine = config.get('voice.recognition_engine', 'google')
        self.timeout = config.get('voice.recognition_timeout', 5)
        self.phrase_limit = config.get('voice.phrase_time_limit', 10)
        self.energy_threshold = config.get('voice.energy_threshold', 4000)
        self.dynamic_energy = config.get('voice.dynamic_energy_threshold', True)
        
        # Configure recognizer
        self.recognizer.energy_threshold = self.energy_threshold
        self.recognizer.dynamic_energy_threshold = self.dynamic_energy
        
        # Calibrate for ambient noise
        self._calibrate()
    
    def _calibrate(self):
        """Calibrate for ambient noise"""
        try:
            logger.info("Calibrating microphone for ambient noise...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            logger.info(f"Calibration complete. Energy threshold: {self.recognizer.energy_threshold}")
        except Exception as e:
            logger.warning(f"Could not calibrate microphone: {e}")
    
    def listen(self, timeout: Optional[float] = None, 
              phrase_time_limit: Optional[float] = None) -> Dict[str, any]:
        """
        Listen for speech and convert to text
        Returns dict with success status and recognized text
        """
        try:
            timeout = timeout or self.timeout
            phrase_limit = phrase_time_limit or self.phrase_limit
            
            logger.debug("Listening for speech...")
            
            with self.microphone as source:
                try:
                    audio = self.recognizer.listen(
                        source,
                        timeout=timeout,
                        phrase_time_limit=phrase_limit
                    )
                except sr.WaitTimeoutError:
                    return {
                        'success': False,
                        'error': 'timeout',
                        'message': 'No speech detected'
                    }
            
            # Recognize speech
            logger.debug(f"Processing speech with {self.engine} engine...")
            text = self._recognize_audio(audio)
            
            if text:
                logger.info(f"Recognized: {text}")
                return {
                    'success': True,
                    'text': text
                }
            else:
                return {
                    'success': False,
                    'error': 'no_recognition',
                    'message': 'Could not understand audio'
                }
            
        except Exception as e:
            logger.error(f"Error during speech recognition: {e}")
            return {
                'success': False,
                'error': 'exception',
                'message': str(e)
            }
    
    def _recognize_audio(self, audio: sr.AudioData) -> Optional[str]:
        """Recognize audio using configured engine"""
        try:
            if self.engine == 'google':
                return self.recognizer.recognize_google(audio)
            elif self.engine == 'sphinx':
                return self.recognizer.recognize_sphinx(audio)
            elif self.engine == 'wit':
                # Requires API key
                api_key = config.get('advanced.api_keys.wit_key')
                if api_key:
                    return self.recognizer.recognize_wit(audio, key=api_key)
            elif self.engine == 'azure':
                # Requires API key
                api_key = config.get('advanced.api_keys.azure_key')
                if api_key:
                    return self.recognizer.recognize_azure(audio, key=api_key)
            
            # Default to Google
            return self.recognizer.recognize_google(audio)
            
        except sr.UnknownValueError:
            logger.debug("Speech recognition could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Recognition service error: {e}")
            return None
        except Exception as e:
            logger.error(f"Recognition error: {e}")
            return None
    
    def listen_continuous(self, callback, stop_event):
        """
        Continuously listen for speech and call callback with recognized text
        Runs until stop_event is set
        """
        logger.info("Starting continuous listening mode")
        
        with self.microphone as source:
            while not stop_event.is_set():
                try:
                    logger.debug("Listening...")
                    
                    audio = self.recognizer.listen(
                        source,
                        timeout=1,
                        phrase_time_limit=self.phrase_limit
                    )
                    
                    # Recognize in background to avoid blocking
                    text = self._recognize_audio(audio)
                    
                    if text and callback:
                        callback(text)
                    
                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    logger.error(f"Error in continuous listening: {e}")
                    continue
        
        logger.info("Stopped continuous listening")
    
    def test_microphone(self) -> Dict[str, any]:
        """Test if microphone is working"""
        try:
            logger.info("Testing microphone...")
            
            with self.microphone as source:
                logger.info("Microphone is accessible")
                
                # Try to record a brief sample
                audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=2)
                
                return {
                    'success': True,
                    'message': 'Microphone is working'
                }
                
        except sr.WaitTimeoutError:
            return {
                'success': True,
                'message': 'Microphone is working (no speech detected in test)'
            }
        except Exception as e:
            logger.error(f"Microphone test failed: {e}")
            return {
                'success': False,
                'message': f'Microphone test failed: {str(e)}'
            }
    
    def set_energy_threshold(self, threshold: int):
        """Set energy threshold for voice detection"""
        self.recognizer.energy_threshold = threshold
        self.energy_threshold = threshold
        logger.info(f"Energy threshold set to {threshold}")
    
    def recalibrate(self):
        """Recalibrate microphone for current ambient noise"""
        self._calibrate()
