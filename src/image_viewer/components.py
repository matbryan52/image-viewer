import pathlib
import importlib
import urllib.parse

import panel as pn
from bokeh.plotting import figure
from skimage.io import imread
from rsciio import IO_PLUGINS
import numpy as np


class LoadException(RuntimeError):
    ...


def default_image() -> tuple[np.ndarray, dict]:
    shape = (480, 640, 5)
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
    if plugin['name'] == 'Image':
        # Simplifies handling of custom RGBA dtype
        return imread(path, as_gray=True), None
    mod = importlib.import_module(plugin['api'])
    result = mod.file_reader(path)
    if isinstance(result, list):
        result = result[0]  # WTF
    return result['data'], result['axes']


def slice_into_channels(data: np.ndarray, axes: list[dict] | None) -> list[np.ndarray]:
    if axes is None or not any(axis['navigate'] for axis in axes):
        yield data
    index_to_axis = {
        axis['index_in_array']: axis
        for axis in axes
    }

    # idea: slice `data` like this: build slicing items like
    # (x, y, :, :)
    # where each non-navigate axis is a `:`, the others are iterated over
    # using `ndindex`

    ndindex_shape = []
    for idx, s in enumerate(data.shape):
        axis = index_to_axis[idx]
        if axis['navigate']:
            ndindex_shape.append(s)

    for idx_tuple in np.ndindex(*tuple(ndindex_shape)):
        idx_lst = list(idx_tuple)
        slice_ = []
        for idx in range(len(index_to_axis)):
            axis = index_to_axis[idx]
            if axis['navigate']:
                slice_.append(idx_lst[0])
                idx_lst = idx_lst[1:]
            else:
                slice_.append(slice(None, None, None))
        yield data[tuple(slice_)]


def load_local(url_hash) -> tuple[np.ndarray, dict]:
    path = extract_uri(url_hash)
    path = urllib.parse.unquote(path)
    path = pathlib.Path(path).expanduser().resolve()
    try:
        array, axes = load_rsciio(path)
        print(f'loaded array of shape {array.shape} dtype {array.dtype}')
    except Exception as e:
        print(e)
        raise
    return list(slice_into_channels(array, axes)), {'path': str(path), 'title': path.name}


def load_url(url_hash) -> tuple[np.ndarray, dict]:
    url = extract_uri(url_hash)
    # scikit-image can read directly from URL to greyscale numpy
    # but it can't handle escaped urls ?
    url = urllib.parse.unquote(url)
    array = imread(url, as_gray=True)
    components = urllib.parse.urlsplit(url)
    title = components.path.split('/')[-1]
    return array, {'url': url, 'title': title}
