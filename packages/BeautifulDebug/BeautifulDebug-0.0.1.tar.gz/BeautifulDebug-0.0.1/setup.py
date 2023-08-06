import codecs
from setuptools import setup
from BeautifulDebug import version

readme = codecs.open('README.md', encoding='utf-8').read()
history = codecs.open('HISTORY.md', encoding='utf-8').read()

setup(
    name='BeautifulDebug',
    version=version,
    description = 'enjoy beautiful debug tools.',
    long_description=u'\n\n'.join([readme, history]),
    author='Xiaojieluo',
    author_email='xiaojieluoff@gmail.com',
    url='https://github.com/xiaojieluo/BeautifulDebug',
    packages=[
        'BeautifulDebug',
    ],
    setup_requires=[
        # minimum version to use environment markers
        'setuptools>=20.6.8',
    ],
    install_requires=[
        # 'colorama;platform_system=="Windows"',
        # 'enum34;python_version<"3.4"',
    ],
    include_package_data=True,
    license='Apache License',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ], )
