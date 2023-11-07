Image Viewer
============

Demonstrate use of `LiberTEM-panel-ui <https://github.com/LiberTEM/LiberTEM-panel-ui>`_
to build a simple image viewer application.

Development server
------------------

.. code-block:: console

    $ panel serve src/image_viewer/app.py --port 9123 --dev

Notes
-----

- Load directly from file on the server, or external URL, via url-arguments (:code:`?url=`, :code:`?path=`)
- Image reading delegated to :code:`skimage.io.imread` but easy to extend
- Image display downsampling enabled by default above a certain size
- Image toolbox (adjustable color map etc)
- Multi-channel images (stacks) are effectively implemented just need some upstream refactoring
- RGB(A) colour image support is possible, but needs work to have downsampling in this mode
- The page is a normal :code:`Panel` layout so can add text / metadata / more interactivity easily
- The same base could be used for a 4D-STEM viewer or Spectrum viewer
  based on what is already implemented in :code:`LiberTEM-panel-ui`. This is
  a minimal example which only displays a 2D greyscale image.
