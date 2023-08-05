Instructions for submitting a new version of KADMOS to PyPi
===========================================================

- Adapt the version in the setup.py file (for versions that are published to PyPi it should be just something like '0.6', the next intermediate version which is not published would be '0.7dev'.

- Adapt the changelog in the [readme.md](readme.md) file.

- Adapt the [MANIFEST.in](MANIFEST.in) file (this file specifies what should be included in the distribution, by default only .py or .pyc files are included in the distribution). Normally you only need to adapt the included visualization packages here.

- Adapt the [requirements.txt](requirements.txt) file and the setup.py file w.r.t. new dependencies.

- Run the release.bat file (or the three commands from the file in a terminal). This creates a wheel distribution in the [dist](dist) directory which should be installable with pip. Test this out.

- Remove intermediate distributions from the [dist](dist) directory (for example version '0.6dev').

- Submit everything to the master branch of the Bitbucket repository.

- Run the submit.bat file for submitting everything to PyPi. You might want to register your PyPi credentials in the [.pypirc](https://docs.python.org/2/distutils/packageindex.html#pypirc) file first.

- Check that the new version is submitted by accessing [https://pypi.python.org/pypi/kadmos](https://pypi.python.org/pypi/kadmos).
