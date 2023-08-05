MIT License

Copyright (c) 2017, Floyd Hightower

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


Description: ===============================
        XN-Twist Python SDK
        ===============================
        
        .. image:: https://img.shields.io/pypi/v/xn-twist-python-sdk.svg
                :target: https://pypi.python.org/pypi/xn-twist-python-sdk
        
        .. image:: https://img.shields.io/travis/xn-twist/xn-twist-python-sdk.svg
                :target: https://travis-ci.org/xn-twist/xn-twist-python-sdk
        
        .. image:: https://api.codacy.com/project/badge/Grade/6927955d30df40f395aa8adbd7b8bfe4
                :alt: Codacy Badge
                :target: https://www.codacy.com/app/fhightower/xn-twist-python-sdk
         
        .. image:: https://codecov.io/gh/xn-twist/xn-twist-python-sdk/branch/master/graph/badge.svg
                :target: https://codecov.io/gh/xn-twist/xn-twist-python-sdk
        
        .. image:: https://readthedocs.org/projects/xn-twist-python-sdk/badge/?version=latest
                :target: https://xn-twist-python-sdk.readthedocs.io/en/latest/?badge=latest
                :alt: Documentation Status
        
        .. image:: https://pyup.io/repos/github/xn-twist/xn-twist-python-sdk/shield.svg
             :target: https://pyup.io/repos/github/xn-twist/xn-twist-python-sdk/
             :alt: Updates
        
        Python SDK for talking with `XN-Twist's API <https://github.com/xn-twist/xn-twist-api>`_ . **Note:** this package is not designed to be your primary interaction with the XN-Twist API. This is simply a package to aid the management of the API and is used behind the scenes in the `xn-twist package <https://github.com/xn-twist/xn-twist>`_.
        
        Installation
        ------------
        
        Stable release
        ++++++++++++++
        
        To install the XN-Twist Python SDK, run this command in your terminal:
        
        .. code-block:: console
        
            $ pip install xn_twist_python_sdk
        
        This is the preferred method to install the XN-Twist Python SDK, as it will always install the most recent stable release. 
        
        If you don't have `pip`_ installed, this `Python installation guide`_ can guide
        you through the process.
        
        .. _pip: https://pip.pypa.io
        .. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
        
        From sources
        ++++++++++++
        
        The sources for the XN-Twist Python SDK can be downloaded from the `Github repo`_.
        
        You can either clone the public repository:
        
        .. code-block:: console
        
            $ git clone git://github.com/xn-twist/xn-twist-python-sdk
        
        Or download the `tarball`_:
        
        .. code-block:: console
        
            $ curl  -OL https://github.com/xn-twist/xn-twist-python-sdk/tarball/master
        
        Once you have a copy of the source, you can install it with:
        
        .. code-block:: console
        
            $ python setup.py install
        
        
        .. _Github repo: https://github.com/xn-twist/xn-twist-python-sdk
        .. _tarball: https://github.com/xn-twist/xn-twist-python-sdk/tarball/master
        
        Usage
        -----
        
        .. code-block:: python
        
            from xn_twist_python_sdk import xn_twist_python
        
            # instantiate an instance of the XN-Twist Python SDK
            xn_sdk = xn_twist_python.XnTwistSDK()
        
        Credits
        -------
        
        This package was created with Cookiecutter_ and the `fhightower/python-project-template`_ project template.
        
        .. _Cookiecutter: https://github.com/audreyr/cookiecutter
        .. _`xn-twist/python-project-template`: https://github.com/fhightower/python-project-template
        
        
        =======
        History
        =======
        
        1.0.0 (2017-06-24)
        ------------------
        
        * First release on PyPI.
        
        0.1.0 - 0.2.1 (2017-06)
        ------------------
        
        * Initial development
Keywords: xn_twist_python_sdk
Platform: UNKNOWN
Classifier: Development Status :: 2 - Pre-Alpha
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: MIT License
Classifier: Natural Language :: English
Classifier: Programming Language :: Python :: 2
Classifier: Programming Language :: Python :: 2.6
Classifier: Programming Language :: Python :: 2.7
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.3
Classifier: Programming Language :: Python :: 3.4
Classifier: Programming Language :: Python :: 3.5
