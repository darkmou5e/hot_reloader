import re
import os
import pathlib

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from .log import log
from .deps import hot_reload_modules_dependend_on, path_to_module


class _FileChangeEventHandler(FileSystemEventHandler):
    # TODO: Refactor "root_dir" logic
    def __init__(self, root_path, root_dir, after_reload_hook):
        self._root_path = root_path
        self._root_dir = root_dir
        self._root_parent_path = pathlib.Path(root_path).parent
        self._after_reload_hook = after_reload_hook
        log.debug(f"FileChange observer init: root_path={self._root_path}, root_dir={self._root_dir}, root_parent_path={self._root_parent_path}")

    def on_any_event(self, event: FileSystemEvent) -> None:
        root_path = pathlib.Path(self._root_path)
        src_path = event.src_path
        log.debug(f"New file system event: {event}")

        try:
            if re.match(r"^[^#]+\.py$", src_path):
                file_path = pathlib.Path(src_path)
                rel_path = file_path.relative_to(self._root_parent_path).as_posix()
                mod_name = path_to_module(rel_path)
                log.debug(f"Python file has been changed. file_path={file_path}, root_relative_path={rel_path}")
                log.debug(f"Reload modules after {mod_name} change")
                hot_reload_modules_dependend_on(mod_name, self._root_dir)
                if self._after_reload_hook:
                    log.debug(f"Calling after reload hook for {mod_name} change")
                    self._after_reload_hook(mod_name)
        except Exception as e:
            log.exception("hot reload exception!")
            log.exception(e)


def start_hot_reloading(root_dir="hot_reload", after_reload_hook=None):
    root_path = os.getcwd() + "/" + root_dir
    log.info(f"Start with root_dir={root_dir} and root_path={root_path}")

    event_handler = _FileChangeEventHandler(root_path, root_dir, after_reload_hook)
    observer = Observer()
    observer.schedule(event_handler, root_path, recursive=True)
    observer.start()
