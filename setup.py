import setuptools

# Using setup.py to support the auto-registration of
# jupyter_serverproxy_servers entrypoints, seemingly not
# supported with pyproject.toml

setuptools.setup(
    name="image_viewer",
    version="0.0.1",
    license="LICENSE",
    repository="https://github.com/matbryan52/image-viewer",
    where='src',
    entry_points={
        "jupyter_serverproxy_servers": [
            "image-viewer = image_viewer:setup_proxy_config",
        ]
    },
    install_requires=[
        "libertem_ui@git+https://github.com/LiberTEM/LiberTEM-panel-ui",
        "panel",
        "bokeh",
        "rosettasciio",
    ],
)
