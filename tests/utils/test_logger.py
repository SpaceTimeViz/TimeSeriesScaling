import logging

from ts_scaler.utils.logger import setup_logger


def test_setup_logger():
    logger = setup_logger()
    assert isinstance(logger, logging.Logger)
    assert logger.level == logging.INFO

    assert any(
        isinstance(handler, logging.StreamHandler) for handler in logger.handlers
    )

    reused_logger = setup_logger()
    assert reused_logger is logger

    assert reused_logger.level == logging.INFO
    assert any(
        isinstance(handler, logging.StreamHandler) for handler in reused_logger.handlers
    )
    file_handler = logging.FileHandler("test.log")
    reused_logger.addHandler(file_handler)
    assert any(
        isinstance(handler, logging.FileHandler) for handler in reused_logger.handlers
    )
