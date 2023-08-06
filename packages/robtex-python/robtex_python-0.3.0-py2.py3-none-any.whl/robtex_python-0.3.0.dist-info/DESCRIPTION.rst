MIT License

Copyright (c) 2017, Floyd Hightower

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


Description: *******************************
        Robtex Python
        *******************************
        
        
        .. image:: https://img.shields.io/pypi/v/robtex_python.svg
                :target: https://pypi.python.org/pypi/robtex_python
        
        .. image:: https://img.shields.io/travis/fhightower/robtex-python.svg
                :target: https://travis-ci.org/fhightower/robtex-python
        
        .. image:: https://codecov.io/gh/fhightower/robtex-python/branch/master/graph/badge.svg
                :target: https://codecov.io/gh/fhightower/robtex-python
        
        .. image:: https://api.codacy.com/project/badge/Grade/8151c710cd704ddeb8575ee6dfbbd96e
                :target: https://www.codacy.com/app/fhightower/robtex-python
        
        .. image:: https://readthedocs.org/projects/robtex-python/badge/?version=latest
                :target: http://robtex-python.readthedocs.io/en/latest/?badge=latest
                :alt: Documentation Status
        
        Simple python wrapper for the `Robtex API <https://www.robtex.com/api/>`_ . This project is currently **under development**. Feel free to contribute and don't forget to add yourself to the `AUTHORS.rst <https://github.com/fhightower/robtex-python/blob/master/AUTHORS.rst>`_ file!
        
        * Free software: MIT license
        * Documentation: https://robtex-python.readthedocs.io
        
        Installation
        ============
        
        Stable release
        --------------
        
        To install Robtex Python, run this command in your terminal:
        
        .. code-block:: console
        
            pip install robtex-python
        
        This is the preferred method to install the Robtex API wrapper, as it will always install the most recent stable release. 
        
        If you don't have `pip`_ installed, this `Python installation guide`_ can guide
        you through the process.
        
        .. _pip: https://pip.pypa.io
        .. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
        
        From sources
        ------------
        
        The sources for Robtex Python can be downloaded from the `Github repo`_.
        
        You can either clone the public repository:
        
        .. code-block:: console
        
            $ git clone git://github.com/fhightower/robtex-python
        
        Or download the `tarball`_:
        
        .. code-block:: console
        
            $ curl  -OL https://github.com/fhightower/robtex-python/tarball/master
        
        Once you have a copy of the source, you can install it with:
        
        .. code-block:: console
        
            $ python3 setup.py install
        
        .. _Github repo: https://github.com/fhightower/robtex-python
        .. _tarball: https://github.com/fhightower/robtex-python/tarball/master
        
        Usage
        =====
        
        Via Python
        ----------
        
        You can use Robtex Python in a script as follows:
        
        .. code-block:: python
        
            from robtex_python import robtex_python
            response = robtex_python.pdns_forward("example.com")
        
        Via Command Line
        ----------------
        
        You can use Robtex Python as a command-line tool as follows:
        
        .. code-block:: shell
        
            Usage:
                robtex_python --ip=<ip>
                robtex_python --as=<asn>
                robtex_python --pdns-forward=<hostname>
                robtex_python --pdns-reverse=<ip>
                robtex_python (-h | --help)
                robtex_python --version
        
        Credits
        =======
        
        This package was created with Cookiecutter_ and the `fhightower/python-project-template`_ project template.
        
        .. _Cookiecutter: https://github.com/audreyr/cookiecutter
        .. _`fhightower/python-project-template`: https://github.com/fhightower/python-project-template
        
        
        *******
        History
        *******
        
        0.1.0 (2017-09-19)
        ==============================================
        
        * First release on PyPI.
        
Keywords: robtex
Platform: UNKNOWN
Classifier: Development Status :: 4 - Beta
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: MIT License
Classifier: Natural Language :: English
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.3
Classifier: Programming Language :: Python :: 3.4
Classifier: Programming Language :: Python :: 3.5
