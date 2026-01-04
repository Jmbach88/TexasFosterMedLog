"""
Application Configuration
Contains version information and application constants
"""

# Application metadata
APP_NAME = "Medication Logger"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Medication Tracker Team"
APP_DESCRIPTION = "Track medication administration for foster care patients"

# Build information (updated automatically by build script)
BUILD_NUMBER = 9
BUILD_DATE = "2026-01-01"

# Application settings
DEFAULT_EXPORT_DIR = "exports"
SUPPORTED_EXPORT_FORMATS = ['word', 'pdf', 'excel']

# File names
TEMPLATE_NAME = "med_log_template.docx"
PROFILES_FILE = "profiles.json"

# User data directory name
USER_DATA_DIRNAME = "MedicationLogger"

def get_version_string() -> str:
    """
    Get formatted version string

    Returns:
        Version string with build number
    """
    return f"{APP_VERSION} (Build {BUILD_NUMBER})"

def get_about_text() -> str:
    """
    Get formatted about text for the application

    Returns:
        Multi-line about text
    """
    return f"""{APP_NAME}
Version {get_version_string()}

{APP_DESCRIPTION}

Build Date: {BUILD_DATE}
"""
