# Jarvis V2 - Desktop AI Assistant

An advanced desktop AI assistant inspired by Tony Stark's JARVIS, capable of controlling applications, managing files, taking screenshots, and providing intelligent assistance through voice and text interfaces.

## Features

### 🎯 Core Capabilities
- **Application Management**: Launch, close, and switch between applications
- **Screenshot Operations**: Capture full screen, windows, or specific regions
- **System Control**: Volume, brightness, power management
- **File Operations**: Search, open, create, and manage files
- **Window Management**: Resize, position, and organize windows
- **Voice Interface**: Natural language commands with text-to-speech responses
- **Intelligent Responses**: Context-aware, personality-driven interactions

### 🤖 Personality
- Sophisticated and intelligent communication
- Professional yet personable demeanor
- Occasionally witty and clever observations
- Proactive suggestions and optimizations

## Installation

### Prerequisites
- Python 3.8 or higher
- Windows 10/11 (primary support)
- Microphone (for voice commands)
- Speakers/Headphones (for voice responses)

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd JarivsV2
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure settings**
- Copy `config/config.example.json` to `config/config.json`
- Adjust settings as needed

5. **Run Jarvis**
```bash
python main.py
```

## Usage

### Voice Commands

**Application Control:**
- "Open Chrome"
- "Launch Visual Studio Code"
- "Close all browsers"
- "Switch to Discord"

**Screenshots:**
- "Take a screenshot"
- "Screenshot this window"
- "Capture screen and save to Desktop"

**System Control:**
- "Set volume to 50%"
- "Mute"
- "Lock screen"
- "How's the system doing?"

**File Operations:**
- "Open my Documents folder"
- "Find all PDFs in Downloads"
- "Create a new folder called Projects"

**Window Management:**
- "Maximize this window"
- "Split screen with Chrome and VSCode"
- "Move to second monitor"

### Text Commands

You can also interact with Jarvis through the GUI text interface using the same natural language commands.

## Project Structure

```
JarivsV2/
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── config/
│   ├── config.json        # User configuration
│   └── config.example.json # Example configuration
├── core/
│   ├── jarvis.py          # Main Jarvis controller
│   ├── command_processor.py # Command processing engine
│   ├── intent_recognizer.py # Intent recognition
│   └── validator.py       # Command validation
├── modules/
│   ├── application_manager.py  # App control
│   ├── screenshot_manager.py   # Screenshot operations
│   ├── system_controller.py    # System operations
│   ├── file_manager.py         # File operations
│   └── window_manager.py       # Window management
├── voice/
│   ├── speech_recognition.py   # Speech to text
│   ├── text_to_speech.py       # Text to speech
│   └── wake_word.py            # Wake word detection
├── personality/
│   ├── response_generator.py   # Response creation
│   └── templates.py            # Response templates
├── gui/
│   ├── main_window.py         # GUI interface
│   └── system_tray.py         # System tray icon
├── utils/
│   ├── logger.py              # Logging utilities
│   ├── config_manager.py      # Configuration management
│   └── helpers.py             # Helper functions
└── logs/                      # Application logs
```

## Configuration

Edit `config/config.json` to customize:

- **Voice Settings**: Recognition engine, TTS voice, wake word
- **Behavior**: Confirmation prompts, auto-save locations
- **Appearance**: GUI theme, system tray behavior
- **Shortcuts**: Custom keyboard shortcuts
- **Personality**: Response style, formality level

## Development

### Adding New Commands

1. Add intent pattern in `core/intent_recognizer.py`
2. Implement command handler in appropriate module
3. Add response templates in `personality/templates.py`
4. Update command processor in `core/command_processor.py`

### Testing

```bash
# Run tests
python -m pytest tests/

# Run with debug logging
python main.py --debug
```

## Troubleshooting

### Voice recognition not working
- Check microphone permissions in Windows settings
- Ensure microphone is set as default recording device
- Test with `python -m speech_recognition` in terminal

### Applications not launching
- Verify application is installed
- Check if application path is in system PATH
- Try running with administrator privileges

### High CPU usage
- Adjust voice recognition sensitivity in config
- Disable continuous listening mode
- Reduce screenshot quality settings

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes with clear commit messages
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Inspired by JARVIS from the Iron Man franchise
- Built with Python and love for automation
- Thanks to the open-source community for amazing libraries

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the documentation wiki
- Join our Discord community

---

**"Good morning, sir. Jarvis online and ready. All systems operational."**
