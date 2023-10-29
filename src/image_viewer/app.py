import pathlib
import urllib.parse

import numpy as np
import panel as pn
from bokeh.plotting import figure
from skimage.io import imread

from libertem_ui.display.image_db import BokehImage
from libertem_ui.live_plot import adapt_figure


class LoadException(RuntimeError):
    ...


def default_image() -> tuple[np.ndarray, dict]:
    shape = (480, 640)
    return (
        np.random.uniform(size=shape).astype(np.float32),
        {'info': 'Default image'},
    )


def load_local(url_hash) -> tuple[np.ndarray, dict]:
    # token auth key breaks path inference
    # when launching via binder this is appended
    # to the URL path so we can split using *_
    path, *_ = url_hash.split('&token=')
    path_parts = path.split('=')
    path = '='.join(path_parts[1:])
    path = urllib.parse.unquote(path)
    path = pathlib.Path(path).expanduser().resolve()
    array = imread(path, as_gray=True)
    return array, {'info': str(path)}


def load_url(url_hash) -> tuple[np.ndarray, dict]:
    raise load_local(url_hash)


def load_image() -> tuple[np.ndarray, dict]:
    supported_load = {
        '?path=': load_local,
        '?url=': load_url,
    }

    # seems to be a bug upstream where true URL hash
    # params is not synced to Python
    url_hash = pn.state.location.search

    if not isinstance(url_hash, str):
        return default_image()

    for key, loader in supported_load.items():
        if url_hash.startswith(key):
            try:
                return loader(url_hash)
            except LoadException:
                pass

    return default_image()


def viewer():
    header_md = pn.pane.Markdown(object="""
# Image viewer""")

    array, _ = load_image()
    fig = figure()
    img = (
        BokehImage
        .new()
        .from_numpy(array)
    )
    img.on(fig)
    adapt_figure(fig, array.shape, maxdim=600)

    return pn.Column(
        header_md,
        pn.pane.Bokeh(fig),
    )


viewer().servable()
