from setuptools import setup

long_description = """
Foster is a thin wrapper around twine, making it easier to build and publish python packages.
"""

setup(
    name = 'foster',
    version = '0.1.0',

    packages = ['foster'],
    include_package_data = True,

    install_requires = ['twine >= 1, < 2'],
    entry_points = {'console_scripts': ['foster=foster.main:run']},

    author = 'Hugo Leonardo Leão Mota',
    author_email = 'hugo.txt@gmail.com',
    license = 'MIT',
    url = 'https://github.com/hugollm/foster',

    keywords = 'foster python package build publish',
    description = 'An easy way to publish your python packages',

    long_description = long_description,
)
