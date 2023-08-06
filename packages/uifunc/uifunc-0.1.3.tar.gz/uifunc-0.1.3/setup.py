from setuptools import setup

setup(
    name='uifunc',
    version='0.1.3',
    packages=['uifunc'],
    url='https://github.com/Palpatineli/uifunc',
    download_url='https://github.com/Palpatineli/uifunc/archive/0.1.3.tar.gz',
    license='GPLv3',
    author='Keji Li',
    author_email='mail@keji.li',
    extras_require={'wx': ['wx'], 'qt': ['PyQt5']},
    description='convenience functions for opening and saving files/folders',
    classifiers=['Development Status :: 4 - Beta',
                 'Programming Language :: Python :: 3']
)
