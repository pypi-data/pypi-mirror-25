from distutils.core import setup
from setuptools import find_packages

setup(
    name = 'modelchemy',
    packages = find_packages('src'),
    package_dir={'': 'src'},
    version = '0.0.1-alpha3',
    description = 'Library for working SQLAlchemy with Django',
    author='Raymond Joseph Usher Roche',
    author_email = 'rjusher+pypi@gmail.com',
    install_requires=['django', 'sqlalchemy'],
    url='https://github.com/rjusher/modelchemy',
    download_url = 'https://github.com/rjusher/modelchemy/archive/v0.0.1-alpha2.tar.gz',
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
