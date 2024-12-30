import re
import os
import pathlib
import sys
import importlib

from .import_parser import get_deps_list
from .log import log

def path_to_module(path: str) -> str:
    mod_name = re.sub(r"[/\\]", ".", path)
    if path.endswith(".py"):
        return mod_name[:-3]
    else:
        return mod_name


def get_hot_reload_dir_deps(root_dir):
    deps_by_mods = {}

    root_path = pathlib.Path(root_dir)
    for path, dirs, files in os.walk(root_path):
        # skip __pycache__ and so on
        if "__" in path:
            log.debug(f"Skip path {path}")
            continue

        current_path = pathlib.Path(path)
        relative_path = current_path.relative_to(root_path)
        mod_name = root_dir + "." + re.sub(r"[/\\]", ".", relative_path.as_posix())

        for f in files:
            if f.endswith(".py"):
                file_mod_name = root_dir + "." + path_to_module(f)
                deps = get_deps_list(path + "/" + f)
                log.debug(f"Found dependencies for {file_mod_name}. deps={deps}")

                for dep in deps:
                    if dep.startswith(root_dir):
                      if dep in deps_by_mods:
                          deps_by_mods[dep].add(file_mod_name)
                      else:
                          deps_by_mods[dep] = {file_mod_name}
    log.debug(f"Calculated dependencies by mods {deps_by_mods}")
    return deps_by_mods


def hot_reload_modules_dependend_on(mod_name, root_dir):
    deps = get_hot_reload_dir_deps(root_dir)
    # optimization. If module is not loaded, there is no need to reload
    if not mod_name in sys.modules:
        log.debug(f"Module {mod_name} is not in sys.modules. Skipping it.")
        return

    log.info(f"Reload module {mod_name}")
    mod = sys.modules[mod_name]
    importlib.reload(mod)

    if mod_name in deps:
        for dep in deps[mod_name]:
            # reload modules that depend on current
            hot_reload_modules_dependend_on(dep, root_dir)
