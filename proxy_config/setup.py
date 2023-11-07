import setuptools

# Using setup.py to support the auto-registration of
# jupyter_serverproxy_servers entrypoints, seemingly not
# supported with pyproject.toml

setuptools.setup(
    name="image-viewer-proxy",
    version="0.0.1",
    license="MIT",
    repository="https://github.com/matbryan52/image-viewer",
    where='src',
    dependencies=[
        'jupyter-server-proxy'
    ],
    entry_points={
        "jupyter_serverproxy_servers": [
            "image-viewer = image_viewer_proxy:setup_proxy_config",
        ]
    },
)

