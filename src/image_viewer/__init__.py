import pathlib
app_file = pathlib.Path(__file__).parent / 'app.py'


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
