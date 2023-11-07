import numpy as np
import panel as pn

from libertem_ui.live_plot import ApertureFigure
from image_viewer.components import (
    load_local, load_url, LoadException, default_image,
)


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
    array, meta = load_image()

    header_md = pn.pane.Markdown(object=f"""
# Image viewer

**File**: {meta.get('path', None)}
""")

    figure = ApertureFigure.new(
        array,
        title=meta.get('title', None),
        channel_dimension=meta.get('channel_dimension', -1),
    )
    return pn.Column(
        header_md,
        figure.layout,
    )


viewer().servable(title='Image viewer')
