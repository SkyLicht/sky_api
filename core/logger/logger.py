import logging
from logging.handlers import RotatingFileHandler

class Logger:
    _instances = {}  # Dictionary to store multiple logger instances

    @classmethod
    def get_logger(cls,
                   name: str = 'AppLogger',
                   log_file: str = 'config/logs/app.log',
                   max_file_size: int = 10 * 1024 * 1024,
                   backup_count: int = 3,
                   console_level=logging.WARNING,
                   file_level=logging.DEBUG):
        """
        Retrieve a logger by name, or create one if it doesn't exist.

        :param name: Name of the logger
        :param log_file: Path to the log file
        :param max_file_size: Maximum size of the log file before rotation (in bytes)
        :param backup_count: Number of backup files to keep
        :param console_level: Logging level for console output
        :param file_level: Logging level for file output
        :return: A logger instance
        """
        if name not in cls._instances:
            # Create and configure a new logger
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)  # Base level for all loggers

            # Prevent duplicate handlers
            if not logger.hasHandlers():
                # Console handler
                console_handler = logging.StreamHandler()
                console_handler.setLevel(console_level)

                # Rotating file handler
                file_handler = RotatingFileHandler(log_file, maxBytes=max_file_size, backupCount=backup_count)
                file_handler.setLevel(file_level)

                # Formatter
                formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'  # Format without milliseconds
                )
                console_handler.setFormatter(formatter)
                file_handler.setFormatter(formatter)

                # Add handlers
                logger.addHandler(console_handler)
                logger.addHandler(file_handler)

            # Store the logger in the dictionary
            cls._instances[name] = logger

        return cls._instances[name]
