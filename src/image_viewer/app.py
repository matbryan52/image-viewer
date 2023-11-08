from __future__ import annotations

import numpy as np
import panel as pn

from libertem_ui.live_plot import ApertureFigure
from image_viewer.components import (
    load_local, default_image, LoadException, default_image,
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
        'default': default_image,
    }

    if len(pn.state.session_args) == 0:
        accepted = ', '.join("?" + k + "=" for k in supported_load.keys())
        raise LoadException(f'Need load method in URL, accepts one of [``{accepted}``]')

    url_args = {
        k: v for k, v
        in pn.state.session_args.items()
        if k in supported_load.keys()
    }

    if len(url_args) == 0:
        raise LoadException('No compatible load method provided')

    load_method = tuple(url_args.keys())[0]
    try:
        arg = url_args[load_method][0].decode('utf-8')
    except (IndexError, KeyError, UnicodeDecodeError):
        raise LoadException('Invalid URL load format')
    loader = supported_load[load_method]
    return loader(arg)


def display_exception(md_pane: pn.pane.Markdown, exception: Exception):
    md_pane.object = f"""
**{type(exception).__name__}**: {str(exception)}

**URL args**: {pn.state.session_args}
"""


def viewer():
    md = pn.pane.Markdown(object=f"""
**File**: None
""")

    template = pn.template.MaterialTemplate(
        title='Image Viewer',
        collapsed_sidebar=True,
    )
    template.main.append(md)
    fig_col = pn.Column(
        pn.indicators.LoadingSpinner(
            value=True, size=50, color='secondary', name='Loading...'
        )
    )
    template.main.append(fig_col)

    def do_onload():
        try:
            array, meta = load_image()
        except Exception as e:
            fig_col.clear()
            return display_exception(md, e)

        figure = ApertureFigure.new(
            array,
            title=meta.get('title', None),
            channel_dimension=meta.get('channel_dimension', -1),
        )
        md.object = f"""
**File**: {meta.get('path', None)}
"""
        fig_col.clear()
        fig_col.extend(figure.layout.objects)

    pn.state.onload(do_onload)

    return template


viewer().servable(title='Image viewer')
