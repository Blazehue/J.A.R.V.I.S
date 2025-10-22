"""
Test script for Jarvis V2
Basic functionality tests
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import get_jarvis
from utils import get_logger

logger = get_logger()


def test_text_commands():
    """Test text command processing"""
    print("\n=== Testing Text Commands ===")
    
    jarvis = get_jarvis()
    jarvis.start()
    
    test_commands = [
        "hello",
        "what time is it",
        "list running apps",
        "help",
        "thank you"
    ]
    
    for command in test_commands:
        print(f"\nCommand: {command}")
        result = jarvis.process_command(command, speak_response=False)
        print(f"Success: {result['success']}")
        print(f"Response: {result['response']}")
    
    jarvis.stop()
    print("\n✓ Text commands test completed")


def test_system_info():
    """Test system information"""
    print("\n=== Testing System Info ===")
    
    jarvis = get_jarvis()
    jarvis.start()
    
    result = jarvis.process_command("how's the system doing?", speak_response=False)
    
    if result['success']:
        print("System info retrieved successfully")
        data = result.get('data', {})
        print(f"CPU: {data.get('cpu', {}).get('percent', 'N/A')}%")
        print(f"Memory: {data.get('memory', {}).get('percent', 'N/A')}%")
        print("✓ System info test passed")
    else:
        print("✗ System info test failed")
    
    jarvis.stop()


def test_app_manager():
    """Test application manager"""
    print("\n=== Testing Application Manager ===")
    
    from modules import ApplicationManager
    
    app_manager = ApplicationManager()
    
    # Test listing apps
    result = app_manager.list_running()
    if result['success']:
        print(f"✓ Found {result['count']} running applications")
    else:
        print("✗ Failed to list applications")
    
    # Test launch (notepad is always available on Windows)
    print("\nTesting app launch (notepad)...")
    result = app_manager.launch("notepad")
    print(f"Launch result: {result['success']} - {result['message']}")
    
    import time
    time.sleep(2)
    
    # Test close
    print("Testing app close (notepad)...")
    result = app_manager.close("notepad")
    print(f"Close result: {result['success']} - {result['message']}")


def test_microphone():
    """Test microphone"""
    print("\n=== Testing Microphone ===")
    
    jarvis = get_jarvis()
    
    if not jarvis.voice_enabled:
        print("Voice not enabled, skipping microphone test")
        return
    
    result = jarvis.test_microphone()
    
    if result['success']:
        print("✓ Microphone test passed")
    else:
        print(f"✗ Microphone test failed: {result['message']}")


def test_tts():
    """Test text-to-speech"""
    print("\n=== Testing Text-to-Speech ===")
    
    from voice import TextToSpeech
    
    tts = TextToSpeech()
    
    if tts.available:
        print("Testing TTS...")
        tts.speak("Testing text to speech. This is Jarvis.", wait=True)
        print("✓ TTS test completed")
    else:
        print("✗ TTS not available")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("  JARVIS V2 - System Tests")
    print("="*60)
    
    try:
        test_text_commands()
        test_system_info()
        test_app_manager()
        test_microphone()
        test_tts()
        
        print("\n" + "="*60)
        print("  All tests completed!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
