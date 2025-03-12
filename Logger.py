import logging


class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    # Define the log format with the timestamp [HH:MM:SS] LOG_LEVEL MESSAGE
    format = "[%(asctime)s] %(levelname)-8s %(message)s"

    # Define the formats for different log levels
    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def __init__(self):
        # Call the constructor of the parent Formatter class
        super().__init__(datefmt="%H:%M:%S")  # Set time format to HH:MM:SS

    def format(self, record):
        # Get the log format based on the log level
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%H:%M:%S")
        return formatter.format(record)


# Create logger with 'My_app'
logger = logging.getLogger("My_app")
logger.setLevel(logging.DEBUG)

# Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Set custom formatter for the console handler
ch.setFormatter(CustomFormatter())

# Add handler to the logger
logger.addHandler(ch)
