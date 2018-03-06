# PyTicTacToe
Tic Tac Toe written in Python. First attempt at using PySDL2.

For Ubuntu
==========

sudo apt-get install libsdl2-2.0-0 libsdl2-dev python python-pip
sudo pip install libsdl2

For Windows
===========

1. Download and install PySDL2
   1. https://pypi.python.org/pypi/PySDL2
   2. Unpack archive
   3. $ python setup.py install # in the unpacked directory; its not necessary to set the PYTHONPATH and PYTHON env vars using this method
2. Download SDL2 binaries
   * https://www.libsdl.org/release/SDL2-2.0.8-win32-x64.zip
3. In CMD $ set PYSDL2_DLL_PATH=<SDL2.dll_DIR>
