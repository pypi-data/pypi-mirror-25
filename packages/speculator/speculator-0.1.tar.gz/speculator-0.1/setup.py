from setuptools import setup, find_packages
from codecs import open
from os import path

cur_path = path.abspath(path.dirname(__file__))
with open(path.join(cur_path, 'README.md'), encoding='utf-8') as f:
    readme = f.read()

setup(
    name='speculator',
    version='0.1',
    description='Predict next Bitcoin market trends with machine learning and technical analysis',
    long_description=readme,
    url='https://github.com/AllstonMickey/Speculator',
    download_url='https://github.com/AllstonMickey/Speculator/archive/0.1.tar.gz',
    author='Allston Mickey',
    author_email='allston.mickey@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords=[
        'finance',
        'analysis',
        'machine learning',
        'artificial intelligence',
        'bitcoin',
        'ethereum',
        'crypto'
    ],
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'delorean',
        'requests',
        'numpy',
        'scikit-learn',
        'pandas'
    ]
)
