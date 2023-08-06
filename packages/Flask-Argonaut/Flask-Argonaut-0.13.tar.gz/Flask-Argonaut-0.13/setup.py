"""
    Flask-Argonaut
    ------------
    Argon hashing for your Flask.

"""
from setuptools import setup

setup(name='Flask-Argonaut',
      version='0.13',
      description='Flask extension use hashing data with Argon2',
      author='Anton Oleynik',
      author_email='levantado@me.com',
      license='BSD',
      packages=['flask_argonaut'],
      platforms='any',
      install_requires=['Flask', 'argon2'],
      zip_safe=False)
