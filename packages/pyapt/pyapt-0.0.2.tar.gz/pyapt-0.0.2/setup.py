import setuptools

import sys
if not sys.version_info[0] == 3:
    sys.exit("Sorry, only python version 3 is supported")

setuptools.setup(
    name='pyapt',
    version='0.0.2',
    description='module to help you maintain third party apt repos in a sane way',
    long_description='module to help you maintain third party apt repos in a sane way',
    url='https://veltzer.github.io/pyapt',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='pyapt apt apt-key',
    packages=setuptools.find_packages(),
    install_requires=[
        'pylogconf',  # for logging configuration
        'click',  # used for command line parsing
    ],
    entry_points={
        'console_scripts': [
            'pyapt_update=pyapt.scripts.update:main',
        ],
    },
)
