#!/usr/bin/env python3

from distutils.core import setup
from distutils import util

embypy_objs = util.convert_path('embypy/objects')
embypy_utils = util.convert_path('embypy/utils')
print(embypy_utils)
setup(name='EmbyPy',
      version='0.1',
      description='Python API wrapper for emby media browser',
      author='Andriy Zasypkin',
      author_email='AndriyZasypkin@gmail.com',
      url='https://github.com/andy29485/embypy',
      package_dir = {
        'embypy': 'embypy',
        'embypy.utils': embypy_utils,
        'embypy.objects': embypy_objs
      },
      install_requires=[
        'aiohttp',
        'asyncio'
        'json',
        'requests',
        'simplejson',
        'ssl',
        'websockets',
      ],
      packages=['embypy', 'embypy.objects', 'embypy.utils'],
)
