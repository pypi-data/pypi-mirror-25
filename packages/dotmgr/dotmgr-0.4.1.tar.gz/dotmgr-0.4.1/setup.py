from distutils.core import setup
from setuptools import find_packages

setup(
    name='dotmgr',
    description='A small script that can help you maintain your dotfiles across several devices',
    keywords=['dotmgr', 'dotfile', 'management'],
    author='Sebastian Neuser',
    author_email='haggl@sineband.de',
    url='https://gitlab.com/haggl/dotmgr',
    license='GPLv3+',
    version='0.4.1',
    install_requires=['gitpython'],
    packages=find_packages(),
    entry_points={
        'console_scripts':[
            'dotmgr = dotmgr.cli:main',
        ]
    },
)
