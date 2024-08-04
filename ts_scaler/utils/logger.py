import logging


def setup_logger(name: str ="ts_scaler.utils.logger")-> logging.Logger:
    if logging.getLogger(name).handlers:
        return logging.getLogger(name)

    # Create a new logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)

    return logger
