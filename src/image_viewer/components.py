import pathlib
import importlib
import urllib.parse

import panel as pn
from bokeh.plotting import figure
from skimage.io import imread
from rsciio import IO_PLUGINS
import numpy as np

from libertem_ui.display.image_db import BokehImage
from libertem_ui.live_plot import adapt_figure, AperturePlot


class LoadException(RuntimeError):
    ...


def default_image() -> tuple[np.ndarray, dict]:
    shape = (480, 640)
    return (
        np.random.uniform(size=shape).astype(np.float32),
        {'title': 'Default image'},
    )


def extract_uri(url_hash):
    # token auth key breaks path inference
    # when launching via binder this is appended
    # to the URL path so we can split using *_
    path, *_ = url_hash.split('&token=')
    path_parts = path.split('=')
    return '='.join(path_parts[1:])


def plugin_def_for_path(path: pathlib.Path):
    ext = path.suffix[1:]
    for plugin in IO_PLUGINS:
        if ext in plugin['file_extensions']:
            return plugin
    raise LoadException(f"unknown file extension: {ext}")


def load_rsciio(path: pathlib.Path):
    print(f"loading from {path}")
    plugin = plugin_def_for_path(path)
    mod = importlib.import_module(plugin['api'])
    result = mod.file_reader(path)
    print(f"{mod}")
    if isinstance(result, list):
        result = result[0]  # WTF
    return result['data']


def load_local(url_hash) -> tuple[np.ndarray, dict]:
    path = extract_uri(url_hash)
    path = urllib.parse.unquote(path)
    path = pathlib.Path(path).expanduser().resolve()
    try:
        array = load_rsciio(path)
    except Exception as e:
        print(e)
        raise
    # array = imread(path, as_gray=True)
    return array, {'path': str(path), 'title': path.name}


def load_url(url_hash) -> tuple[np.ndarray, dict]:
    url = extract_uri(url_hash)
    # scikit-image can read directly from URL to greyscale numpy
    # but it can't handle escaped urls ?
    url = urllib.parse.unquote(url)
    array = imread(url, as_gray=True)
    components = urllib.parse.urlsplit(url)
    title = components.path.split('/')[-1]
    return array, {'url': url, 'title': title}


class ApertureFigure:
    def __init__(self, fig, im):
        """
        Minimal version of AperturePlot from LiberTEM-panel-ui
        without components necessary to be compatible with the LivePlot2D
        interface. With some refactoring upstream this class would
        no longer be necessary. It mostly adds the toolbar (hidden) and
        the methods to add the control panel / hover text
        """
        self._fig = fig
        self._im = im
        self._pane = pn.pane.Bokeh(fig)
        self._toolbar = pn.Row(
            height=1,
            margin=(0, 0)
        )
        self._layout = pn.Column(
            self._toolbar,
            self._pane,
            margin=(0, 0),
        )

    @classmethod
    def new(cls, array: np.ndarray, title=None):
        fig = figure()
        if title is not None:
            fig.title.text = title
        img = (
            BokehImage
            .new()
            .from_numpy(array)
        )
        img.on(fig)
        img.enable_downsampling()
        adapt_figure(fig, array.shape, maxdim=600)
        return ApertureFigure(fig, img)

    @property
    def fig(self) -> figure | None:
        return self._fig

    @property
    def im(self) -> BokehImage | None:
        return self._im

    @property
    def layout(self) -> pn.Column:
        return self._layout

    def add_hover_position_text(self):
        return AperturePlot.add_hover_position_text(self)

    def add_control_panel(
        self,
        name: str = 'Image Controls',
    ):
        return AperturePlot.add_control_panel(self, name=name)
