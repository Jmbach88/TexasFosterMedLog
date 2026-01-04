#!/usr/bin/env python3
"""
Medication Log Tracker
Main entry point for the application
"""

import sys
import tkinter as tk
from tkinter import messagebox
import logging

# Import configuration
from config import APP_NAME, get_version_string

# Import core modules
from core.resource_manager import ResourceManager
from core.data_migration import DataMigrator
from core.logging_config import setup_logging, clean_old_logs, log_exception

# Import GUI
from gui.tkinter_app import MedicationTrackerApp


def initialize_application():
    """
    Initialize application resources and perform first-run setup

    Returns:
        Tuple of (success: bool, error_message: str or None)
    """
    try:
        # Set up logging first
        logger = setup_logging()
        logger.info(f"Initializing {APP_NAME} {get_version_string()}")

        # Clean old log files (keep last 30 days)
        clean_old_logs(days_to_keep=30)

        # Initialize resource manager (creates user directories)
        resource_manager = ResourceManager()
        logger.info(f"Resource manager initialized")
        logger.info(f"User data directory: {resource_manager.user_data_dir}")

        # Run data migration if needed
        migrator = DataMigrator()
        success, message = migrator.run_migration_if_needed()

        if not success:
            logger.error(f"Data migration failed: {message}")
            return False, f"Data migration failed:\n{message}"

        if "migrated" in message.lower() and "successfully" in message.lower():
            logger.info(f"Data migration completed: {message}")

        logger.info("Application initialization complete")
        return True, None

    except Exception as e:
        error_msg = f"Failed to initialize application: {str(e)}"
        logging.error(error_msg, exc_info=True)
        return False, error_msg


def main():
    """Launch the application"""
    logger = logging.getLogger(__name__)

    try:
        # Initialize application
        success, error_message = initialize_application()

        if not success:
            # Show error to user before GUI starts
            root = tk.Tk()
            root.withdraw()  # Hide main window
            messagebox.showerror(
                "Initialization Error",
                f"Failed to initialize {APP_NAME}:\n\n{error_message}\n\n"
                "Please check the log files for more details."
            )
            root.destroy()
            sys.exit(1)

        # Launch GUI
        logger.info("Launching GUI...")
        root = tk.Tk()
        app = MedicationTrackerApp(root)
        logger.info("GUI initialized successfully")

        # Run main loop
        root.mainloop()

        logger.info("Application closed normally")

    except Exception as e:
        # Log unexpected errors
        error_msg = f"Unexpected error in main: {str(e)}"
        if 'logger' in locals():
            log_exception(logger, e, "Unexpected error in main")
        else:
            logging.error(error_msg, exc_info=True)

        # Show error to user
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Application Error",
                f"An unexpected error occurred:\n\n{str(e)}\n\n"
                "Please check the log files for more details."
            )
            root.destroy()
        except:
            pass  # If even the error dialog fails, just exit

        sys.exit(1)


if __name__ == "__main__":
    main()
