"""
Example usage of Jarvis V2 API
"""

from core import get_jarvis

# Get Jarvis instance
jarvis = get_jarvis()

# Start Jarvis
jarvis.start()

# Process text commands
result = jarvis.process_command("open chrome", speak_response=True)
print(f"Success: {result['success']}")
print(f"Response: {result['response']}")

# Process voice command
result = jarvis.process_voice_command()

# Get system info
result = jarvis.process_command("how's the system doing?")
print(result['data'])  # Access system info data

# Take screenshot
result = jarvis.process_command("take a screenshot")
print(f"Screenshot saved to: {result.get('filepath')}")

# Customize voice
jarvis.set_voice_rate(150)  # Slower speech
jarvis.set_voice_volume(0.8)  # Quieter

# Register callbacks
def on_command_received(command):
    print(f"User said: {command}")

def on_response_generated(result):
    print(f"Jarvis responded: {result['response']}")

jarvis.on_command(on_command_received)
jarvis.on_response(on_response_generated)

# Continuous listening
jarvis.start_listening()

# Keep running
try:
    import time
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    jarvis.stop()
