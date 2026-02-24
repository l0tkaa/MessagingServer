# logger_config.py
import logging
import os
import threading
import time
import sys



# Create logs folder if it doesn't exist
os.makedirs("logs", exist_ok=True)

class ContextFilter(logging.Filter):
    """
    Adds thread name, local/UTC time, and client IP to all logs.
    """
    def filter(self, record):
        record.thread_name = threading.current_thread().name
        record.localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        record.utctime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        if not hasattr(record, 'client_ip'):
            record.client_ip = "N/A"
        return True

def setup_logger(name, level=logging.DEBUG):
    """
    Returns a logger that logs to console + file, with context filter.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        logger.addFilter(ContextFilter())

        # Console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_fmt = '[%(localtime)s | UTC %(utctime)s] [%(thread_name)s] %(name)s %(levelname)s: %(message)s (IP: %(client_ip)s)'
        console_handler.setFormatter(logging.Formatter(fmt=console_fmt))
        logger.addHandler(console_handler)

        # File
        file_handler = logging.FileHandler(f"logs/{name}.log")
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(fmt=console_fmt))
        logger.addHandler(file_handler)

    return logger

def setup_global_exception_handler(logger):
    """
    Logs uncaught exceptions automatically.
    """
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    sys.excepthook = handle_exception

def log_calls(func):
    """
    Decorator to log function entry/exit automatically.
    """
    logger_name = func.__module__
    logger = logging.getLogger(logger_name)
    def wrapper(*args, **kwargs):
        logger.debug(f"Entering {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        logger.debug(f"Exiting {func.__name__} returning {result}")
        return result
    return wrapper

# --- Automatic socket wrappers --- #

def wrap_socket_recv(sock, client_ip, bufsize=1024, logger_name="server"):
    """
    Wrapper for socket.recv that logs automatically.
    """
    logger = logging.getLogger(logger_name)
    try:
        data = sock.recv(bufsize)
        if data:
            logger.info(f"Received: {data.decode(errors='ignore')}", extra={"client_ip": client_ip})
        else:
            logger.info("Client disconnected", extra={"client_ip": client_ip})
        return data
    except Exception as e:
        logger.error(f"Error receiving data: {e}", extra={"client_ip": client_ip})
        raise


def wrap_socket_send(sock, client_ip, data, logger_name="server"):
    """
    Wrapper for socket.sendall that logs automatically.
    """
    logger = logging.getLogger(logger_name)
    try:
        sock.sendall(data)
        logger.info(f"Sent: {data.decode(errors='ignore')}", extra={"client_ip": client_ip})
    except Exception as e:
        logger.error(f"Error sending data: {e}", extra={"client_ip": client_ip})
        raise