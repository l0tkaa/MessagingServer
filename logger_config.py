# logger_config.py
import logging
import os

# optional: create a logs folder
os.makedirs("logs", exist_ok=True)

def setup_logger(name, level=logging.DEBUG):
    """
    Returns a logger that logs to both console and file.
    - name: string, e.g., 'server', 'client', or module name
    - level: logging level (DEBUG/INFO/etc.)
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:  # prevent adding multiple handlers
        # 1️⃣ Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_formatter = logging.Formatter(
            fmt='[%(asctime)s] %(name)s %(levelname)s: %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # 2️⃣ File handler (logs/<name>.log)
        file_handler = logging.FileHandler(f"logs/{name}.log")
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(
            fmt='[%(asctime)s] %(name)s %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'  # more precise timestamp in file
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger
