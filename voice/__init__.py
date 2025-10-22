"""
Voice package for Jarvis V2
"""

from .speech_recognition import SpeechRecognizer
from .text_to_speech import TextToSpeech
from .wake_word import WakeWordDetector, SimpleWakeWordDetector

__all__ = [
    'SpeechRecognizer',
    'TextToSpeech',
    'WakeWordDetector',
    'SimpleWakeWordDetector'
]
