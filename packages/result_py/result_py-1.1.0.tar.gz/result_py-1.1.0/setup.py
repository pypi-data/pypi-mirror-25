'''setup.py
'''

from distutils.core import setup

setup(
    name='result_py',
    packages=['result_py'],
    version='1.1.0',
    description='A Result type much like Rust\'s, featuring generics and lovely combinators.',
    author='Zack Mullaly',
    author_email='zsck@riseup.net',
    url='https://github.com/zsck/result_py',
    download_url='https://github.com/zsck/result_py/archive/1.1.0.tar.gz',
    keywords=[
        'rust',
        'result',
        'generics',
        'type hinting',
        'error handling',
        'combinators',
        'functional programming'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
