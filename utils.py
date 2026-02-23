from logger_config import setup_logger

logger = setup_logger(__name__)  # logs go to console + logs/utils.log

def helper_function():
    logger.info("Helper function running")