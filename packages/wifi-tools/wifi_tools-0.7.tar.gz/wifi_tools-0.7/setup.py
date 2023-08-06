#!/usr/bin/env python
# -*- coding: utf-8 -*-
import platform

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'dpkt',
    'pypcap',
    'pybluez',
    'tqdm',
    'scapy-python3',
    'redis',
    'sqlalchemy',
    'SpoofMAC',
    'netifaces',
    'requests',
    'netaddr',
    'lcubo_helpers',
    'pyrcrack',
    'python3-wifi',
    'nosexcover',
    'python-dateutil',
    #'pyiw',
    'python-nmap',
    'multiprocessing-logging',
    'gpsd-py3',
    'pygpio',
    'RPi.GPIO',
    'char_lcd',
    'Adafruit_GPIO',
    'Pillow',
    'pypcap',
    'raspjack'
]

try:
    platform.mac_ver()
except Exception:
    platform.linux_distribution()
    requirements.append('iwlib')
except Exception:
    raise Exception('Platform not yet supported')

test_requirements = [
    'nose',
    'mock',
    'fakeredis',
    'coverage',
    'pytest',
]

setup(
    name='wifi_tools',
    version='0.7',
    description="Wifi python scripts for raspberry pi wardriving. Supports wifi, bluetooth, nrf24",
    long_description=readme + '\n\n' + history,
    author="llazzaro",
    author_email='llazzaro@dc.uba.ar',
    url='https://github.com/pepe/wifi_tools',
    dependency_links=[
        'git+https://github.com/cmheisel/nose-xcover.git#egg=nosexcover',
        'git+https://github.com/kelleyk/py3k-netifaces.git#egg=netifaces',
        'git+https://github.com/llazzaro/pyrcrack.git#egg=pyrcrack',
        'git+https://github.com/llazzaro/python3-wifi.git#egg=python3-wifi',
        'git+https://github.com/jruere/multiprocessing-logging.git#egg=multiprocessing_logging',
        'git+https://github.com/DigitalSecurity/raspjack.git#egg=raspjack'
    ],
    packages=find_packages(),
    package_dir={'wifi_tools':
                 'wifi_tools'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='wifi_tools',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={'console_scripts': [
        'manage = wifi_tools.scripts.manage:main',
        'init_db = wifi_tools.scripts.init_db:main',
        'import_wigle = wifi_tools.scripts.import_wigle:main',
        'generate_kml = wifi_tools.scripts.generate_kml:main',
    ]}
)
