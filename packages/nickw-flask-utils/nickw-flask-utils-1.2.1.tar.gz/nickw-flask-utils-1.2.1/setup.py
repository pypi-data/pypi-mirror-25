from setuptools import setup
import os

extras = {
    'ldap': [],
    'restful': ['flask-restful'],
    'celery': ['celery'],
    'sentry': ['raven[flask]'],
    'pagination': ['webargs', 'marshmallow'],
    'webargs': ['webargs'],
    'token_auth': ['marshmallow']
}

packages = [
    'flask_utils',
    'flask_utils.celery',
    'flask_utils.config',
    'flask_utils.deployment_release',
    'flask_utils.pagination',
    'flask_utils.restful',
    'flask_utils.sentry',
    'flask_utils.testing',
    'flask_utils.token_auth',
    'flask_utils.webargs',
]

tests_require = []
for x in extras.values():
    tests_require.extend(x)


def get_version():
    version_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'VERSION')
    v = open(version_path).read()
    if type(v) == str:
            return v.strip()
    return v.decode('UTF-8').strip()


readme_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)),
    'README.rst',
)
long_description = open(readme_path).read()

try:
    version = get_version()
except Exception as e:
    version = '0.0.0-dev'

setup(
    name='nickw-flask-utils',
    version=version,
    packages=packages,
    package_data={'': ['LICENSE', 'README.rst']},
    zip_safe=False,
    include_package_data=True,
    extras_require=extras,
    tests_require=tests_require,
    test_suite='tests',
    url='https://github.com/nickw444/nickw-flask-utils',
    author='Nick Whyte',
    author_email='nick@nickwhyte.com',
    description=('A set of utilities to make working with flask web '
                 'applications easier.'),
    long_description=long_description
)
