import io
import re
from setuptools import setup, find_packages

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

with io.open('backend/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='devblog',
    version=version,
    url='https://github.com/dotRollen/edwardnunez.io',
    maintainer='Edward Nunez',
    maintainer_email='edwardnnz@gmail.com',
    description='Personal blogging and portfolio web page.',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask>=1.0.2',
        'Flask-HTTPAuth>=3.2.4',
        'Flask-Login>=0.4.1',
        'Flask-Mail>=0.9.1',
        'flask-mongoengine>=0.9.5',
        'redis>=2.10.6',
        'celery>=4.2.1',
        'Werkzeug>=0.14.1',
        'requests>=2.18.4',
        'itsdangerous>=0.24',
        'python-dotenv>=0.9.1',
        'click>=6.7',
        'gunicorn>=19.9.0',
    ],
    extras_require={
        'dev': [
            'coverage>=4.5.1',
            'flake8>=3.5.0 ',
            'black>=18.6b4',
        ]
    },
)
