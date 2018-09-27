import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(
        data_file=os.path.join(os.path.dirname(__file__), '.coverage'),
        branch=True,
        include=os.path.join(os.path.dirname(__file__), 'app/*')
        )
    COV.start()

import sys
import click
from backend.app import create_app, db
from backend.app.models.auth import User, Role, Permission

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.cli.command()
@click.option('--coverage/--no-coverage', default=False,
              help='Run tests under code coverage.')
def test(coverage, test_name=None):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import subprocess
        os.environ['FLASK_COVERAGE'] = '1'
        sys.exit(subprocess.call(sys.argv))

    import unittest
    if test_name is None:
        test_directory = os.path.join(os.path.dirname(__file__), 'tests')
        tests = unittest.TestLoader().discover(test_directory)
    else:
        tests = unittest.TestLoader().loadTestsFromName('tests.' + test_name)
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


@app.cli.command()
@click.option('--length', default=25,
              help='Number of functions to include in the profiler report.')
@click.option('--profile-dir', default=None,
              help='Directory where profiler data files are saved.')
def profile(length, profile_dir):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # create or update user roles
    Role.insert_roles()

    # create administrator
    r = Role.objects(name="Administrator").first()
    u = User(
        email=os.getenv('BACKEND_ADMIN'),
        username=os.getenv('BACKEND_ADMIN_USERNAME'),
        role=r,
        confirmed=True
        )
    u.password = os.getenv('BACKEND_ADMIN_PASSWORD')
    u.can(Permission.FOLLOW)
    u.can(Permission.COMMENT)
    u.can(Permission.WRITE)
    u.can(Permission.MODERATE)
    u.can(Permission.ADMIN)
    u.save()
