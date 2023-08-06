from argon2 import argon2_hash
import os

"""
    flaskext.argonaut
    ---------------

    A Flask extension providing Argon2 hashing and comparison hash.

    :copyright: (c) 2017 by Anton Oleynick.
    :license: BSD, see LICENSE for more details.
"""

__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)
__author__ = 'Anton Oleynick'
__license__ = 'BSD'
__copyright__ = '(c) 2017 by Anton Oleynick'
__all__ = ['Argonaut', 'generate_salt', 'generate_hash', 'check_hash']


class Argonaut(object):
    def __init__(self, app=None):
        self.salt = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initalizes the application with the extension.
        :param app: The Flask application object.
        """
        self.salt = app.config.get('ARGON_SALT')

    @staticmethod
    def __checker(raw_data, type_check):
        if type_check == 'len':
            if len(str(raw_data)) < 8:
                raise ValueError('Too short Salt, minimal length salt is 8 chars')
        if type_check == 'empty':
            if not raw_data:
                raise ValueError('Empty data import to hashing')

    @staticmethod
    def generate_salt():
        with open('/dev/urandom', 'rb') as f:
            return f.read(20).hex()

    def generate_hash(self, data, salt=None):
        self.__checker(data, 'empty')
        if (not salt) and (not self.salt):
            salt = self.generate_salt()
        elif self.salt:
            self.__checker(self.salt, 'len')
            salt = str(self.salt)
        elif salt:
            self.__checker(salt, 'len')
            salt = str(salt)
        return argon2_hash(data, salt).hex(), salt

    def check_hash(self, hashed_data, data, salt):
        h_d, _ = self.generate_hash(data, salt)
        if hashed_data == h_d:
            return True
        return False
