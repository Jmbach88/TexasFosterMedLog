"""
Logging Configuration Module
Sets up application logging to user data directory
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from .resource_manager import ResourceManager


def setup_logging(log_level: int = logging.INFO) -> logging.Logger:
    """
    Configure application logging

    Args:
        log_level: Logging level (default: INFO)

    Returns:
        Configured logger instance
    """
    # Get log directory from ResourceManager
    resource_manager = ResourceManager()
    log_dir = resource_manager.get_log_dir()

    # Create log filename with date
    log_filename = f"medication_logger_{datetime.now().strftime('%Y%m%d')}.log"
    log_file = log_dir / log_filename

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove any existing handlers
    root_logger.handlers.clear()

    # File handler - logs everything
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Console handler - only warnings and errors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("Medication Logger Application Starting")
    logger.info(f"Log file: {log_file}")
    logger.info(f"User data directory: {resource_manager.user_data_dir}")
    logger.info(f"Running from: {resource_manager.base_path}")
    logger.info(f"Frozen: {resource_manager.is_frozen()}")
    logger.info("=" * 60)

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def log_exception(logger: logging.Logger, exception: Exception, context: str = ""):
    """
    Log an exception with full traceback

    Args:
        logger: Logger instance
        exception: Exception to log
        context: Optional context description
    """
    if context:
        logger.error(f"{context}: {str(exception)}", exc_info=True)
    else:
        logger.error(f"Exception occurred: {str(exception)}", exc_info=True)


def clean_old_logs(days_to_keep: int = 30):
    """
    Delete log files older than specified days

    Args:
        days_to_keep: Number of days of logs to retain
    """
    try:
        resource_manager = ResourceManager()
        log_dir = resource_manager.get_log_dir()

        if not log_dir.exists():
            return

        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)

        for log_file in log_dir.glob("medication_logger_*.log"):
            try:
                # Get file modification time
                mtime = datetime.fromtimestamp(log_file.stat().st_mtime)

                if mtime < cutoff_date:
                    log_file.unlink()
                    logging.info(f"Deleted old log file: {log_file.name}")

            except Exception as e:
                logging.warning(f"Could not delete log file {log_file.name}: {e}")

    except Exception as e:
        logging.error(f"Error cleaning old logs: {e}")
