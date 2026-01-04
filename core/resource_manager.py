"""
Resource Manager Module
Handles paths for bundled resources and user data directories
Supports both development and PyInstaller bundled environments
"""

import os
import sys
from pathlib import Path
from typing import Optional


class ResourceManager:
    """Manages resource and data paths for both development and bundled environments"""

    _instance = None

    def __new__(cls):
        """Singleton pattern to ensure only one instance exists"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize resource manager"""
        if self._initialized:
            return

        self._initialized = True
        self._base_path = self._get_base_path()
        self._user_data_dir = self._get_user_data_dir()
        self._ensure_user_directories()

    def _get_base_path(self) -> Path:
        """
        Get the base path for bundled resources

        Returns:
            Path to bundled resources (handles PyInstaller's _MEIPASS)
        """
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # Running in PyInstaller bundle
            return Path(sys._MEIPASS)
        else:
            # Running in development mode
            return Path(__file__).parent.parent

    def _get_user_data_dir(self) -> Path:
        """
        Get the user data directory

        Returns:
            Path to user data directory (~/MedicationLogger/data)
        """
        home = Path.home()
        app_dir = home / "MedicationLogger"
        return app_dir / "data"

    def _ensure_user_directories(self):
        """Create user data directories if they don't exist"""
        # Create main data directory
        self._user_data_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        (self._user_data_dir / "patients").mkdir(exist_ok=True)
        (self._user_data_dir / "logs").mkdir(exist_ok=True)

    @property
    def base_path(self) -> Path:
        """Get the base path for bundled resources"""
        return self._base_path

    @property
    def user_data_dir(self) -> Path:
        """Get the user data directory"""
        return self._user_data_dir

    def get_resource_path(self, relative_path: str) -> Path:
        """
        Get the absolute path to a bundled resource

        Args:
            relative_path: Relative path to resource (e.g., 'templates/med_log_template.docx')

        Returns:
            Absolute path to the resource
        """
        return self._base_path / relative_path

    def get_data_path(self, relative_path: str) -> Path:
        """
        Get the absolute path to a user data file

        Args:
            relative_path: Relative path within user data dir (e.g., 'profiles.json')

        Returns:
            Absolute path to the data file
        """
        return self._user_data_dir / relative_path

    def get_template_path(self, template_name: str = 'med_log_template.docx') -> Path:
        """
        Get the path to the Word template file

        Args:
            template_name: Name of the template file

        Returns:
            Absolute path to the template
        """
        return self.get_resource_path(f'templates/{template_name}')

    def get_profiles_path(self) -> Path:
        """Get the path to the profiles.json file"""
        return self.get_data_path('profiles.json')

    def get_patient_dir(self, profile_id: str) -> Path:
        """
        Get the directory for a specific patient

        Args:
            profile_id: The patient's profile ID

        Returns:
            Path to patient directory
        """
        patient_dir = self.get_data_path(f'patients/{profile_id}')
        patient_dir.mkdir(parents=True, exist_ok=True)
        return patient_dir

    def get_log_path(self, profile_id: str, month_year: str) -> Path:
        """
        Get the path to a medication log file

        Args:
            profile_id: The patient's profile ID
            month_year: Month and year (e.g., 'January 2025')

        Returns:
            Path to the log file
        """
        patient_dir = self.get_patient_dir(profile_id)
        filename = f"{profile_id}_{month_year.replace(' ', '_')}.json"
        return patient_dir / filename

    def get_medication_card_path(self, profile_id: str, medicine_name: str) -> Path:
        """
        Get the path to a medication card file

        Args:
            profile_id: The patient's profile ID
            medicine_name: Name of the medication

        Returns:
            Path to the medication card file
        """
        patient_dir = self.get_patient_dir(profile_id)
        cards_dir = patient_dir / "medication_cards"
        cards_dir.mkdir(exist_ok=True)

        # Sanitize medicine name for filename
        safe_name = medicine_name.replace(' ', '_').replace('/', '_')
        return cards_dir / f"{safe_name}.json"

    def get_log_dir(self) -> Path:
        """Get the logs directory for application logs"""
        log_dir = self._user_data_dir.parent / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir

    def list_patient_logs(self, profile_id: str) -> list:
        """
        List all medication logs for a patient

        Args:
            profile_id: The patient's profile ID

        Returns:
            List of (month_year, file_path) tuples
        """
        patient_dir = self.get_patient_dir(profile_id)
        logs = []

        if patient_dir.exists():
            for file in patient_dir.glob(f"{profile_id}_*.json"):
                # Extract month_year from filename
                filename = file.stem
                month_year = filename.replace(f"{profile_id}_", "").replace('_', ' ')
                logs.append((month_year, file))

        return sorted(logs)

    def list_medication_cards(self, profile_id: str) -> list:
        """
        List all medication cards for a patient

        Args:
            profile_id: The patient's profile ID

        Returns:
            List of (medicine_name, file_path) tuples
        """
        patient_dir = self.get_patient_dir(profile_id)
        cards_dir = patient_dir / "medication_cards"
        cards = []

        if cards_dir.exists():
            for file in cards_dir.glob("*.json"):
                medicine_name = file.stem.replace('_', ' ')
                cards.append((medicine_name, file))

        return sorted(cards)

    def is_frozen(self) -> bool:
        """Check if running in a PyInstaller bundle"""
        return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

    def get_old_data_dir(self) -> Optional[Path]:
        """
        Get the old data directory location (for migration)

        Returns:
            Path to old data directory if it exists, None otherwise
        """
        old_dir = self._base_path / "data"
        return old_dir if old_dir.exists() else None
