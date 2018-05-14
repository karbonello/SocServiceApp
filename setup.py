"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup
from glob import glob

APP = ['main.py']
DATA_FILES = [
    ('static/images', glob('static/images/*.jpg')),
    ('static/fonts', glob('static/fonts/*.ttf')),
]


OPTIONS = {'argv_emulation': True,
           'qt_plugins' : "sqldrivers",
           'includes' : ('PyQt5', 'reportlab', 'reportlab.rl_settings', 'pdfgen'),
           'semi_standalone': 'False',
           'compressed' : 'True',
          }

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)