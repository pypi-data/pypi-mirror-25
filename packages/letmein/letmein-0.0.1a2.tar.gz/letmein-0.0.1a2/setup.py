from distutils.core import setup
from setuptools import find_packages

setup(
    name = 'letmein',
    packages = find_packages('src'),
    package_dir={'': 'src'},
    version = '0.0.1-alpha2',
    description = 'Drop in replacement for django.contrib.auth in a modelchemy context',
    author='Raymond Joseph Usher Roche',
    author_email = 'rjusher+pypi@gmail.com',
    install_requires=['django', 'sqlalchemy'],
    url='https://github.com/rjusher/letmein',
    download_url = 'https://github.com/rjusher/letmein/archive/v0.0.1-alpha1.tar.gz',
    license='BSD',
    keywords = ['django', 'sqlalchemy'],
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
