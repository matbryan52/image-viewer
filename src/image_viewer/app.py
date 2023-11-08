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
    # True also if we aren't using token auth (i.e. None == None)
    return api_token == api_key

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
    header_md = pn.pane.Markdown(object=f"""
**File**: None
""")

    template = pn.template.MaterialTemplate(
        title='Image Viewer',
        collapsed_sidebar=True,
    )
    template.main.append(header_md)
    fig_col = pn.Column(
        pn.indicators.LoadingSpinner(
            value=True, size=50, color='secondary', name='Loading...'
        )
    )
    template.main.append(fig_col)

    def do_onload():
        array, meta = load_image()

        figure = ApertureFigure.new(
            array,
            title=meta.get('title', None),
            channel_dimension=meta.get('channel_dimension', -1),
        )
        header_md.object = f"""
**File**: {meta.get('path', None)}
"""
        fig_col.clear()
        fig_col.extend(figure.layout.objects)

    pn.state.onload(do_onload)

    return template


viewer().servable(title='Image viewer')
