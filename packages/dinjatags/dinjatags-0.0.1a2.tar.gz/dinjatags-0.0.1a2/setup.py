from distutils.core import setup
from setuptools import find_packages

setup(
    name = 'dinjatags',
    packages = find_packages('src'),
    package_dir={'': 'src'},
    version = '0.0.1-alpha2',
    description = 'Library for loading Jinja2 Filters and Tags like django tags',
    author='Raymond Joseph Usher Roche',
    author_email = 'rjusher+pypi@gmail.com',
    install_requires=['django', 'jinja2', ],
    url='https://github.com/rjusher/dinjatags',
    download_url = 'https://github.com/rjusher/dinjatags/archive/v0.0.1-alpha1.tar.gz',
    license='BSD',
    keywords = ['django', 'Jinja2'],
    classifiers = [
        "Topic :: Database :: Front-Ends",
        'Programming Language :: Python',
        "Intended Audience :: Developers",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: BSD License',
    ]
    )
