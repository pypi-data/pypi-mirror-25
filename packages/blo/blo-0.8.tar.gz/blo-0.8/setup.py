from setuptools import setup, find_packages
from os import path


with open(path.join(path.abspath(path.dirname(__file__)), 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='blo',
    version='0.8',
    license='BSD-3-clause',
    author='Yann Savuir',
    author_email='savuir@gmail.com',
    description='Blo - a simple static blog generator',
    long_description=long_description,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'blo = blo.blog:main',
        ],
    },
    install_requires=['jinja2', 'markdown', 'PyRSS2Gen'],
    package_data={'': ['blo/default.json', 'blo/draft_templates.json',]},
    include_package_data=True,
    url='https://github.com/savuir/blo',  # use the URL to the github repo
    download_url='https://github.com/savuir/blo/tarball/0.1',  # I'll explain this in a second
    keywords=['blogging', 'blog', 'static blog generator'],  # arbitrary keywords
)
