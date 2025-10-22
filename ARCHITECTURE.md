# Jarvis V2 - Project Architecture

## Overview
Jarvis V2 is a sophisticated desktop AI assistant inspired by Tony Stark's JARVIS. It provides natural language control over your Windows desktop through voice and text commands.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     Main Entry Point                     │
│                       (main.py)                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ├──────┬──────┬──────┬────────┐
                     │      │      │      │        │
          ┌──────────▼─┐  ┌─▼───┐ ┌▼───┐ ┌▼─────┐ │
          │   GUI Mode │  │ CLI │ │Voice│ │Daemon│ │
          └──────┬─────┘  └──┬──┘ └─┬──┘ └──┬───┘ │
                 │           │      │       │      │
                 └───────────┴──────┴───────┴──────┘
                             │
                    ┌────────▼─────────┐
                    │  Jarvis Core     │
                    │  (core/jarvis.py)│
                    └────────┬─────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
    ┌─────▼──────┐  ┌───────▼────────┐  ┌─────▼──────┐
    │  Voice     │  │    Command      │  │ Personality│
    │ Interface  │  │   Processor     │  │  System    │
    └────────────┘  └────────┬────────┘  └────────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
    ┌─────▼─────┐   ┌───────▼────────┐  ┌─────▼──────┐
    │  Intent   │   │   Validator    │  │  Modules   │
    │Recognizer │   │                │  │  (Desktop  │
    └───────────┘   └────────────────┘  │  Control)  │
                                        └─────┬──────┘
                                              │
              ┌───────────┬──────────┬────────┼────────┬───────────┐
              │           │          │        │        │           │
        ┌─────▼────┐ ┌───▼───┐ ┌───▼────┐ ┌─▼────┐ ┌─▼─────┐ ┌───▼────┐
        │   App    │ │Screen │ │ System │ │ File │ │Window │ │ Utils  │
        │ Manager  │ │ shot  │ │Control │ │  Mgr │ │  Mgr  │ │        │
        └──────────┘ └───────┘ └────────┘ └──────┘ └───────┘ └────────┘
```

## Component Structure

### 1. Core System (`core/`)
**Purpose**: Central control and command processing

- `jarvis.py` - Main controller, manages all components
- `command_processor.py` - Processes commands and routes to modules
- `intent_recognizer.py` - Natural language understanding
- `validator.py` - Command validation and safety checks

### 2. Desktop Control Modules (`modules/`)
**Purpose**: Execute desktop operations

- `application_manager.py` - Launch/close/manage applications
- `screenshot_manager.py` - Capture screenshots
- `system_controller.py` - Volume, power, system info
- `file_manager.py` - File operations
- `window_manager.py` - Window positioning

### 3. Voice Interface (`voice/`)
**Purpose**: Voice input/output

- `speech_recognition.py` - Speech-to-text
- `text_to_speech.py` - Text-to-speech
- `wake_word.py` - Wake word detection

### 4. Personality System (`personality/`)
**Purpose**: Natural language generation

- `response_generator.py` - Generates human-like responses
- Context-aware, personality-driven communication

### 5. User Interface (`gui/`)
**Purpose**: Graphical interface

- `main_window.py` - GUI using CustomTkinter
- Chat-like interface
- Real-time command/response display

### 6. Utilities (`utils/`)
**Purpose**: Common functionality

- `logger.py` - Logging system
- `config_manager.py` - Configuration management
- `helpers.py` - Helper functions

## Data Flow

### Text Command Flow
```
User Input → Command Processor → Intent Recognizer → Validator
                                                          ↓
Response ← Personality System ← Module Execution ← Valid?
```

### Voice Command Flow
```
Microphone → Speech Recognition → Text Command Flow → Text-to-Speech
```

### Wake Word Flow
```
Continuous Listening → Wake Word Detected → Listen for Command → Process
```

## Key Design Patterns

### 1. Singleton Pattern
- Global `Jarvis` instance
- Global `Config` instance
- Global `Logger` instance

### 2. Command Pattern
- Commands encapsulated as intents
- Validators check before execution
- Modules execute commands

### 3. Strategy Pattern
- Multiple recognition engines (Google, Sphinx)
- Multiple operation modes (GUI, CLI, Voice)
- Configurable response styles

### 4. Observer Pattern
- Callbacks for commands and responses
- Event-driven architecture

## Configuration System

### Hierarchy
```
config.example.json (template)
    ↓
config.json (user config)
    ↓
