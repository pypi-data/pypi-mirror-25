# from distutils.core import setup
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='exif2timestream-v2',
    version='0.9.2',
    python_requires='>=3.2',
    packages=['libexif2timestream2', 'exif2timestream_scripts'],
    url='https://borevitzlab.github.io/exif2timestream/',
    license='GPLv3',
    author='Gareth Dunstone, Borevitz Lab, Australian Plant Phenomics Facility, TimeScience',
    author_email='appf@anu.edu.au',
    description='A tool to turn unstructured timelapses into nested directory trees with downsampled images based on exif data.',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3 :: Only"
    ],
    keywords=['timelapse', 'imaging'],
    entry_points={
        'console_scripts': [
            'exif2timestream-batch = exif2timestream_scripts.exif2timestream_batch:main',
            'exif2timestream-cli = exif2timestream_scripts.exif2timestream_cli:main'
        ]
    },
    install_requires=requirements
)
