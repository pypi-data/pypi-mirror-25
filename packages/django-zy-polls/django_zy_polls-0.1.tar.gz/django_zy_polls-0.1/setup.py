import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
      name='django_zy_polls',
      version='0.1',
      packages=['polls'],
      include_package_data=True,
      license='BSD License',  # example license
      description='A simple Django app to conduct Web-based polls.',
      long_description=README,
      url='http://127.0.0.1:8000/polls/',
      author='Wingdi',
      author_email='lens_z@163.com',
      classifiers=[
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License', # example license
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   # Replace these appropriately if you are stuck on Python 2.
                   'Programming Language :: Python :: 3.5',
                   'Topic :: Internet :: WWW/HTTP',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
                   ],
      )
