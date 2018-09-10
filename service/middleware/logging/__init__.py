import logging
from os import path


def logging_factory(root_directory):
    logger = logging.getLogger("ocr-logger")
    fh = logging.FileHandler(path.join(root_directory, "log", "ocr.log"))
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)

    def log_data(request, response, exception=None, data=None):
        if response is not None and not response.status == 200:
            error_message = f"[{response.status}] Caught Exception while trying to process request => {request.path}"
            logger.exception(error_message)
        else:
            success_message = (
                f"[{response.status}] Successfully processed request => {request.path}"
            )
            logger.info(success_message)

    return log_data
