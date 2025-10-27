# JARVIS V2 - Technology Stack

## Overview
This document provides a comprehensive list of all technologies, libraries, frameworks, and tools used in the JARVIS V2 Desktop AI Assistant project.

---

## Core Technologies

### Programming Language
- **Python 3.8+** (Primary Language)
  - Version: 3.8 or higher required
  - Used for: Entire application development
  - Features: Type hints, async/await, modern syntax

---

## Speech & Audio Technologies

### Speech Recognition
- **SpeechRecognition 3.10.0+**
  - Purpose: Convert speech to text
  - Engines: Google Speech API, CMU Sphinx
  - Features: Multiple backend support, noise adaptation

- **PyAudio 0.2.14+**
  - Purpose: Audio stream handling
  - Features: Cross-platform audio I/O
  - Dependencies: PortAudio

### Text-to-Speech (TTS)
- **pyttsx3 2.90+**
  - Purpose: Convert text to speech
  - Engine: Native OS TTS engines
  - Features: Offline operation, customizable voice

### Wake Word Detection
- **pvporcupine 3.0.0+**
  - Purpose: Hot word detection ("Hey Jarvis")
  - Engine: Picovoice Porcupine
  - Features: Low latency, customizable keywords

---

## Desktop Automation & Control

### System Control
- **psutil 5.9.6+**
  - Purpose: System and process utilities
  - Features: CPU, memory, disk, network monitoring
  - OS: Cross-platform system information

- **pywin32 306+**
  - Purpose: Windows API access
  - Features: Native Windows operations
  - Modules: win32api, win32gui, win32con, win32com

### Desktop Automation
- **pyautogui 0.9.54+**
  - Purpose: GUI automation and screenshot capture
  - Features: Mouse/keyboard control, screen capture
  - Dependencies: PIL/Pillow, pymsgbox, pytweening

- **pygetwindow 0.0.9+**
  - Purpose: Window management
  - Features: Get/set window position, size, title
  - Platform: Windows-specific

- **pyrect 0.2.0**
  - Purpose: Rectangle geometry utilities
  - Used by: pygetwindow for window positioning

### Additional Automation Tools
- **pymsgbox 2.0.1**
  - Purpose: Cross-platform message boxes
  - Features: Alert, confirm, prompt dialogs

- **pytweening 1.2.0**
  - Purpose: Animation and easing functions
  - Used by: pyautogui for smooth movements

- **pyscreeze 1.0.1**
  - Purpose: Screenshot functionality
  - Features: Multi-monitor support

- **mouseinfo 0.1.3**
  - Purpose: Mouse position information
  - Used by: pyautogui for debugging

- **pyperclip 1.11.0**
  - Purpose: Clipboard operations
  - Features: Copy/paste text across platforms

---

## User Interface

### GUI Framework
- **customtkinter 5.2.2+**
  - Purpose: Modern UI components
  - Based on: Tkinter (standard library)
  - Features: Modern widgets, themes, scaling

- **darkdetect 0.8.0**
  - Purpose: System theme detection
  - Features: Detect dark/light mode
  - Used by: CustomTkinter for theme matching

### System Tray
- **pystray 0.19.5+**
  - Purpose: System tray icon and menu
  - Features: Background operation, quick access
  - Platform: Windows/macOS/Linux

---

## Image Processing

### Image Manipulation
- **Pillow 10.0.0+** (PIL Fork)
  - Purpose: Image processing and manipulation
  - Features: Screenshot processing, format conversion
  - Formats: PNG, JPEG, BMP, GIF, TIFF

---

## Natural Language Processing & AI

### NLP Libraries
- **OpenAI API 1.3.0+** (Optional)
  - Purpose: Advanced intent recognition
  - Features: GPT models, embeddings
  - Status: Optional dependency

### Numerical Computing
- **NumPy 1.26.0+**
  - Purpose: Numerical operations
  - Features: Array operations, mathematical functions
  - Used by: AI/ML operations, data processing

---

## File Operations & Monitoring

### File System Operations
- **pathlib** (Standard Library)
  - Purpose: Object-oriented filesystem paths
  - Features: Cross-platform path handling

- **watchdog 3.0.0+**
  - Purpose: File system event monitoring
  - Features: Watch directories for changes
  - Use cases: File detection, auto-reload

---

## Configuration & Environment

### Configuration Management
- **python-dotenv 1.0.0+**
  - Purpose: Load environment variables from .env files
  - Features: Configuration management, secrets

- **PyYAML 6.0.0+**
  - Purpose: YAML file parsing
  - Features: Config file support (alternative to JSON)
  - Format: YAML configuration files

### Standard Library (Built-in)
- **json**
  - Purpose: JSON configuration files
  - Features: Parse and write JSON

---

## HTTP & Network

