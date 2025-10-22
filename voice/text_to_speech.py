"""
Text-to-Speech for Jarvis V2
Converts text to spoken audio
"""

import pyttsx3
from typing import Optional
from utils.logger import get_logger
from utils.config_manager import get_config

logger = get_logger()
config = get_config()


class TextToSpeech:
    """Handles text-to-speech conversion"""
    
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            
            # Load configuration
            self.rate = config.get('voice.tts_rate', 175)
            self.volume = config.get('voice.tts_volume', 0.9)
            voice_name = config.get('voice.tts_voice', 'default')
            
            # Configure engine
            self.engine.setProperty('rate', self.rate)
            self.engine.setProperty('volume', self.volume)
            
            # Set voice
            if voice_name != 'default':
                self._set_voice(voice_name)
            
            self.available = True
            logger.info("Text-to-speech initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize text-to-speech: {e}")
            self.engine = None
            self.available = False
    
    def speak(self, text: str, wait: bool = True) -> bool:
        """
        Speak the given text
        
        Args:
            text: Text to speak
            wait: Whether to wait for speech to complete before returning
            
        Returns:
            True if successful, False otherwise
        """
        if not self.available or not self.engine:
            logger.warning("Text-to-speech not available")
            return False
        
        try:
            logger.debug(f"Speaking: {text}")
            
            self.engine.say(text)
            
            if wait:
                self.engine.runAndWait()
            
            return True
            
        except Exception as e:
            logger.error(f"Error during speech: {e}")
            return False
    
    def stop(self):
        """Stop current speech"""
        if self.available and self.engine:
            try:
                self.engine.stop()
                logger.debug("Speech stopped")
            except Exception as e:
                logger.error(f"Error stopping speech: {e}")
    
    def set_rate(self, rate: int):
        """
        Set speech rate
        
        Args:
            rate: Words per minute (typical range: 100-200)
        """
        if not self.available or not self.engine:
            return
        
        try:
            self.engine.setProperty('rate', rate)
            self.rate = rate
            logger.info(f"Speech rate set to {rate} WPM")
        except Exception as e:
            logger.error(f"Error setting rate: {e}")
    
    def set_volume(self, volume: float):
        """
        Set speech volume
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        if not self.available or not self.engine:
            return
        
        try:
            volume = max(0.0, min(1.0, volume))
            self.engine.setProperty('volume', volume)
            self.volume = volume
            logger.info(f"Speech volume set to {volume}")
        except Exception as e:
            logger.error(f"Error setting volume: {e}")
    
    def get_voices(self) -> list:
        """Get list of available voices"""
        if not self.available or not self.engine:
            return []
        
        try:
            voices = self.engine.getProperty('voices')
            return [{'id': v.id, 'name': v.name} for v in voices]
        except Exception as e:
            logger.error(f"Error getting voices: {e}")
            return []
    
    def set_voice(self, voice_id: str):
        """Set voice by ID"""
        if not self.available or not self.engine:
            return False
        
        return self._set_voice(voice_id)
    
    def _set_voice(self, voice_id: str) -> bool:
        """Internal method to set voice"""
        try:
            voices = self.engine.getProperty('voices')
            
            # Try to find voice by ID
            for voice in voices:
                if voice_id in voice.id or voice_id.lower() in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    logger.info(f"Voice set to: {voice.name}")
                    return True
            
            logger.warning(f"Voice not found: {voice_id}")
            return False
            
        except Exception as e:
            logger.error(f"Error setting voice: {e}")
            return False
    
    def save_to_file(self, text: str, filename: str) -> bool:
        """
        Save speech to audio file
        
        Args:
            text: Text to convert to speech
            filename: Output filename (should end in .mp3 or .wav)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.available or not self.engine:
            return False
        
        try:
            self.engine.save_to_file(text, filename)
            self.engine.runAndWait()
            logger.info(f"Speech saved to: {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving speech to file: {e}")
            return False