Runtime config (in-memory)
```

### Configuration Sections
- `general`: App settings
- `voice`: Voice recognition/TTS
- `personality`: Response style
- `applications`: App shortcuts
- `screenshots`: Screenshot settings
- `system`: System operation settings
- `files`: File operation settings
- `security`: Safety controls
- `gui`: Interface settings

## Security Features

### Safety Controls
1. **Validation**: All commands validated before execution
2. **Confirmation**: Dangerous operations require confirmation
3. **Restricted Operations**: System changes can be disabled
4. **Path Protection**: System paths cannot be deleted
5. **Error Handling**: Graceful failure, never crashes

### Configurable Restrictions
- File deletion (can be disabled)
- System changes (can be disabled)
- Registry access (disabled by default)
- Admin commands (require confirmation)

## Extension Points

### Adding New Commands

1. **Add Intent Pattern** (`core/intent_recognizer.py`)
```python
'new_command': [
    (re.compile(r'\bmy pattern\b', re.I), {}),
]
```

2. **Add Validator** (`core/validator.py`)
```python
def _validate_new_command(self, params):
    # Validation logic
    return True, None, None
```

3. **Add Executor** (`core/command_processor.py`)
```python
def _execute_new_command(self, params):
    # Execution logic
    return {'success': True, 'response': 'Done'}
```

4. **Add Response Template** (`personality/response_generator.py`)
```python
'new_command': ["Command executed, {sir}."]
```

### Adding New Modules

1. Create module in `modules/`
2. Implement required methods
3. Import in `modules/__init__.py`
4. Add to `CommandProcessor`

## Performance Considerations

### Optimization Strategies
1. **Lazy Loading**: Modules loaded on demand
2. **Caching**: Recognition results cached
3. **Background Processing**: Voice recognition in threads
4. **Resource Management**: Cleanup after operations

### Resource Usage
- **Memory**: ~50-100MB (base)
- **CPU**: <5% (idle), 10-30% (active recognition)
- **Disk**: Minimal (logs only)

## Error Handling

### Levels
1. **Validation Errors**: Caught before execution
2. **Execution Errors**: Graceful failure, user notification
3. **System Errors**: Logged, fallback behavior
4. **Fatal Errors**: Clean shutdown

### Logging
- Console: Color-coded, user-friendly
- File: Detailed, rotating daily
- Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

## Testing Strategy

### Test Levels
1. **Unit Tests**: Individual components
2. **Integration Tests**: Component interactions
3. **System Tests**: End-to-end workflows
4. **Manual Tests**: User scenarios

### Test Script (`test_jarvis.py`)
- Text commands
- System info
- Application management
- Voice interface
- Microphone/TTS

## Deployment

### Requirements
- Windows 10/11
- Python 3.8+
- Microphone (for voice)
- ~500MB disk space

### Installation
```bash
# Automatic
install.bat

# Manual
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Running
```bash
# GUI
python main.py

# CLI
python main.py --mode cli

# Voice
python main.py --mode voice

# Single command
python main.py --command "open chrome"
```

## Future Architecture Considerations

### Planned Enhancements
1. **Plugin System**: Dynamic module loading
2. **Web API**: REST API for remote control
3. **Mobile App**: Companion app
4. **Cloud Sync**: Settings and preferences
5. **Multi-platform**: macOS, Linux support
6. **AI Integration**: GPT-4, Claude integration
7. **Automation**: Workflow creation
8. **Analytics**: Usage tracking

### Scalability
- Modular design allows easy additions
- Configuration-driven behavior
- Extensible command system
- Pluggable voice engines

## Troubleshooting Guide

### Common Issues

**Voice not working**
- Check microphone permissions
- Test with: `python -m speech_recognition`
- Verify in config.json

**Commands not recognized**
- Check intent patterns
- Enable debug mode
- Review logs

**Import errors**
- Reinstall dependencies
- Check Python version
- Verify virtual environment

**Performance issues**
- Disable continuous listening
- Reduce screenshot quality
- Check system resources

## Credits and Attribution

### Technologies Used
- **Speech Recognition**: Google Speech API, CMU Sphinx
- **TTS**: pyttsx3
- **GUI**: CustomTkinter
- **Desktop Control**: psutil, pywin32, pyautogui
- **Wake Word**: Picovoice Porcupine

### Inspiration
- Iron Man's JARVIS
- Modern AI assistants
- Desktop automation tools

---

**Version**: 2.0.0
**Last Updated**: October 22, 2025
**License**: MIT
