import os
import re
import sys
import shutil

from setuptools import setup, find_packages


def get_version(package):
    """Return package version as listed in `__version__` in `init.py`."""
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()

VERSION = get_version('django_asservio_core')

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (VERSION, VERSION))
    print("  git push --tags")
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree('django_asservio_core.egg-info')
    sys.exit()

setup(
    name='django-asservio-core',
    version=VERSION,
    description='Django general purpose lib used in Asservio.',
    long_description=read('README.rst'),
    url='http://django-asservio-core.readthedocs.org',
    download_url='',
    author='Aleksey, Alexander Osin',
    author_email='quant@apologist.io, alexandre.osin@gmail.com',
    license='Unlicense',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
