import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='mylibtest',
    version='0.1.1',
    packages=['testapp'],
    description='A line of description',
    long_description=README,
    author='shrawan shinde',
    author_email='syntaxerror1972@gmail.com',
    url='https://upload.pypi.org/legacy/mylibtest_v011/',
    license='MIT',
    install_requires=[
        'Django>=1.6,<1.11.5',
    ]
)