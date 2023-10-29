Image Viewer
============

Demonstrate use of `LiberTEM-panel-ui <https://github.com/LiberTEM/LiberTEM-panel-ui>`_
to build a simple image viewer application.

Integrates into Jupyter using
`jupyter-server-proxy <https://github.com/jupyterhub/jupyter-server-proxy>`_.

Launch via Binder with default image:

`<https://mybinder.org/v2/gh/matbryan52/image-viewer/HEAD?urlpath=/image-viewer/app>`_

.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/matbryan52/image-viewer/HEAD?urlpath=%2Fimage-viewer%2Fapp


Directly load an image from the :code:`data` directory:

`<https://mybinder.org/v2/gh/matbryan52/image-viewer/HEAD?urlpath=/image-viewer/app?path=./data/logo.png>`_

.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/matbryan52/image-viewer/HEAD?urlpath=/image-viewer/app?path=./data/logo.png


Directly load an image from an URL:

`<https://mybinder.org/v2/gh/matbryan52/image-viewer/HEAD?urlpath=/image-viewer/app?url=https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/RedCat_8727.jpg/1200px-RedCat_8727.jpg>`_

.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/matbryan52/image-viewer/HEAD?urlpath=/image-viewer/app?url=https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/RedCat_8727.jpg/1200px-RedCat_8727.jpg


Notes
-----

- Load directly from file on the server, or URL
- Image downsampling enabled by default above a certain size
- Image toolbox (adjustable color map etc)
- Multi-channel images (stacks) are effectively implemented just need some upstream refactoring
- RGB(A) colour image support is possible, but needs work to have downsampling in this mode
- The page is a normal :code:`Panel` layout so can add text / metadata / more interactivity easily
- The same base could be used for a 4D-STEM viewer or Spectrum viewer
  based on what is already implemented in :code:`LiberTEM-panel-ui`. This is
  a minimal example which only displays a 2D greyscale image.
