# from distutils.core import setup

from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

setup(
    name='ramdpy',
    version='0.1.0',
    license='BSD',
    description='A Python port of RamdaJS',
    author='Neil Russell',
    author_email='neilrussell6@gmail.com',
    url='https://github.com/neilrussell6/ramdpy',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
)
