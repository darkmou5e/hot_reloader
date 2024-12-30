from .log import setup_logger
setup_logger()

from .fs_observer import start_hot_reloading

__all__ = ["start_hot_reloading"]
