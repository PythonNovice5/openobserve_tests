import logging
import os

def get_logger():
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Create a stream handler for console output
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Create a file handler for writing logs to test.log
        log_dir = os.path.abspath(os.path.join('.', 'ui_tests')) 
        log_file = os.path.join(log_dir, 'ui_test.log')

        fh = logging.FileHandler(log_file, mode='w')
        fh.setLevel(logging.INFO)

        # Create log format
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
        
        # Set the formatter for both handlers
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        # Add the handlers to the logger
        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger
