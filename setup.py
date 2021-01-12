from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {
    'packages': ["os", "sys", "scikit-image", "pandas", "tkinter"],
    'includes': ["zlib", "codecs", "cmath"],
    'include_files': ["/Users/ftom/Desktop/imagesorter-main/filesorter", "/Users/ftom/Desktop/imagesorter-main/imageslicer", "/Users/ftom/Desktop/imagesorter-main/colorcodes"],
    'excludes': []}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('main.py', base=base, targetName = 'Cutsort')
]

setup(name='Cut&Sort',
      version = '1.0',
      description = 'Cut and sort image files',
      executables = executables)
