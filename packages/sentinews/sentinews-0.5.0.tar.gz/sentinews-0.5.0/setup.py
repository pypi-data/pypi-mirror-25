# coding: utf-8
import os
import sys
import subprocess
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup
    from distutils.util import convert_path


def _find_packages(where='.', exclude=()):
    """Return a list all Python packages found within directory 'where'
        'where' should be supplied as a "cross-platform" (i.e. URL-style)
        path; it will be converted to the appropriate local path syntax.
        'exclude' is a sequence of package names to exclude; '*' can be used
        as a wildcard in the names, such that 'foo.*' will exclude all
        subpackages of 'foo' (but not 'foo' itself).
        """
    out = []
    stack = [(convert_path(where), '')]
    while stack:
        where, prefix = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if ('.' not in name and os.path.isdir(fn) and
                    os.path.isfile(os.path.join(fn, '__init__.py'))):
                out.append(prefix + name)
                stack.append((fn, prefix + name + '.'))
    for pat in list(exclude) + ['ez_setup', 'distribute_setup']:
        from fnmatch import fnmatchcase
        out = [item for item in out if not fnmatchcase(item, pat)]


def loadRequirement():
    '''
    自动加载requirements.txt配置的依赖包
    :return:
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    requires = open(os.path.join(path, 'requirements.txt'), 'r').readlines()

    return [req.strip('\n') for req in requires]


PUBLISH_CMD = 'python setup.py register sdist upload'

if 'publish' in sys.argv:
    status = subprocess.call(PUBLISH_CMD, shell=True)
    sys.exit(status)

setup(
    name="sentinews",
    version="0.5.0",
    author="Liujie zhang",
    author_email='liujiezhangbupt@gmail.com',
    description="sentiment classifier for news trained by LSTM.",
    keywords=['sentiment', 'LSTM'],
    license="MIT",
    install_requires=[
        "h5py>=2.7",
        "tensorflow==1.2.1",
        "jieba>=0.38",
        "Keras==2.0.6",
        "scikit_learn>=0.18",
        "PyYAML>=3.0",
    ],
    url="https://github.com/KillersDeath/the_machine",
    packages=find_packages(exclude=('test*', )),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        "Programming Language :: Python :: 3.5",
    ],
    include_package_data=True
    )
