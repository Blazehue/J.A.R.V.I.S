"""
Logger utility for Jarvis V2
Provides structured logging with color-coded console output and file logging
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from colorama import Fore, Style, init

# Initialize colorama for Windows
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color-coded output"""
    
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }
    
    def format(self, record):
        # Add color to level name
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{Style.RESET_ALL}"
        
        # Format the message
        result = super().format(record)
        
        # Reset levelname for file logging
        record.levelname = levelname
        return result


class JarvisLogger:
    """Centralized logging system for Jarvis"""
    
    def __init__(self, name="Jarvis", log_dir="logs", level=logging.INFO):
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Prevent duplicate handlers
        if self.logger.handlers:
            return
        
        # Console handler with colors
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_formatter = ColoredFormatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler - daily log files
        log_file = self.log_dir / f"jarvis_{datetime.now().strftime('%Y-%m-%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)  # Log everything to file
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
    
    def debug(self, message, **kwargs):
        """Log debug message"""
        self.logger.debug(message, **kwargs)
    
    def info(self, message, **kwargs):
        """Log info message"""
        self.logger.info(message, **kwargs)
    
    def warning(self, message, **kwargs):
        """Log warning message"""
        self.logger.warning(message, **kwargs)
    
    def error(self, message, **kwargs):
        """Log error message"""
        self.logger.error(message, **kwargs)
    
    def critical(self, message, **kwargs):
        """Log critical message"""
        self.logger.critical(message, **kwargs)
    
    def command(self, command, status="EXECUTED"):
        """Log command execution"""
        self.info(f"[COMMAND {status}] {command}")
    
    def response(self, response):
        """Log Jarvis response"""
        self.info(f"[JARVIS] {response}")
    
    def system(self, message):
        """Log system event"""
        self.info(f"[SYSTEM] {message}")


# Global logger instance
_logger = None


def get_logger(name="Jarvis", log_dir="logs", level=logging.INFO):
    """Get or create the global logger instance"""
    global _logger
    if _logger is None:
        _logger = JarvisLogger(name, log_dir, level)
    return _logger


# Convenience functions
def log_startup():
    """Log system startup"""
    logger = get_logger()
    logger.system("=" * 50)
    logger.system("JARVIS V2 INITIALIZING")
    logger.system(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.system("=" * 50)


def log_shutdown():
    """Log system shutdown"""
    logger = get_logger()
    logger.system("=" * 50)
    logger.system("JARVIS V2 SHUTTING DOWN")
    logger.system(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.system("=" * 50)