### HTTP Client
- **requests 2.31.0+**
  - Purpose: HTTP requests
  - Features: REST API calls, web requests
  - Dependencies: urllib3, certifi, charset-normalizer, idna

### Supporting Libraries
- **urllib3 2.2.3+**
  - Purpose: HTTP client
  - Used by: requests library

- **certifi 2024.8.30+**
  - Purpose: SSL certificate bundle
  - Used by: requests for HTTPS

- **charset-normalizer 3.4.0+**
  - Purpose: Character encoding detection
  - Used by: requests library

- **idna 2.10+**
  - Purpose: Internationalized domain names
  - Used by: requests library

---

## Data Validation & Type Checking

### Data Validation
- **pydantic 2.9.2+**
  - Purpose: Data validation using Python type hints
  - Features: Settings management, data parsing
  - Dependencies: pydantic-core, annotated-types

- **pydantic-core 2.23.4+**
  - Purpose: Core validation logic for pydantic
  - Performance: Rust-based validation

- **annotated-types 0.7.0+**
  - Purpose: Type annotations for pydantic
  - Features: Extended type hints

### Type Extensions
- **typing-extensions 4.12.2+**
  - Purpose: Backported typing features
  - Features: Latest type hints for older Python versions

---

## Async & Concurrency

### Async Framework
- **anyio 4.6.2.post1+**
  - Purpose: Asynchronous I/O
  - Features: Async networking, file I/O
  - Used by: OpenAI SDK, httpx

### HTTP Client (Async)
- **httpx 0.27.2+**
  - Purpose: Async HTTP client
  - Features: HTTP/2, async requests
  - Used by: OpenAI API client

- **httpcore 1.0.7+**
  - Purpose: Low-level HTTP transport
  - Used by: httpx

- **h11 0.14.0+**
  - Purpose: HTTP/1.1 protocol implementation
  - Used by: httpcore

### Concurrency Utilities
- **sniffio 1.3.1+**
  - Purpose: Detect async library in use
  - Features: AsyncIO, Trio, Curio detection

---

## Testing Framework

### Testing Tools
- **pytest 7.4.0+** (or 8.4.2)
  - Purpose: Testing framework
  - Features: Test discovery, fixtures, parametrization
  - Platform: Cross-platform

- **pytest-cov 7.0.0+**
  - Purpose: Code coverage plugin for pytest
  - Features: Coverage reports, HTML output
  - Dependencies: coverage

- **coverage 7.10.6+** (or 7.11.0)
  - Purpose: Code coverage measurement
  - Features: Branch coverage, exclusions

### Test Utilities
- **pluggy 1.6.0+**
  - Purpose: Plugin system for pytest
  - Features: Hook management

- **iniconfig 2.1.0+**
  - Purpose: INI file parsing for pytest
  - Used by: pytest configuration

---

## Command Line Interface

### Terminal & Output
- **colorama 0.4.6+**
  - Purpose: Cross-platform colored terminal output
  - Features: ANSI color codes on Windows
  - Used by: Logger, CLI interface

---

## Progress & UI Utilities

### Progress Bars
- **tqdm 4.67.1+**
  - Purpose: Progress bars for loops and downloads
  - Features: Auto-updating progress indicators
  - Used by: OpenAI SDK, file operations

---

## Platform-Specific

### Windows Platform
- **comtypes 1.4.12+**
  - Purpose: COM interface access
  - Platform: Windows-only
  - Used by: pyttsx3, Windows automation

- **pypiwin32 223+**
  - Purpose: pywin32 installer helper
  - Platform: Windows-only

---

## AI & Machine Learning (Optional)

### AI SDKs
- **OpenAI SDK 1.55.2+**
  - Purpose: GPT-4, embeddings, completions
  - Features: Async support, streaming
  - Status: Optional dependency

### Supporting AI Libraries
- **distro 1.9.0+**
  - Purpose: Linux distribution detection
  - Used by: OpenAI SDK

- **jiter 0.8.0+**
  - Purpose: Fast JSON iteration
  - Used by: OpenAI SDK, pydantic

---

## Syntax & Code Quality

### Syntax Highlighting
- **pygments 2.18.0+**
  - Purpose: Syntax highlighting
  - Used by: pytest output, documentation

---

## Utility Libraries

### Standard Library (Python Built-in)
- **threading** - Multi-threading support
- **subprocess** - Process management
- **os** - Operating system interface
- **re** - Regular expressions
- **datetime** - Date and time operations
- **time** - Time-related functions
- **logging** - Logging facility
- **argparse** - Command-line argument parsing
- **pathlib** - Object-oriented filesystem paths
- **typing** - Type hints support
- **enum** - Enumeration support
- **dataclasses** - Data classes

---

## Development Tools

### Version Control
- **Git**
  - Purpose: Source code version control
  - Platform: All major platforms

### Virtual Environment
- **venv** (Standard Library)
  - Purpose: Isolated Python environments
  - Features: Dependency isolation

