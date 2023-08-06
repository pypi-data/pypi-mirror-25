
scipy-sugar
===========

|PyPI-Status| |Conda-Forge-Status| |Conda-Downloads|

|Build-Status| |Codacy-Grade| |License-Badge| |Doc-Status|

Missing SciPy functionalities.

Install
-------

The recommended way of installing it is via conda_

.. code:: bash

    conda install -c conda-forge scipy-sugar

An alternative way would be via pip_

.. code:: bash

    pip install scipy-sugar

Running the tests
-----------------

After installation, you can test it

.. code:: bash

    python -c "import scipy_sugar; scipy_sugar.test()"

as long as you have pytest_.

Authors
-------

* `Danilo Horta`_

License
-------

This project is licensed under the MIT License - see the `License file`_ for
details.

.. |Build-Status| image:: https://travis-ci.org/limix/scipy-sugar.svg?branch=master
    :target: https://travis-ci.org/limix/scipy-sugar

.. |Codacy-Grade| image:: https://api.codacy.com/project/badge/Grade/279d016293724b79ad8e667c1440d3d0
    :target: https://www.codacy.com/app/danilo.horta/scipy-sugar?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=limix/scipy-sugar&amp;utm_campaign=Badge_Grade

.. |PyPI-Status| image:: https://img.shields.io/pypi/v/scipy-sugar.svg
    :target: https://pypi.python.org/pypi/scipy-sugar

.. |PyPI-Versions| image:: https://img.shields.io/pypi/pyversions/scipy-sugar.svg
    :target: https://pypi.python.org/pypi/scipy-sugar

.. |Conda-Forge-Status| image:: https://anaconda.org/conda-forge/scipy-sugar/badges/version.svg
    :target: https://anaconda.org/conda-forge/scipy-sugar

.. |Conda-Downloads| image:: https://anaconda.org/conda-forge/scipy-sugar/badges/downloads.svg
    :target: https://anaconda.org/conda-forge/scipy-sugar

.. |License-Badge| image:: https://img.shields.io/pypi/l/scipy-sugar.svg
    :target: https://raw.githubusercontent.com/limix/scipy-sugar/master/LICENSE.txt

.. |Doc-Status| image:: https://readthedocs.org/projects/scipy-sugar/badge/?style=flat-square&version=stable
    :target: https://scipy-sugar.readthedocs.io/

.. _License file: https://raw.githubusercontent.com/limix/scipy-sugar/master/LICENSE.txt

.. _Danilo Horta: https://github.com/horta

.. _conda: http://conda.pydata.org/docs/index.html

.. _pip: https://pypi.python.org/pypi/pip

.. _pytest: http://docs.pytest.org/en/latest/
