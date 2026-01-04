"""
Log Management Module
Handles CRUD operations for medication administration logs
"""

import json
import os
import tempfile
from datetime import datetime
from typing import Dict, Optional, List
from collections import defaultdict
from .resource_manager import ResourceManager


class LogManager:
    """Manages medication administration logs with persistent JSON storage"""

    def __init__(self, data_dir: str = None):
        """
        Initialize LogManager

        Args:
            data_dir: Optional legacy data directory (for backward compatibility)
                     If None, uses ResourceManager to determine path
        """
        if data_dir is None:
            # Use ResourceManager for new path structure
            self.resource_manager = ResourceManager()
            self.data_dir = str(self.resource_manager.user_data_dir / "patients")
        else:
            # Legacy mode for development/testing
            self.resource_manager = None
            self.data_dir = data_dir

        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """Create patients directory if it doesn't exist"""
        os.makedirs(self.data_dir, exist_ok=True)

    def _get_patient_logs_dir(self, profile_id: str) -> str:
        """Get patient-specific logs directory"""
        logs_dir = os.path.join(self.data_dir, profile_id, "logs")
        os.makedirs(logs_dir, exist_ok=True)
        return logs_dir

    def _get_log_filename(self, profile_id: str, medicine_name: str, month_year: str) -> str:
        """Generate log filename from profile_id, medicine_name, and month_year"""
        # Convert to safe filename format
        safe_medicine = medicine_name.lower().replace(' ', '_').replace(',', '').replace('/', '_')
        safe_month = month_year.lower().replace(' ', '_').replace(',', '')
        logs_dir = self._get_patient_logs_dir(profile_id)
        return os.path.join(logs_dir, f"{safe_medicine}_{safe_month}.json")
    
    def _load_log(self, filename: str) -> Optional[Dict]:
        """Load log from file"""
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (IOError, json.JSONDecodeError) as e:
                raise RuntimeError(f"Failed to load log from {filename}: {str(e)}")
        return None
    
    def _save_log(self, filename: str, log_data: Dict):
        """Save log to file using atomic write"""
        # Get directory of log file
        log_dir = os.path.dirname(filename)

        # Create temporary file in same directory
        fd, temp_path = tempfile.mkstemp(dir=log_dir, suffix='.json.tmp')

        try:
            # Write to temporary file
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)

            # Atomic rename - replaces target file
            if os.path.exists(filename):
                os.replace(temp_path, filename)
            else:
                os.rename(temp_path, filename)

        except Exception as e:
            # Clean up temp file on failure
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass  # Best effort cleanup
            raise RuntimeError(f"Failed to save log to {filename}: {str(e)}")
    
    def get_log(self, profile_id: str, medicine_name: str, month_year: str) -> Optional[Dict]:
        """Get log for specific patient/medicine/month"""
        filename = self._get_log_filename(profile_id, medicine_name, month_year)
        return self._load_log(filename)
    
    def create_log(self, profile_id: str, month_year: str, medication_info: Dict) -> Dict:
        """
        Create new log for a patient/month
        medication_info should contain: medicine_name, strength, dosage, reason_prescribed, reason_prn
        """
        medicine_name = medication_info.get('medicine_name', '')

        log_data = {
            'profile_id': profile_id,
            'month_year': month_year,
            'medicine_name': medicine_name,
            'strength': medication_info.get('strength', ''),
            'dosage': medication_info.get('dosage', ''),
            'reason_prescribed': medication_info.get('reason_prescribed', ''),
            'reason_prn': medication_info.get('reason_prn', ''),
            'administration_log': [],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }

        filename = self._get_log_filename(profile_id, medicine_name, month_year)
        self._save_log(filename, log_data)

        return log_data
    
    def save_log(self, profile_id: str, medicine_name: str, month_year: str, log_data: Dict):
        """Save/update entire log"""
        log_data['updated_at'] = datetime.now().isoformat()
        filename = self._get_log_filename(profile_id, medicine_name, month_year)
        self._save_log(filename, log_data)
    
    def log_exists(self, profile_id: str, medicine_name: str, month_year: str) -> bool:
        """Check if log exists for patient/medicine/month"""
        filename = self._get_log_filename(profile_id, medicine_name, month_year)
        return os.path.exists(filename)
    
    def list_logs_for_profile(self, profile_id: str) -> List[tuple]:
        """Get list of all logs for a profile as (medicine_name, month_year) tuples"""
        logs = []
        logs_dir = self._get_patient_logs_dir(profile_id)

        if not os.path.exists(logs_dir):
            return logs

        for filename in os.listdir(logs_dir):
            if filename.endswith('.json'):
                # Load the file to get the actual medicine_name and month_year
                log_data = self._load_log(os.path.join(logs_dir, filename))
                if log_data:
                    medicine_name = log_data.get('medicine_name', '')
                    month_year = log_data.get('month_year', '')
                    logs.append((medicine_name, month_year))

        return sorted(logs, key=lambda x: (x[1], x[0]))  # Sort by month_year, then medicine_name
    
    def add_entry(self, profile_id: str, medicine_name: str, month_year: str, entry_data: Dict):
        """
        Add administration entry to log
        entry_data should contain: day, time, initials, amount_remaining
        """
        log_data = self.get_log(profile_id, medicine_name, month_year)

        if log_data is None:
            # Log doesn't exist, can't add entry
            raise ValueError(f"Log for {profile_id} / {medicine_name} / {month_year} does not exist")

        # Add entry
        log_data['administration_log'].append(entry_data)

        # Sort entries by day
        log_data['administration_log'].sort(key=lambda x: x['day'])

        # Save
        self.save_log(profile_id, medicine_name, month_year, log_data)
    
    def get_entries_for_day(self, profile_id: str, medicine_name: str, month_year: str, day: int) -> List[Dict]:
        """Get all entries for a specific day"""
        log_data = self.get_log(profile_id, medicine_name, month_year)

        if log_data is None:
            return []

        return [entry for entry in log_data['administration_log'] if entry['day'] == day]
    
    def update_entry(self, profile_id: str, medicine_name: str, month_year: str, day: int,
                     admin_index: int, entry_data: Dict):
        """
        Update specific entry
        admin_index is 0-2 for the 1st, 2nd, or 3rd administration that day
        """
        log_data = self.get_log(profile_id, medicine_name, month_year)

        if log_data is None:
            raise ValueError(f"Log for {profile_id} / {medicine_name} / {month_year} does not exist")

        # Find entries for this day
        day_entries_indices = [
            i for i, entry in enumerate(log_data['administration_log'])
            if entry['day'] == day
        ]

        if admin_index >= len(day_entries_indices):
            raise ValueError(f"No entry at index {admin_index} for day {day}")

        # Update the entry
        actual_index = day_entries_indices[admin_index]
        log_data['administration_log'][actual_index] = entry_data

        # Save
        self.save_log(profile_id, medicine_name, month_year, log_data)
    
    def delete_entry(self, profile_id: str, medicine_name: str, month_year: str, day: int, admin_index: int):
        """
        Delete specific entry
        admin_index is 0-2 for the 1st, 2nd, or 3rd administration that day
        """
        log_data = self.get_log(profile_id, medicine_name, month_year)

        if log_data is None:
            raise ValueError(f"Log for {profile_id} / {medicine_name} / {month_year} does not exist")

        # Find entries for this day
        day_entries_indices = [
            i for i, entry in enumerate(log_data['administration_log'])
            if entry['day'] == day
        ]

        if admin_index >= len(day_entries_indices):
            raise ValueError(f"No entry at index {admin_index} for day {day}")

        # Delete the entry
        actual_index = day_entries_indices[admin_index]
        del log_data['administration_log'][actual_index]

        # Save
        self.save_log(profile_id, medicine_name, month_year, log_data)
    
    def delete_all_entries_for_day(self, profile_id: str, medicine_name: str, month_year: str, day: int):
        """Delete all entries for a specific day"""
        log_data = self.get_log(profile_id, medicine_name, month_year)

        if log_data is None:
            raise ValueError(f"Log for {profile_id} / {medicine_name} / {month_year} does not exist")

        # Remove all entries for this day
        log_data['administration_log'] = [
            entry for entry in log_data['administration_log']
            if entry['day'] != day
        ]

        # Save
        self.save_log(profile_id, medicine_name, month_year, log_data)
    
    def get_administration_summary(self, profile_id: str, medicine_name: str, month_year: str) -> Dict:
        """Get summary of which days have entries"""
        log_data = self.get_log(profile_id, medicine_name, month_year)

        if log_data is None:
            return {}

        # Count entries per day
        summary = defaultdict(int)
        for entry in log_data['administration_log']:
            summary[entry['day']] += 1

        return dict(summary)
    
    def delete_log(self, profile_id: str, medicine_name: str, month_year: str) -> bool:
        """Delete entire log file"""
        filename = self._get_log_filename(profile_id, medicine_name, month_year)

        if os.path.exists(filename):
            os.remove(filename)
            return True

        return False
