import io
import re
from setuptools import setup, find_packages

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

with io.open('source/__init__.py', 'rt', encoding='utf8') as f:
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
        'alembic==0.9.9'
        'Babel==2.6.0'
        'blinker==1.4'
        'certifi==2018.4.16'
        'celery>=4.2.1',
        'chardet==3.0.4'
        'click==6.7'
        'dominate==2.3.1'
        'elasticsearch==6.2.0'
        'Flask>=1.0.2',
        'Flask-Babel==0.11.2',
        'Flask-Bootstrap==3.3.7.1',
        'Flask-HTTPAuth>=3.2.4',
        'Flask-Login>=0.4.1',
        'Flask-Mail>=0.9.1',
        'Flask-Moment==0.6.0',
        'Flask-WTF==0.14.2',
        'flask-mongoengine>=0.9.5',
        'guess-language-spirit==0.5.3',
        'gunicorn>=19.9.0',
        'idna==2.6',
        'itsdangerous>=0.24',
        'Jinja2==2.10',
        'Mako==1.0.7',
        'MarkupSafe==1.0',
        'PyJWT==1.6.4',
        'python-dateutil==2.7.3',
        'python-dotenv>=0.9.1',
        'python-editor==1.0.3',
        'pytz==2018.4',
        'redis>=2.10.6',
        'requests==2.18.4',
        'six==1.11.0',
        'urllib3==1.22',
        'visitor==0.1.3',
        'Werkzeug==0.14.1',
        'WTForms==2.1',
    ],
    extras_require={
        'dev': [
            'coverage>=4.5.1',
            'flake8>=3.5.0 ',
            'black>=18.6b4',
        ]
    },
)
