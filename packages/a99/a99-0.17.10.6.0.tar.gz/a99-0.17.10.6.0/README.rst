a99
===

A multi-purpose API in Python

Some features
-------------

GUI development (PyQt5):

- Widgets
- Windows
- Python syntax highlighter
- Window placement in desktop
- Widget formatting

Miscellanea:

- Subclass of `configobj.ConfigObj`
- Work with SQLite3 databases
- Introspection
- Logging
- Matplotlib
- Text interface
- Many conversion routines
- File I/O
- Searches
- Random person name generator


Installation
------------

Requirements
~~~~~~~~~~~~

- Python 3.xx

Mandatory packages:

- numpy
- configobj

Optional packages (will have limited funcionality without them):

- matplotlib
- pyqt5
- astropy

Install
~~~~~~~

Method 1 (prefer _pip_, use _apt_ package as alternative)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: shell

   sudo pip3 install numpy configobj matplotlib pyqt5 astropy a99

If _PyQt5_ fails to install with _pip_:

.. code:: shell

   sudo apt-get install python3-PyQt5

Method 2 (prefer _apt_, use _pip_ if no _apt_ package available)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: shell

   sudo apt-get install python3-matplotlib python3-numpy python3-PyQt5 python3-astropy python3-pip
   sudo pip3 install configobj a99

Method 3 (virtual environment with _conda_)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This may be an alternative if you want to work with a separate installation of Python and related packages.
Here you need to have _Anaconda_ or _Miniconda_ installed.

Create a new virtual environment called "astroenv" (or any name you like):

.. code:: shell

   conda create --name astroenv python=3.5

Activate this new virtual environment:

.. code:: shell

   source activate astroenv

Now you should be able to install _f311_ from _pip_:

.. code:: shell

   sudo pip install numpy configobj matplotlib pyqt5 astropy a99

**Note** Every time you want to work with _f311_, you will need to activate the environment:

.. code:: shell

   source activate astroenv

To deactivate the environment:

.. code:: shell

   source deactivate

Method 4 (development mode)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Clone repository:

.. code:: shell

   git clone ssh://git@github.com/trevisanj/a99.git

or

.. code:: shell

   git clone http://github.com/trevisanj/a99

Install in **developer** mode:

.. code:: shell

   cd a99
   sudo python3 setup.py develop
