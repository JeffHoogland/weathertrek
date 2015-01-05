# Run the build process by running the command 'python setupwin.py build'

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': 'atexit'
    }
}

executables = [
    Executable('weathertrek.py', base=base)
]

setup(name='Weather Trek',
      version='0.2',
      description='Weather for traveling',
      options=options,
      executables=executables
      )
