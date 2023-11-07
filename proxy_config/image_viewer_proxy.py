from image_viewer import app_file


def setup_proxy_config():
    return {
        "command": [
            "panel",
            "serve",
            str(app_file),
            "--allow-websocket-origin=*",
            "--port",
            "{port}",
        ],
        "launcher_entry": {
            "enabled": False,
        }
    }
