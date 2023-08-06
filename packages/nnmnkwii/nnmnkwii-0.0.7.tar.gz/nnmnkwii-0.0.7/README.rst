nnmnkwii (nanami)
=================

|image0| |image1| |PyPI| |Build Status| |codecov|

Library to build speech synthesis systems designed for easy and fast
prototyping.

Supported python versions: 2.7 and 3.6.

Documentation
-------------

-  `**STABLE** <https://r9y9.github.io/nnmnkwii/stable>`__ — **most
   recently tagged version of the documentation.**
-  `**LATEST** <https://r9y9.github.io/nnmnkwii/latest>`__ —
   *in-development version of the documentation.*

Installation
------------

The latest release is availabe on pypi. Assuming you have already
``numpy`` installed, you can install nnmnkwii by:

::

    pip install nnmnkwii

If you want the latest development version, run:

::

    pip install git+https://github.com/r9y9/nnmnkwii

or:

::

    git clone https://github.com/r9y9/nnmnkwii
    cd nnmnkwii
    python setup.py develop # or install

This should resolve the package dependencies and install ``nnmnkwii``
property.

At the moment, ``nnmnkwii.autograd`` package depends on
`PyTorch <http://pytorch.org/>`__. If you need autograd features, please
install PyTorch as well.

Acknowledgements
----------------

The library is inspired by the following open source projects:

-  Merlin: https://github.com/CSTR-Edinburgh/merlin
-  Librosa: https://github.com/librosa/librosa

.. |image0| image:: https://img.shields.io/badge/docs-stable-blue.svg
   :target: https://r9y9.github.io/nnmnkwii/stable
.. |image1| image:: https://img.shields.io/badge/docs-latest-blue.svg
   :target: https://r9y9.github.io/nnmnkwii/latest
.. |PyPI| image:: https://img.shields.io/pypi/v/nnmnkwii.svg
   :target: https://pypi.python.org/pypi/nnmnkwii
.. |Build Status| image:: https://travis-ci.org/r9y9/nnmnkwii.svg?branch=master
   :target: https://travis-ci.org/r9y9/nnmnkwii
.. |codecov| image:: https://codecov.io/gh/r9y9/nnmnkwii/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/r9y9/nnmnkwii
