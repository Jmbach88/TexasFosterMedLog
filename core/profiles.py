"""
Profile Management Module
Handles CRUD operations for patient profiles
"""

import json
import os
import tempfile
from datetime import datetime
from typing import Dict, Optional, List
from pathlib import Path
from .resource_manager import ResourceManager


class ProfileManager:
    """Manages patient profiles with persistent JSON storage"""

    def __init__(self, data_dir: str = None):
        """
        Initialize ProfileManager

        Args:
            data_dir: Optional legacy data directory (for backward compatibility)
                     If None, uses ResourceManager to determine path
        """
        if data_dir is None:
            # Use ResourceManager for new path structure
            self.resource_manager = ResourceManager()
            self.profiles_file = str(self.resource_manager.get_profiles_path())
            self.data_dir = str(self.resource_manager.user_data_dir)
        else:
            # Legacy mode for development/testing
            self.resource_manager = None
            self.data_dir = data_dir
            self.profiles_file = os.path.join(data_dir, "profiles.json")

        self._ensure_data_dir()
        self._load_profiles()

    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist"""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def _load_profiles(self):
        """Load profiles from JSON file"""
        if os.path.exists(self.profiles_file):
            try:
                with open(self.profiles_file, 'r', encoding='utf-8') as f:
                    self.profiles = json.load(f)
            except (IOError, json.JSONDecodeError) as e:
                raise RuntimeError(f"Failed to load profiles from {self.profiles_file}: {str(e)}")
        else:
            self.profiles = {}
            self._save_profiles()
    
    def _save_profiles(self):
        """Save profiles to JSON file using atomic write"""
        # Get directory of profiles file
        profiles_dir = os.path.dirname(self.profiles_file)

        # Create temporary file in same directory
        fd, temp_path = tempfile.mkstemp(dir=profiles_dir, suffix='.json.tmp')

        try:
            # Write to temporary file
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump(self.profiles, f, indent=2, ensure_ascii=False)

            # Atomic rename - replaces target file
            # On Windows, need to remove target first if it exists
            if os.path.exists(self.profiles_file):
                os.replace(temp_path, self.profiles_file)
            else:
                os.rename(temp_path, self.profiles_file)

        except Exception as e:
            # Clean up temp file on failure
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass  # Best effort cleanup
            raise RuntimeError(f"Failed to save profiles to {self.profiles_file}: {str(e)}")
    
    def _generate_id(self, child_name: str) -> str:
        """Generate profile ID from child name"""
        # Convert to lowercase, replace spaces with underscores
        base_id = child_name.lower().replace(' ', '_').replace('.', '')
        
        # Remove non-alphanumeric characters except underscores
        base_id = ''.join(c for c in base_id if c.isalnum() or c == '_')
        
        # Handle duplicates by adding number
        profile_id = base_id
        counter = 1
        while profile_id in self.profiles:
            profile_id = f"{base_id}_{counter}"
            counter += 1
        
        return profile_id
    
    def get_all_profiles(self) -> Dict:
        """Get all profiles as dictionary"""
        return self.profiles.copy()
    
    def get_profile(self, profile_id: str) -> Optional[Dict]:
        """Get single profile by ID"""
        return self.profiles.get(profile_id)
    
    def get_profile_list(self) -> List[tuple]:
        """Get list of (profile_id, child_name) tuples for UI"""
        return [(pid, data['child_name']) for pid, data in self.profiles.items()]
    
    def create_profile(self, profile_data: Dict) -> str:
        """
        Create new profile
        Returns the generated profile_id
        """
        # Generate ID from child name
        profile_id = self._generate_id(profile_data['child_name'])
        
        # Add metadata
        profile_data['profile_id'] = profile_id
        profile_data['created_at'] = datetime.now().isoformat()
        profile_data['updated_at'] = datetime.now().isoformat()
        
        # Save
        self.profiles[profile_id] = profile_data
        self._save_profiles()
        
        return profile_id
    
    def update_profile(self, profile_id: str, profile_data: Dict) -> bool:
        """
        Update existing profile
        Returns True if successful, False if profile doesn't exist
        """
        if profile_id not in self.profiles:
            return False
        
        # Preserve metadata
        profile_data['profile_id'] = profile_id
        profile_data['created_at'] = self.profiles[profile_id].get('created_at')
        profile_data['updated_at'] = datetime.now().isoformat()
        
        self.profiles[profile_id] = profile_data
        self._save_profiles()
        
        return True
    
    def delete_profile(self, profile_id: str) -> bool:
        """
        Delete profile
        Returns True if successful, False if profile doesn't exist
        """
        if profile_id not in self.profiles:
            return False
        
        del self.profiles[profile_id]
        self._save_profiles()
        
        return True
    
    def profile_exists(self, profile_id: str) -> bool:
        """Check if profile exists"""
        return profile_id in self.profiles
    
    def search_profiles(self, search_term: str) -> Dict:
        """Search profiles by child name"""
        search_term = search_term.lower()
        return {
            pid: data for pid, data in self.profiles.items()
            if search_term in data['child_name'].lower()
        }
