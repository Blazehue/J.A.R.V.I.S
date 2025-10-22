"""
Helper utilities for Jarvis V2
Common functions used across the application
"""

import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple
import subprocess


def get_time_greeting() -> str:
    """Get appropriate greeting based on time of day"""
    hour = datetime.now().hour
    
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 22:
        return "Good evening"
    else:
        return "Good night"


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format"""
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} minutes"
    else:
        hours = seconds / 3600
        return f"{hours:.1f} hours"


def sanitize_filename(filename: str) -> str:
    """Remove invalid characters from filename"""
    # Remove invalid Windows filename characters
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', filename)
    
    # Remove leading/trailing spaces and periods
    sanitized = sanitized.strip('. ')
    
    return sanitized or 'unnamed'


def ensure_directory(path: str) -> Path:
    """Ensure directory exists, create if it doesn't"""
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def get_timestamp(format_str: str = "%Y%m%d_%H%M%S") -> str:
    """Get current timestamp as formatted string"""
    return datetime.now().strftime(format_str)


def find_executable(app_name: str) -> Optional[str]:
    """Find executable path for an application"""
    # Try common Windows locations
    common_paths = [
        f"C:\\Program Files\\{app_name}",
        f"C:\\Program Files (x86)\\{app_name}",
        os.path.expandvars(f"%LOCALAPPDATA%\\Programs\\{app_name}"),
        os.path.expandvars(f"%APPDATA%\\{app_name}"),
    ]
    
    # Check if it's in PATH
    try:
        result = subprocess.run(
            ['where', app_name],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip().split('\n')[0]
    except:
        pass
    
    # Search common paths
    for base_path in common_paths:
        if os.path.exists(base_path):
            # Look for .exe files
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    if file.lower().endswith('.exe') and app_name.lower() in file.lower():
                        return os.path.join(root, file)
    
    return None


def parse_natural_number(text: str) -> Optional[int]:
    """Parse natural language numbers (e.g., 'five' -> 5)"""
    number_words = {
        'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
        'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
        'ten': 10, 'twenty': 20, 'thirty': 30, 'forty': 40,
        'fifty': 50, 'sixty': 60, 'seventy': 70, 'eighty': 80,
        'ninety': 90, 'hundred': 100, 'thousand': 1000
    }
    
    text = text.lower().strip()
    
    # Try to parse as digit first
    try:
        return int(text)
    except ValueError:
        pass
    
    # Try to parse as word
    if text in number_words:
        return number_words[text]
    
    return None


def extract_percentage(text: str) -> Optional[int]:
    """Extract percentage value from text"""
    # Look for patterns like "50%", "50 percent", "fifty percent"
    patterns = [
        r'(\d+)\s*%',
        r'(\d+)\s*percent',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return int(match.group(1))
    
    # Try to parse word numbers
    words = text.lower().split()
    for word in words:
        num = parse_natural_number(word)
        if num is not None and 0 <= num <= 100:
            return num
    
    return None


def is_valid_path(path: str) -> bool:
    """Check if a path is valid"""
    try:
        Path(path)
        return True
    except (ValueError, OSError):
        return False


def get_desktop_path() -> Path:
    """Get user's desktop path"""
    return Path.home() / "Desktop"


def get_documents_path() -> Path:
    """Get user's documents path"""
    return Path.home() / "Documents"


def get_downloads_path() -> Path:
    """Get user's downloads path"""
    return Path.home() / "Downloads"


def throttle(func, min_interval: float = 1.0):
    """Decorator to throttle function calls"""
    last_called = [0.0]
    
    def wrapper(*args, **kwargs):
        now = time.time()
        if now - last_called[0] >= min_interval:
            last_called[0] = now
            return func(*args, **kwargs)
        return None
    
    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0):
    """Decorator to retry function on failure"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


def normalize_app_name(name: str) -> str:
    """Normalize application name for matching"""
    # Remove common suffixes
    name = re.sub(r'\.(exe|app)$', '', name.lower())
    
    # Remove version numbers
    name = re.sub(r'\s*\d+(\.\d+)*\s*', '', name)
    
    # Remove special characters
    name = re.sub(r'[^a-z0-9\s]', '', name)
    
    # Collapse whitespace
    name = ' '.join(name.split())
    
    return name.strip()


def similarity_score(str1: str, str2: str) -> float:
    """Calculate simple similarity score between two strings (0-1)"""
    str1 = str1.lower()
    str2 = str2.lower()
    
    if str1 == str2:
        return 1.0
    
    if str1 in str2 or str2 in str1:
        return 0.8
    
    # Simple character overlap
    set1 = set(str1)
    set2 = set(str2)
    overlap = len(set1.intersection(set2))
    total = len(set1.union(set2))
    
    return overlap / total if total > 0 else 0.0


def confirm_action(message: str) -> bool:
    """Request confirmation from user (for CLI)"""
    response = input(f"{message} (y/n): ").strip().lower()
    return response in ['y', 'yes']


class Timer:
    """Simple context manager for timing operations"""
    
    def __init__(self, name: str = "Operation"):
        self.name = name
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, *args):
        self.end_time = time.time()
    
    @property
    def elapsed(self) -> float:
        """Get elapsed time in seconds"""
        if self.end_time:
            return self.end_time - self.start_time
        return time.time() - self.start_time
    
    def __str__(self):
        return f"{self.name}: {self.elapsed:.2f}s"
