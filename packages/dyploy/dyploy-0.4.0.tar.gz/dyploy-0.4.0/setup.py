from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

version = '0.4.0'

setup(
    name='dyploy',
    version=version,
    description="dyploy",
    long_description=README,
    classifiers=[],
    keywords='dyploy',
    author='me',
    author_email='me@example.org',
    url='https://example.org',
    license='LGPL v3',
    zip_safe=True,
    py_modules=['dyploy'],
    include_package_data=True,
    package_dir={},
    install_requires=[
        'click',
        'prettytable',
        'configobj',
        'paramiko',
        'scp',
        'voluptuous',
        'pyyaml',
        'dpath',
        'dyools',
    ],
    entry_points='''
        [console_scripts]
        dyploy=dyploy:main
    ''',
)