### Package Management
- **pip**
  - Purpose: Python package installer
  - Features: Install, upgrade, remove packages

---

## Build & Deployment

### Batch Scripts (Windows)
- **install.bat** - Automated installation script
- **run_jarvis.bat** - Quick launch script
- **run_cli.bat** - CLI mode launcher
- **test.bat** - Test runner script

### Configuration Files
- **requirements.txt** - Python dependencies list
- **config.json** - Runtime configuration
- **.gitignore** - Git exclusion rules

---

## Documentation

### Markdown
- **Markdown (.md files)**
  - Purpose: Project documentation
  - Files: README, ARCHITECTURE, QUICKSTART, etc.

### Document Generation
- **python-docx 1.2.0**
  - Purpose: Create Word documents
  - Used by: Report generation script

- **lxml 6.0.2**
  - Purpose: XML processing
  - Used by: python-docx

---

## Dependencies Summary

### Production Dependencies (20+ packages)
1. SpeechRecognition
2. pyttsx3
3. pyaudio
4. pvporcupine
5. pyautogui
6. pygetwindow
7. psutil
8. pywin32
9. pillow
10. customtkinter
11. pystray
12. watchdog
13. requests
14. python-dotenv
15. pyyaml
16. colorama
17. numpy
18. openai (optional)
19. pydantic
20. typing-extensions

### Development Dependencies (5+ packages)
1. pytest
2. pytest-cov
3. coverage
4. python-docx (for reports)
5. lxml

### Total Package Count
- **Direct Dependencies**: ~25 packages
- **Sub-dependencies**: ~50+ packages
- **Total Installed**: ~75+ packages

---

## Platform Requirements

### Operating System
- **Windows 10/11** (Primary Target)
  - 64-bit recommended
  - Administrator access for some features

### Python Version
- **Python 3.8+** (Minimum)
- **Python 3.12** (Tested & Recommended)

### Hardware Requirements
- **CPU**: Modern multi-core processor
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 500MB free space
- **Microphone**: Required for voice input
- **Speakers/Headphones**: Required for voice output

---

## External Services (Optional)

### Cloud Services
- **Google Speech Recognition API**
  - Purpose: Online speech-to-text
  - Requirement: Internet connection
  - Cost: Free tier available

- **OpenAI API** (Optional)
  - Purpose: Advanced NLP capabilities
  - Requirement: API key, internet
  - Cost: Paid service

---

## Architecture Patterns Used

### Design Patterns
1. **Singleton Pattern** - Global instances (Config, Logger)
2. **Command Pattern** - Command processing
3. **Strategy Pattern** - Multiple recognition engines
4. **Observer Pattern** - Event-driven callbacks
5. **Facade Pattern** - Unified interface (Jarvis Controller)
6. **Factory Pattern** - Module creation
7. **MVC Pattern** - UI separation

---

## License Information

### Open Source Licenses
- **MIT License** - JARVIS V2 Project
- Various open-source licenses for dependencies
  - Most are MIT, BSD, or Apache 2.0
  - Check individual package licenses for details

---

## Version Information

- **Project Version**: 2.0.0
- **Python**: 3.8+ (3.12 recommended)
- **Last Updated**: October 27, 2025

---

## Installation Commands

### Quick Install
```bash
pip install -r requirements.txt
```

### Individual Package Installation
```bash
# Speech & Audio
pip install SpeechRecognition pyttsx3 pyaudio pvporcupine

# Desktop Automation
pip install pyautogui pygetwindow psutil pywin32 pillow

# GUI
pip install customtkinter pystray

# File Operations
pip install watchdog

# HTTP & Config
pip install requests python-dotenv pyyaml

# Utilities
pip install colorama numpy

# Testing
pip install pytest pytest-cov

# Optional
pip install openai
```

---

## Troubleshooting

### Common Installation Issues

**PyAudio Installation**
- Windows: Download pre-built wheel from unofficial binaries
- Requires: Microsoft Visual C++ 14.0 or greater

**pywin32 Installation**
- May require manual post-install script
- Run: `python Scripts/pywin32_postinstall.py -install`

**pvporcupine Issues**
- Requires internet for initial model download
- Free tier has usage limits

---

## References & Documentation

### Official Documentation Links
- Python: https://docs.python.org/3/
- SpeechRecognition: https://pypi.org/project/SpeechRecognition/
- pyttsx3: https://pypi.org/project/pyttsx3/
- CustomTkinter: https://github.com/TomSchimansky/CustomTkinter
- PyAutoGUI: https://pyautogui.readthedocs.io/
- psutil: https://psutil.readthedocs.io/
- OpenAI: https://platform.openai.com/docs

---

**Document Version**: 1.0
**Last Updated**: October 27, 2025
**Project**: JARVIS V2 - Desktop AI Assistant
