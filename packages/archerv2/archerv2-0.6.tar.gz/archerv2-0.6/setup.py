import os

from setuptools import setup

readme = open('README.rst').read()

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Other Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Utilities',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

py_modules = []

for root, folders, files in os.walk('archerv2'):
    for f in files:
        if f.endswith('.py'):
            full = os.path.join(root, f[:-3])
            parts = full.split(os.path.sep)
            modname = '.'.join(parts)
            py_modules.append(modname)

setup(
    name='archerv2',
    version='0.6',

    url='https://github.com/dstarner15/archerv2',
    description='Thrift app the flask way...The Right Way',
    long_description=readme,
    author='Daniel Starner',
    author_email='starner.daniel5@gmail.com',
    license='MIT',

    classifiers=CLASSIFIERS,
    zip_safe=False,
    py_modules=py_modules,
    include_package_data=True,
    setup_requires=[
        'click>=3.3',
        'thriftpy>=0.3.9'
    ],
    install_requires=[
        'click>=3.3',
        'thriftpy>=0.3.9'
    ],
    entry_points="""
    [console_scripts]
    archerv2=archerv2.cli:main
    """
)
