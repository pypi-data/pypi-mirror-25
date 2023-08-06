# this is your project's setup.py script

import os
from distutils.command.register import register as register_orig
from distutils.command.upload import upload as upload_orig

from setuptools import setup


class register(register_orig):

    def _get_rc_file(self):
        return os.path.join('.', '.pypirc')

class upload(upload_orig):

    def _get_rc_file(self):
        return os.path.join('.', '.pypirc')

from distutils.core import setup

setup(
 name = 'FaisalPrintListFunc',
 version = '1.0.0',
 py_modules = ['PrintListFunc'],
 author = 'faianwar',
 author_email = 'faifai@fai.com',
 url = 'http://www.faifai.com',
 description = 'A simple printer of nested lists',
 cmdclass={
        'register': register,
        'upload': upload,
    }
 )
