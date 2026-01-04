"""
Medication Card Management Module
Handles CRUD operations for medication card templates
"""

import json
import os
import shutil
import tempfile
from datetime import datetime
from typing import Dict, Optional, List
from pathlib import Path
from PIL import Image
from .resource_manager import ResourceManager

# Register HEIF plugin for iPhone image support
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    # pillow-heif not installed - HEIC images won't be supported
    pass


class MedicationCardManager:
    """Manages medication card templates with image support"""

    def __init__(self, data_dir: str = None):
        """
        Initialize MedicationCardManager

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

    def _get_patient_dir(self, profile_id: str) -> str:
        """Get patient-specific directory"""
        patient_dir = os.path.join(self.data_dir, profile_id)
        os.makedirs(patient_dir, exist_ok=True)
        return patient_dir

    def _get_medication_cards_file(self, profile_id: str) -> str:
        """Get path to medication cards JSON file"""
        return os.path.join(self._get_patient_dir(profile_id), "medication_cards.json")

    def _get_medication_images_dir(self, profile_id: str, medicine_name: str) -> str:
        """Get directory for medication images"""
        safe_medicine = medicine_name.lower().replace(' ', '_').replace(',', '').replace('/', '_')
        images_dir = os.path.join(
            self._get_patient_dir(profile_id),
            "images",
            "medications",
            safe_medicine
        )
        os.makedirs(images_dir, exist_ok=True)
        return images_dir

    def _load_cards(self, profile_id: str) -> Dict:
        """Load all medication cards for a patient"""
        cards_file = self._get_medication_cards_file(profile_id)

        if os.path.exists(cards_file):
            try:
                with open(cards_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (IOError, json.JSONDecodeError) as e:
                raise RuntimeError(f"Failed to load medication cards from {cards_file}: {str(e)}")

        return {}

    def _save_cards(self, profile_id: str, cards: Dict):
        """Save medication cards to file using atomic write"""
        cards_file = self._get_medication_cards_file(profile_id)

        # Get directory of cards file
        cards_dir = os.path.dirname(cards_file)

        # Create temporary file in same directory
        fd, temp_path = tempfile.mkstemp(dir=cards_dir, suffix='.json.tmp')

        try:
            # Write to temporary file
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump(cards, f, indent=2, ensure_ascii=False)

            # Atomic rename - replaces target file
            if os.path.exists(cards_file):
                os.replace(temp_path, cards_file)
            else:
                os.rename(temp_path, cards_file)

        except Exception as e:
            # Clean up temp file on failure
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass  # Best effort cleanup
            raise RuntimeError(f"Failed to save medication cards to {cards_file}: {str(e)}")

    def get_all_cards(self, profile_id: str) -> Dict:
        """Get all medication cards for a patient"""
        return self._load_cards(profile_id)

    def get_card(self, profile_id: str, medicine_name: str) -> Optional[Dict]:
        """Get a specific medication card"""
        cards = self._load_cards(profile_id)
        return cards.get(medicine_name)

    def create_card(self, profile_id: str, card_data: Dict) -> Dict:
        """
        Create a new medication card
        card_data should contain: medicine_name, strength, dosage, reason_prescribed, reason_prn
        """
        medicine_name = card_data.get('medicine_name', '')

        if not medicine_name:
            raise ValueError("Medicine name is required")

        cards = self._load_cards(profile_id)

        if medicine_name in cards:
            raise ValueError(f"Medication card for '{medicine_name}' already exists")

        card = {
            'medicine_name': medicine_name,
            'strength': card_data.get('strength', ''),
            'dosage': card_data.get('dosage', ''),
            'reason_prescribed': card_data.get('reason_prescribed', ''),
            'reason_prn': card_data.get('reason_prn', ''),
            'images': [],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }

        cards[medicine_name] = card
        self._save_cards(profile_id, cards)

        return card

    def update_card(self, profile_id: str, medicine_name: str, card_data: Dict):
        """Update an existing medication card"""
        cards = self._load_cards(profile_id)

        if medicine_name not in cards:
            raise ValueError(f"Medication card for '{medicine_name}' does not exist")

        # Update fields (preserve images list)
        cards[medicine_name].update({
            'strength': card_data.get('strength', ''),
            'dosage': card_data.get('dosage', ''),
            'reason_prescribed': card_data.get('reason_prescribed', ''),
            'reason_prn': card_data.get('reason_prn', ''),
            'updated_at': datetime.now().isoformat()
        })

        self._save_cards(profile_id, cards)

    def delete_card(self, profile_id: str, medicine_name: str, delete_images: bool = True):
        """Delete a medication card and optionally its images"""
        cards = self._load_cards(profile_id)

        if medicine_name not in cards:
            raise ValueError(f"Medication card for '{medicine_name}' does not exist")

        # Delete images if requested
        if delete_images:
            images_dir = self._get_medication_images_dir(profile_id, medicine_name)
            if os.path.exists(images_dir):
                shutil.rmtree(images_dir)

        # Remove card
        del cards[medicine_name]
        self._save_cards(profile_id, cards)

    def add_image(self, profile_id: str, medicine_name: str, image_path: str) -> str:
        """
        Add an image to a medication card
        Returns the filename stored
        """
        cards = self._load_cards(profile_id)

        if medicine_name not in cards:
            raise ValueError(f"Medication card for '{medicine_name}' does not exist")

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        # Validate file size (max 10 MB)
        file_size = os.path.getsize(image_path)
        max_size = 10 * 1024 * 1024  # 10 MB in bytes
        if file_size > max_size:
            raise ValueError(f"Image file too large: {file_size / (1024*1024):.2f} MB (max 10 MB)")

        # Validate image format
        try:
            with Image.open(image_path) as img:
                # Verify it's a valid image
                img.verify()

                # Re-open for additional checks (verify() closes the file)
                with Image.open(image_path) as img:
                    # Check format is supported (includes mobile phone formats)
                    supported_formats = {'JPEG', 'PNG', 'GIF', 'BMP', 'TIFF', 'WEBP', 'HEIF', 'HEIC'}
                    if img.format not in supported_formats:
                        raise ValueError(f"Unsupported image format: {img.format}. Supported: {', '.join(sorted(supported_formats))}")

                    # Check image dimensions (max 4000x4000)
                    max_dimension = 4000
                    if img.width > max_dimension or img.height > max_dimension:
                        raise ValueError(f"Image dimensions too large: {img.width}x{img.height} (max {max_dimension}x{max_dimension})")

        except IOError as e:
            raise ValueError(f"Invalid or corrupted image file: {str(e)}")

        # Get destination directory
        images_dir = self._get_medication_images_dir(profile_id, medicine_name)

        # Generate unique filename
        original_filename = os.path.basename(image_path)
        dest_filename = original_filename
        dest_path = os.path.join(images_dir, dest_filename)

        # If file exists, add number suffix
        counter = 1
        while os.path.exists(dest_path):
            name, ext = os.path.splitext(original_filename)
            dest_filename = f"{name}_{counter}{ext}"
            dest_path = os.path.join(images_dir, dest_filename)
            counter += 1

        # Copy image to destination
        shutil.copy2(image_path, dest_path)

        # Update card with image reference
        if dest_filename not in cards[medicine_name]['images']:
            cards[medicine_name]['images'].append(dest_filename)
            cards[medicine_name]['updated_at'] = datetime.now().isoformat()
            self._save_cards(profile_id, cards)

        return dest_filename

    def remove_image(self, profile_id: str, medicine_name: str, filename: str):
        """Remove an image from a medication card"""
        cards = self._load_cards(profile_id)

        if medicine_name not in cards:
            raise ValueError(f"Medication card for '{medicine_name}' does not exist")

        # Remove from card
        if filename in cards[medicine_name]['images']:
            cards[medicine_name]['images'].remove(filename)
            cards[medicine_name]['updated_at'] = datetime.now().isoformat()
            self._save_cards(profile_id, cards)

        # Delete file
        image_path = os.path.join(
            self._get_medication_images_dir(profile_id, medicine_name),
            filename
        )

        if os.path.exists(image_path):
            os.remove(image_path)

    def get_image_path(self, profile_id: str, medicine_name: str, filename: str) -> str:
        """Get full path to an image file"""
        return os.path.join(
            self._get_medication_images_dir(profile_id, medicine_name),
            filename
        )

    def list_cards(self, profile_id: str) -> List[str]:
        """Get list of all medication card names for a patient"""
        cards = self._load_cards(profile_id)
        return sorted(cards.keys())
