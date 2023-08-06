dtgui
=====

.. image:: https://img.shields.io/pypi/v/dtgui.svg
    :target: https://pypi.python.org/pypi/dtgui
    :alt: PyPI Version

dtgui is a graphical user interface for interactively testing a baseline-removal algorithm based on the dual-tree complex wavelet transform
published in the following article:

    .. [#] L. P. René de Cotret and B. J. Siwick, A general method for baseline-removal in ultrafast 
           electron powder diffraction data using the dual-tree complex wavelet transform, Struct. Dyn. 4 (2017) DOI: 10.1063/1.4972518.

The underlying function is `documented in its original package <http://scikit-ued.readthedocs.io/en/release/functions/skued.baseline_dt.html#skued.baseline_dt>`_.

Installation
------------

Other than the pip-installable requirements, dtgui requires PyQt5 to be installed.

Usage
-----

Once installed, the GUI can be started using the following command:

    python -m dtgui

Support / Report Issues
-----------------------

All support requests and issue reports should be
`filed on Github as an issue <https://github.com/LaurentRDC/dtgui/issues>`_.

License
-------

dtgui is made available under the MIT License. For more details, see `LICENSE.txt <https://github.com/LaurentRDC/dtgui/blob/master/LICENSE.txt>`_.
