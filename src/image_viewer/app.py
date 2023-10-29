import numpy as np
import panel as pn
from bokeh.plotting import figure

from libertem_ui.display.image_db import BokehImage
from libertem_ui.live_plot import adapt_figure


def viewer():
    header_md = pn.pane.Markdown(object="""
# Image viewer""")

    shape = (480, 640)
    fig = figure()
    img = (
        BokehImage
        .new()
        .from_numpy(np.random.uniform(size=shape).astype(np.float32))
    )
    img.on(fig)
    adapt_figure(fig, shape, maxdim=600)

    return pn.Column(
        header_md,
        pn.pane.Bokeh(fig),
    )


viewer().servable()
