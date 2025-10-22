# Quick Start Guide for Jarvis V2

## Installation

1. **Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Copy configuration:**
```bash
copy config\config.example.json config\config.json
```

4. **Edit config.json** to customize settings

## Running Jarvis

### GUI Mode (Default)
```bash
python main.py
```

### CLI Mode (Text-only)
```bash
python main.py --mode cli
```

### Voice Mode (Voice-only)
```bash
python main.py --mode voice
```

### Single Command
```bash
python main.py --command "open chrome"
```

## Example Commands

**Applications:**
- "Open Chrome"
- "Close Firefox"  
- "List running apps"

**Screenshots:**
- "Take a screenshot"
- "Screenshot this window"

**System:**
- "Set volume to 50"
- "How's the system doing?"
- "Lock screen"

**Files:**
- "Open Documents folder"
- "Find PDFs in Downloads"
- "Create folder Projects"

**Windows:**
- "Maximize"
- "Minimize"

## Troubleshooting

### Microphone not working
- Check Windows microphone permissions
- Run: `python main.py --debug`
- Test with: `python -m speech_recognition`

### Voice not speaking
- Check if pyttsx3 is installed
- Try different TTS voice in config.json

### Import errors
- Make sure all dependencies are installed
- Try: `pip install -r requirements.txt --upgrade`

## Configuration

Edit `config/config.json`:

- **voice.enabled**: Enable/disable voice features
- **voice.wake_word**: Change wake word ("jarvis", "computer", etc.)
- **personality.formality_level**: "professional", "casual", "technical"
- **screenshots.default_save_path**: Screenshot save location

## API Keys (Optional)

For advanced features, add to config.json:

- **OpenAI API**: Enhanced intent recognition
- **Picovoice**: Wake word detection (get free key at console.picovoice.ai)

## Support

- Check logs in `logs/` folder
- Run with `--debug` flag for detailed output
- Check README.md for full documentation
