import re
from setuptools import setup, find_packages

with open('macss_tallies/__init__.py') as f:
    versionString = re.search(r"__version__ = '(.+)'", f.read()).group(1)

setup(name='macss_tallies',
    version = versionString,
    author="Reid McIlroy-Young",
    author_email = "reidmcy@uchicago.edu",
    license = 'GPL',
    url="https://github.com/reidmcy/MACSS-Workshop-Tallies",
    download_url = "https://github.com/reidmcy/MACSS-Workshop-Tallies/archive/{}.tar.gz".format(versionString),
    keywords= 'MACSS',
    classifiers = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Environment :: MacOS X',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Education',
    ],
    install_requires= ['datetime', 'requests'],
    packages = find_packages(),
    entry_points={'console_scripts': [
              'macss_tallies = macss_tallies.main:main',
    ]},
)
