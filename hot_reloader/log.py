import logging

log = None

def setup_logger():
    global log
    logger_name = "hot_reloader"
    log = logging.getLogger(logger_name)
    logging.basicConfig(filename=f"{logger_name}.log", level=logging.DEBUG)
