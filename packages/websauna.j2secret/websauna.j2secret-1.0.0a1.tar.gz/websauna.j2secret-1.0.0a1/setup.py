"""Websauna Jinja2 extension that adds a tag to generate secrets."""
from setuptools import find_packages
from setuptools import setup

import os


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst')) as f:
    CHANGES = f.read()


requires = [
    'jinja2',
]

dev_requires = [
    'zest.releaser[recommended]'
]

test_requires = [
    'codecov',
    'coverage',
    'flake8',
    'pytest',
    'pytest-cov',
]


setup(
    name='websauna.j2secret',
    version='1.0.0a1',
    description='Websauna Jinja2 extension that adds a tag to generate secrets.',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development',
    ],
    keywords='jinja2, websauna, pyramid',
    author='Websauna Team',
    author_email='developers@websauna.org',
    url='https://github.com/websauna/websauna.j2secret',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require={
        'dev': dev_requires,
        'test': test_requires,
    },
    entry_points="""""",
)
