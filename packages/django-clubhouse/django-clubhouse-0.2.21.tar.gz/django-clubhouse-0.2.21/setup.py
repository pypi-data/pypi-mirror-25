# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
from setuptools import setup, find_packages
from shutil import rmtree
from clubhouse import __version__

if sys.argv[:2] == ['setup.py','bdist_wheel']:
    # Remove caches incase of removed project files
    try:
        rmtree('build')
    except:
        pass

try:
    setup(
        name='django-clubhouse',
        version=__version__,
        author='Charles Mead',
        author_email='chazmead89@gmail.com',
        description='An open source content management system build on the '
                    'Django Framework, extending Mezzanine.',
        long_description=open('README.md','rb').read().decode('utf-8'),
        license='BSD',
        url='https://github.com/chazmead/django-clubhouse',
        zip_safe=False,
        include_package_data=True,
        packages=find_packages(),
        install_requires=[
            'grappelli-safe >= 0.4.5, < 0.5.0',
            'filebrowser-safe >= 0.4.6, < 0.5.0',
            'Mezzanine >= 4.2.0, < 4.3.0',
            'django-image-cropping >= 1.1.0, < 1.2.0',
            'easy-thumbnails >= 2.4.1, < 2.5.0'
        ],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Topic :: Internet :: WWW/HTTP',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            'Topic :: Internet :: WWW/HTTP :: WSGI',
            'Topic :: Software Development :: Libraries :: Application Frameworks',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ]
    )
finally:
    pass
