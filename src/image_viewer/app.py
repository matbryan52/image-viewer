from __future__ import annotations

import numpy as np
import panel as pn

from libertem_ui.live_plot import ApertureFigure
from image_viewer.components import (
    load_local, load_url, LoadException, default_image,
)


def authorize(user_info):
    # Not sure why pn.state.cache puts the key in a tuple and returns a 2-tuple?
    api_token, *_ =  pn.state.cache.get(('api_token',), (None,))
    api_key = pn.state.headers.get('X-Api-Key', None)
    if api_token == api_key:
        # True also if we aren't using token auth (i.e. None == None)
        return True
    return False

pn.config.authorize_callback = authorize


def load_image() -> tuple[np.ndarray, dict]:
    supported_load = {
        'path': load_local,
        'url': load_url,
    }

    # seems to be a bug upstream where true URL hash
    # params is not synced to Python
    url_args = pn.state.session_args

    for key, loader in supported_load.items():
        if key in url_args:
            try:
                arg = url_args[key][0].decode('utf-8')
            except (IndexError, TypeError, UnicodeDecodeError):
                continue
            try:
                return loader(arg)
            except LoadException:
                pass

    return default_image()


def viewer():
    array, meta = load_image()

    header_md = pn.pane.Markdown(object=f"""
**File**: {meta.get('path', None)}
""")

    figure = ApertureFigure.new(
        array,
        title=meta.get('title', None),
        channel_dimension=meta.get('channel_dimension', -1),
    )

    template = pn.template.MaterialTemplate(
        title='Image Viewer',
        collapsed_sidebar=True,
    )
    template.main.append(header_md)
    template.main.append(figure.layout)
    return template


viewer().servable(title='Image viewer')
