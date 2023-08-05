try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requirements = [pkg.split('=')[0] for pkg in open('requirements.txt').readlines()]

classifiers = ['Environment :: Console',
               'Programming Language :: Python :: 3.5'
               ]


setup(
    name='keep_password',

    version='v1.0',  # Ideally should be same as your GitHub release tag varsion
    description='Save password for username',
    author='chandra khadka',
    author_email='chandra2khadka4@gmail.com',
    url='https://github.com/chandrabrt/keep_password',
    scripts=['src/keep_password'],
    install_requires=requirements,
    package=['keep-password'],
    package_dir={'keep-password': 'src/keep-password'},
    classifiers=classifiers
)

