"""
Log file - function to log program workflow in command line and separate files
@M-Malek
"""
import logging
import os

# Class: custom logging message colors:
RESET = "\033[0m"
COLORS = {
    "DEBUG": "\033[36m",     # cyan
    "INFO": "\033[32m",      # green
    "WARNING": "\033[33m",   # yellow
    "ERROR": "\033[31m",     # red
    "CRITICAL": "\033[41m",  # red background
}


class ColorFormatter(logging.Formatter):
    def format(self, record):
        color = COLORS.get(record.levelname, RESET)
        record.msg = f"{color}{record.getMessage()}{RESET}"
        return super().format(record)


def main_logger(message_type, message_body):
    """
    Save log message to .log file in default microservice folder
    :param message: str, message for logger
    :return: logging service status
    """
    # Create logger object
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s: %(levelname)s: %(message)s'
        )

        # Handler do pliku
        if "LOG_FILE" in os.environ:
            log_file = os.getenv("LOG_FILE")
        else:
            log_file = "log_file.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        # Handler do konsoli
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColorFormatter(
            '%(asctime)s: %(levelname)s: %(message)s'
        ))

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    """logging.basicConfig(filename="log_file.log",
                        format='%(asctime)s: %(levelname)s: %(message)s',
                        level=logging.INFO)"""

    # Create logger object body based on information given by user. Save info in file and print it to console
    """if message_type == "warning":
        logger.warning(message_body)
        
    if message_type == "info":
        logger.info(message_body)
        
    if message_type == "error":
        logger.error(message_body)
        
    if message_type == "crit":
        logger.critical(message_body)"""
    # Idea: add third variable called "service_type" which should be added to message_body:
    # service_type + ": " + message_body
    # then create one log file for logging for all 4 services - check if it is possible!
    match message_type:
        case "info":
            logger.info(message_body)
        case "warning":
            logger.warning(message_body)
        case "error":
            logger.error(message_body)
        case "crit":
            logger.critical(message_body)
        case _:
            logger.info(message_body)

