#!/usr/bin/env python3
"""
Settings Manager
Manages user preferences and application settings
"""

import json
from pathlib import Path
from typing import Optional
from .resource_manager import ResourceManager


class SettingsManager:
    """Manages application settings and user preferences"""

    def __init__(self):
        """Initialize the settings manager"""
        self.resource_manager = ResourceManager()
        self.settings_file = self.resource_manager.user_data_dir.parent / "settings.json"
        self.settings = self._load_settings()

    def _load_settings(self) -> dict:
        """Load settings from file"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load settings: {e}")
                return self._get_default_settings()
        else:
            return self._get_default_settings()

    def _get_default_settings(self) -> dict:
        """Get default settings"""
        return {
            "default_export_folder": str(Path.home() / "Documents"),
            "version": "1.0.0"
        }

    def _save_settings(self) -> bool:
        """Save settings to file"""
        try:
            # Ensure parent directory exists
            self.settings_file.parent.mkdir(parents=True, exist_ok=True)

            # Write settings
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving settings: {e}")
            return False

    def get_default_export_folder(self) -> str:
        """Get the default export folder path"""
        return self.settings.get("default_export_folder", str(Path.home() / "Documents"))

    def set_default_export_folder(self, folder_path: str) -> bool:
        """
        Set the default export folder path

        Args:
            folder_path: Path to the default export folder

        Returns:
            True if successful, False otherwise
        """
        # Validate that the path exists
        path = Path(folder_path)
        if not path.exists():
            return False

        if not path.is_dir():
            return False

        # Update and save
        self.settings["default_export_folder"] = str(path)
        return self._save_settings()

    def get_data_location(self) -> str:
        """Get the current data location (read-only for now)"""
        return str(self.resource_manager.user_data_dir.parent)

    def reset_to_defaults(self) -> bool:
        """Reset all settings to defaults"""
        self.settings = self._get_default_settings()
        return self._save_settings()
