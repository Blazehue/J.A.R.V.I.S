"""
Configuration Manager for Jarvis V2
Handles loading, saving, and accessing configuration settings
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from utils.logger import get_logger

logger = get_logger()


class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self, config_path: str = "config/config.json"):
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from file"""
        try:
            if not self.config_path.exists():
                logger.warning(f"Config file not found at {self.config_path}")
                self._create_default_config()
                return
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            
            logger.info(f"Configuration loaded from {self.config_path}")
            
            # Expand environment variables in paths
            self._expand_paths()
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            self._create_default_config()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            self._create_default_config()
    
    def _create_default_config(self) -> None:
        """Create default configuration"""
        logger.info("Creating default configuration")
        
        # Copy from example if exists
        example_path = self.config_path.parent / "config.example.json"
        if example_path.exists():
            try:
                with open(example_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                self.save_config()
                logger.info("Default config created from example")
            except Exception as e:
                logger.error(f"Error copying example config: {e}")
                self._set_minimal_config()
        else:
            self._set_minimal_config()
    
    def _set_minimal_config(self) -> None:
        """Set minimal working configuration"""
        self.config = {
            "general": {
                "app_name": "Jarvis V2",
                "version": "2.0.0",
                "debug_mode": False,
                "log_level": "INFO"
            },
            "voice": {
                "enabled": True,
                "wake_word": "jarvis"
            },
            "personality": {
                "formality_level": "professional",
                "address_user_as": "sir"
            }
        }
        self.save_config()
    
    def save_config(self) -> bool:
        """Save current configuration to file"""
        try:
            # Ensure config directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
            
            logger.info(f"Configuration saved to {self.config_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving config: {e}")
            return False
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        Example: config.get('voice.wake_word')
        """
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any, save: bool = True) -> bool:
        """
        Set configuration value using dot notation
        Example: config.set('voice.wake_word', 'hey jarvis')
        """
        keys = key_path.split('.')
        config = self.config
        
        try:
            # Navigate to the parent dictionary
            for key in keys[:-1]:
                if key not in config:
                    config[key] = {}
                config = config[key]
            
            # Set the value
            config[keys[-1]] = value
            
            if save:
                return self.save_config()
            return True
            
        except Exception as e:
            logger.error(f"Error setting config value: {e}")
            return False
    
    def _expand_paths(self) -> None:
        """Expand environment variables in path configurations"""
        def expand_value(value):
            if isinstance(value, str):
                return os.path.expandvars(value)
            elif isinstance(value, dict):
                return {k: expand_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [expand_value(item) for item in value]
            return value
        
        # Expand paths in specific sections
        if 'screenshots' in self.config:
            if 'default_save_path' in self.config['screenshots']:
                self.config['screenshots']['default_save_path'] = os.path.expandvars(
                    self.config['screenshots']['default_save_path']
                )
        
        if 'files' in self.config:
            if 'search_locations' in self.config['files']:
                self.config['files']['search_locations'] = [
                    os.path.expandvars(path) 
                    for path in self.config['files']['search_locations']
                ]
    
    def reload(self) -> None:
        """Reload configuration from file"""
        logger.info("Reloading configuration")
        self.load_config()
    
    def get_all(self) -> Dict[str, Any]:
        """Get entire configuration dictionary"""
        return self.config.copy()
    
    def update_section(self, section: str, values: Dict[str, Any], save: bool = True) -> bool:
        """Update an entire configuration section"""
        try:
            if section not in self.config:
                self.config[section] = {}
            
            self.config[section].update(values)
            
            if save:
                return self.save_config()
            return True
            
        except Exception as e:
            logger.error(f"Error updating config section: {e}")
            return False


# Global config instance
_config = None


def get_config(config_path: str = "config/config.json") -> ConfigManager:
    """Get or create the global config instance"""
    global _config
    if _config is None:
        _config = ConfigManager(config_path)
    return _config
