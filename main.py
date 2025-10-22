"""
Jarvis V2 - Desktop AI Assistant
Main entry point
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils import get_logger, log_startup, log_shutdown, get_config
from core import get_jarvis

logger = get_logger()
config = get_config()


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Jarvis V2 - Desktop AI Assistant',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--mode',
        choices=['gui', 'voice', 'cli', 'daemon'],
        default='gui',
        help='Operating mode (default: gui)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    parser.add_argument(
        '--no-voice',
        action='store_true',
        help='Disable voice features'
    )
    
    parser.add_argument(
        '--command',
        type=str,
        help='Execute a single command and exit'
    )
    
    return parser.parse_args()


def run_cli_mode(jarvis):
    """Run in CLI mode with text input"""
    logger.info("Starting CLI mode")
    print("\n" + "="*60)
    print("  JARVIS V2 - Desktop AI Assistant")
    print("  Type 'exit' or 'quit' to stop")
    print("  Type 'help' for available commands")
    print("="*60 + "\n")
    
    jarvis.start()
    
    try:
        while True:
            try:
                command = input("\nYou: ").strip()
                
                if not command:
                    continue
                
                if command.lower() in ['exit', 'quit', 'stop']:
                    print("\nJarvis: Goodbye, sir.")
                    break
                
                result = jarvis.process_command(command, speak_response=False)
                print(f"\nJarvis: {result['response']}")
                
            except KeyboardInterrupt:
                print("\n\nJarvis: Shutting down, sir.")
                break
            except EOFError:
                break
    finally:
        jarvis.stop()


def run_voice_mode(jarvis):
    """Run in voice-only mode"""
    logger.info("Starting voice mode")
    print("\n" + "="*60)
    print("  JARVIS V2 - Voice Mode")
    print("  Press Ctrl+C to stop")
    print("  Listening for voice commands...")
    print("="*60 + "\n")
    
    jarvis.start()
    
    try:
        # If wake word is enabled, use that
        if jarvis.wake_word_detector:
            print(f"Say '{config.get('voice.wake_word', 'jarvis')}' to activate")
            jarvis.start_wake_word_detection()
        else:
            # Otherwise, continuous listening
            jarvis.start_listening()
        
        # Keep running
        import time
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\nStopping...")
    finally:
        jarvis.stop()


def run_gui_mode(jarvis):
    """Run with GUI"""
    logger.info("Starting GUI mode")
    
    try:
        from gui.main_window import JarvisGUI
        
        jarvis.start()
        
        # Create and run GUI
        gui = JarvisGUI(jarvis)
        gui.run()
        
    except ImportError as e:
        logger.error(f"GUI dependencies not available: {e}")
        print("\nGUI mode requires customtkinter. Install with:")
        print("  pip install customtkinter pystray")
        print("\nFalling back to CLI mode...")
        run_cli_mode(jarvis)
    except Exception as e:
        logger.error(f"Error in GUI mode: {e}")
        print(f"\nGUI error: {e}")
        print("Falling back to CLI mode...")
        run_cli_mode(jarvis)
    finally:
        jarvis.stop()


def run_daemon_mode(jarvis):
    """Run as background daemon (Windows service)"""
    logger.info("Starting daemon mode")
    print("Daemon mode - Running in background...")
    print("Press Ctrl+C to stop")
    
    jarvis.start()
    
    try:
        # Start wake word or continuous listening
        if jarvis.wake_word_detector:
            jarvis.start_wake_word_detection()
        else:
            jarvis.start_listening()
        
        # Keep running
        import time
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping daemon...")
    finally:
        jarvis.stop()


def execute_single_command(jarvis, command: str):
    """Execute a single command and exit"""
    logger.info(f"Executing single command: {command}")
    
    jarvis.start()
    result = jarvis.process_command(command, speak_response=False)
    
    print(f"\nCommand: {command}")
    print(f"Response: {result['response']}")
    print(f"Success: {result['success']}")
    
    jarvis.stop()
    
    return 0 if result['success'] else 1


def main():
    """Main entry point"""
    args = parse_arguments()
    
    # Set debug mode
    if args.debug:
        import logging
        logger.logger.setLevel(logging.DEBUG)
        config.set('general.debug_mode', True, save=False)
    
    # Disable voice if requested
    if args.no_voice:
        config.set('voice.enabled', False, save=False)
    
    # Get Jarvis instance
    jarvis = get_jarvis()
    
    try:
        # Single command mode
        if args.command:
            return execute_single_command(jarvis, args.command)
        
        # Interactive modes
        if args.mode == 'cli':
            run_cli_mode(jarvis)
        elif args.mode == 'voice':
            run_voice_mode(jarvis)
        elif args.mode == 'gui':
            run_gui_mode(jarvis)
        elif args.mode == 'daemon':
            run_daemon_mode(jarvis)
        
        return 0
        
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\nFatal error: {e}")
        return 1
    finally:
        log_shutdown()


if __name__ == "__main__":
    sys.exit(main())
