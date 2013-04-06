import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allows setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'donation',
    version = '1.0',
    packages = ['donation'],
    include_package_data = True,
    license = 'CC',
    description = 'A simple Django app to collect Web-based donations.',
    long_description = README,
    url = 'http://denigma.de',
    author = 'Hevok',
    author_email = 'hevok@denigma.de',
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Denigma',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: CC License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP : Dynamic Content',
    ]
)