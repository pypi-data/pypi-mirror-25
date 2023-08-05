===========
py_tools_ds
===========

A collection of Python tools by Daniel Scheffler.


* Free software: GNU General Public License v3
* Documentation: http://danschef.gitext.gfz-potsdam.de/py_tools_ds/doc/


Status
------

.. .. image:: https://img.shields.io/travis/danschef/py_tools_ds.svg
        :target: https://travis-ci.org/danschef/py_tools_ds

.. .. image:: https://readthedocs.org/projects/py-tools-ds/badge/?version=latest
        :target: https://py-tools-ds.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. .. image:: https://pyup.io/repos/github/danschef/py_tools_ds/shield.svg
     :target: https://pyup.io/repos/github/danschef/py_tools_ds/
     :alt: Updates

.. image:: https://gitext.gfz-potsdam.de/danschef/py_tools_ds/badges/master/build.svg
        :target: https://gitext.gfz-potsdam.de/danschef/py_tools_ds/commits/master
.. image:: https://gitext.gfz-potsdam.de/danschef/py_tools_ds/badges/master/coverage.svg
        :target: http://danschef.gitext.gfz-potsdam.de/py_tools_ds/coverage/
.. image:: https://img.shields.io/pypi/v/py_tools_ds.svg
        :target: https://pypi.python.org/pypi/py_tools_ds

See also the latest coverage_ report and the nosetests_ HTML report.


Features
--------

* TODO


Installation
------------

py_tools_ds depends on some open source packages which are usually installed without problems by the automatic install
routine. However, for some projects, we strongly recommend resolving the dependency before the automatic installer
is run. This approach avoids problems with conflicting versions of the same software.
Using conda_, the recommended approach is:

 .. code-block:: console

    # create virtual environment for py_tools_ds, this is optional
    conda create -y -q --name py_tools_ds python=3
    source activate py_tools_ds
    conda install -y -q -c conda-forge numpy gdal scikit-image pyproj rasterio shapely

* To install py_tools_ds, use the pip installer:

 .. code-block:: console

    pip install py_tools_ds


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _coverage: http://danschef.gitext.gfz-potsdam.de/py_tools_ds/coverage/
.. _nosetests: http://danschef.gitext.gfz-potsdam.de/py_tools_ds/nosetests_reports/nosetests.html
.. _conda: https://conda.io/docs/
