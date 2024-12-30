import time

import hot_reloader


def post_reload_hook(mod_name):
    print(f"post reload {mod_name}")

hot_reloader.start_hot_reloading(root_dir="hot_reload", after_reload_hook=post_reload_hook)

from hot_reload.target import hello_from_target

print(hello_from_target())

time.sleep(1000)
