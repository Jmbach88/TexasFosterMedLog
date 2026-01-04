"""
Data Migration Module
Handles migration of data from old location to user data directory
"""

import shutil
import logging
from pathlib import Path
from typing import Tuple
from .resource_manager import ResourceManager


logger = logging.getLogger(__name__)


class DataMigrator:
    """Handles data migration from development directory to user directory"""

    def __init__(self):
        self.resource_manager = ResourceManager()

    def needs_migration(self) -> bool:
        """
        Check if data migration is needed

        Returns:
            True if old data exists and new location is empty
        """
        old_data_dir = self.resource_manager.get_old_data_dir()
        new_data_dir = self.resource_manager.user_data_dir

        if not old_data_dir or not old_data_dir.exists():
            return False

        # Check if new directory is empty or doesn't have profiles.json
        profiles_path = new_data_dir / "profiles.json"
        return not profiles_path.exists()

    def migrate_data(self) -> Tuple[bool, str]:
        """
        Migrate data from old location to new user data directory

        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self.needs_migration():
            return True, "No migration needed"

        old_data_dir = self.resource_manager.get_old_data_dir()
        new_data_dir = self.resource_manager.user_data_dir

        try:
            logger.info(f"Migrating data from {old_data_dir} to {new_data_dir}")

            # Migrate profiles.json
            old_profiles = old_data_dir / "profiles.json"
            if old_profiles.exists():
                new_profiles = new_data_dir / "profiles.json"
                shutil.copy2(old_profiles, new_profiles)
                logger.info(f"Migrated profiles.json")

            # Migrate patients directory
            old_patients = old_data_dir / "patients"
            if old_patients.exists():
                new_patients = new_data_dir / "patients"
                if new_patients.exists():
                    # Merge directories
                    self._merge_directories(old_patients, new_patients)
                else:
                    # Copy entire directory
                    shutil.copytree(old_patients, new_patients)
                logger.info(f"Migrated patients directory")

            # Migrate logs directory (old structure)
            old_logs = old_data_dir / "logs"
            if old_logs.exists():
                # Old logs were stored in data/logs, now they go in data/patients/{profile_id}
                self._migrate_old_logs(old_logs)
                logger.info(f"Migrated logs directory")

            logger.info("Data migration completed successfully")
            return True, f"Successfully migrated data to {new_data_dir}"

        except Exception as e:
            error_msg = f"Error during data migration: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def _merge_directories(self, src: Path, dst: Path):
        """
        Recursively merge source directory into destination

        Args:
            src: Source directory path
            dst: Destination directory path
        """
        for item in src.iterdir():
            src_item = src / item.name
            dst_item = dst / item.name

            if src_item.is_dir():
                dst_item.mkdir(exist_ok=True)
                self._merge_directories(src_item, dst_item)
            else:
                if not dst_item.exists():
                    shutil.copy2(src_item, dst_item)

    def _migrate_old_logs(self, old_logs_dir: Path):
        """
        Migrate logs from old structure to new structure

        Old: data/logs/{profile_id}_{month_year}.json
        New: data/patients/{profile_id}/{profile_id}_{month_year}.json

        Args:
            old_logs_dir: Path to old logs directory
        """
        for log_file in old_logs_dir.glob("*.json"):
            filename = log_file.name

            # Extract profile_id from filename
            # Format is typically: {profile_id}_{month}_{year}.json
            parts = filename.replace('.json', '').split('_')

            if len(parts) >= 3:
                # Assume first part is profile_id
                profile_id = parts[0]

                # Create patient directory
                patient_dir = self.resource_manager.get_patient_dir(profile_id)

                # Copy log file to new location
                new_log_path = patient_dir / filename
                if not new_log_path.exists():
                    shutil.copy2(log_file, new_log_path)
                    logger.info(f"Migrated log: {filename}")

    def create_migration_marker(self):
        """Create a marker file to indicate migration has been completed"""
        marker_file = self.resource_manager.user_data_dir / ".migrated"
        marker_file.touch()
        logger.info("Created migration marker file")

    def is_migrated(self) -> bool:
        """
        Check if migration has already been completed

        Returns:
            True if migration marker exists
        """
        marker_file = self.resource_manager.user_data_dir / ".migrated"
        return marker_file.exists()

    def run_migration_if_needed(self) -> Tuple[bool, str]:
        """
        Run migration if needed and create marker

        Returns:
            Tuple of (success: bool, message: str)
        """
        if self.is_migrated():
            return True, "Already migrated"

        if not self.needs_migration():
            self.create_migration_marker()
            return True, "No migration needed"

        success, message = self.migrate_data()

        if success:
            self.create_migration_marker()

        return success, message
