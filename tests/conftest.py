import pytest
import logging
from datetime import datetime

current_time = datetime.now().strftime("%Y%m%d-%H%M%S")


@pytest.fixture(scope="session", autouse=True)
def setup_logging_for_tests():
    log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # File handler
    file_handler = logging.FileHandler(f'logs/test_log_{current_time}.log')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)  # or any other level

    # Get logger and set handler
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    # Ensure the logging is reset at the end of the test session
    yield
    for handler in logger.handlers:
        logger.removeHandler(handler)
        handler.close()
