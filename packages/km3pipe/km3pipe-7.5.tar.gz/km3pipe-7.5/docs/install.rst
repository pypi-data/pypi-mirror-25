Installation
============


.. contents:: :local:


Important Note for Users of the CC-IN3P3 in Lyon
------------------------------------------------

KM3Pipe is preinstalled on the Lyon computing centre. Put this into your
`~/.bashrc` or `~/.zshenv` (or whatever login script you prefer):::

    source /afs/in2p3.fr/throng/km3net/src/python/pyenv.sh

And you are ready to go!
The Python environment also contains all important and commonly used scientific
packages like scipy, numpy, scikit-learn, pandas etc.

Requirements
------------

To install km3pipe, you need:

- Python >= 2.7 or >= 3.4

- pip (via ``$ easy_install pip``)

- C compiler, e.g. ``gcc``.

- HDF5 (the hdf5lib C library, e.g. `apt-get install hdf5`)

(Recommended) Virtual Environments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you're not using a virtual environment (https://virtualenvwrapper.readthedocs.io), you can install it in your own home directory: ``pip install --user ...```, however I recommend using virtual environments for any Python related stuff.


Install
-------


To install the latest stable version:::

    $ pip install km3pipe

To get the development version, use:::

    $ pip install git+http://git.km3net.de/km3py/km3pipe.git@develop


Updating
--------

KM3Pipe comes with a command line utility called `km3pipe`, which can
be used to update KM3Pipe itself::

    $ km3pipe update

To get the latest developer version::

    $ km3pipe update develop

Or you can of course use `pip`::

    $ pip install --upgrade km3pipe


Configuration
-------------

KM3Pipe can read frequently used information (like DB session cookies,
API tokens, etc.) from a configuration file, which is expected to
be `~/.km3net`.

Here is an example configuration::

    [General]
    check_for_updates=no

    [DB]
    cookie=sid_fooman_123.34.56.78_

    [Slack]
    token=xoxp-2355837568-2397897846-8945924372-395f023485
