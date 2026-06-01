import logging
import sys

class ColoredFormatter(logging.Formatter):
    """Custom logging formatter with localized colors and a bold module name."""
    
    # ANSI escape sequences
    RESET = "\x1b[0m"
    BOLD = "\x1b[1m"
    
    # Colors
    GREY = "\x1b[38;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    BLUE = "\x1b[34;20m"

    def __init__(self, datefmt='%H:%M:%S %Y-%m-%d '):
        super().__init__(datefmt=datefmt)
        
        # Standard white layout template with a bold module tag at the end
        def make_fmt(color_code):
            return f"{color_code}%(levelname)s{self.RESET}: %(message)s %(asctime)s, {self.BOLD}%(name)s{self.RESET}"
        
        # Pre-compile formatters with localized color codes
        self.formatters = {
            logging.DEBUG: logging.Formatter(make_fmt(self.GREY), datefmt=datefmt),
            logging.INFO: logging.Formatter(make_fmt(self.BLUE), datefmt=datefmt),
            logging.WARNING: logging.Formatter(make_fmt(self.YELLOW), datefmt=datefmt),
            logging.ERROR: logging.Formatter(make_fmt(self.RED), datefmt=datefmt),
            logging.CRITICAL: logging.Formatter(make_fmt(self.BOLD_RED), datefmt=datefmt),
        }

    def format(self, record):
        formatter = self.formatters.get(record.levelno)
        if formatter:
            return formatter.format(record)
        return super().format(record)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        
        formatter = ColoredFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

# Test execution
if __name__ == "__main__":
    log = get_logger("my_app_module")
    log.info("This text is standard color.")
    log.warning("This text is also standard color.")
    log.error("This text is standard, but ERROR is red.")

