Image Viewer
============

Demonstrate use of `LiberTEM-panel-ui <https://github.com/LiberTEM/LiberTEM-panel-ui>`_
to build a simple image viewer application.

Integrates into Jupyter using
`jupyter-server-proxy <https://github.com/jupyterhub/jupyter-server-proxy>`_.

Launch via Binder with default image:

`<https://mybinder.org/v2/gh/matbryan52/image-viewer/HEAD?urlpath=/image-viewer/app?default=true>`_

.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/matbryan52/image-viewer/HEAD?urlpath=%2Fimage-viewer%2Fapp?default=true


Directly load an image from the :code:`data` directory:

`<https://mybinder.org/v2/gh/matbryan52/image-viewer/HEAD?urlpath=/image-viewer/app?path=./data/logo.png>`_

.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/matbryan52/image-viewer/HEAD?urlpath=/image-viewer/app?path=./data/logo.png


Development server
------------------

.. code-block:: console

    $ panel serve src/image_viewer/app.py --port 9123 --dev

Notes
-----

- Load directly from file on the server, or external URL, via url-arguments (:code:`?url=`, :code:`?path=`)
- Data reading using :code:`rosettasciio`, delegates to :code:`skimage.io.imread` for normal images.
- Multi-channel images (stacks, named channels, 3-D, 4-D data cubes) supported where :code:`rosettasciio`
  generates compatible axis annotations.
- Image display downsampling enabled by default above a certain size
- Image toolbox (adjustable color map etc)
- RGB(A) colour image support is possible, but needs work to have downsampling in this mode
- The page is a normal :code:`Panel` layout so can add text / metadata / more interactivity easily
- The same base could be used for a 4D-STEM viewer or Spectrum viewer
  based on what is already implemented in :code:`LiberTEM-panel-ui`. This is
  a minimal example which only displays a 2D greyscale image.
