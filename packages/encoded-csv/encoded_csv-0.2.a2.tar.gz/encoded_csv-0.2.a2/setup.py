from codecs import open
from distutils.core import setup
from os import path

here = path.abspath(path.dirname(__file__))
readme_file = path.join(here, 'README.md')
try:
    from m2r import parse_from_file
    long_description = parse_from_file(readme_file)
except ImportError:
    # m2r may not be installed in user environment
    with open(readme_file, encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='encoded_csv',
    version='0.2.a2',
    description='Read a CSV file using arbitrary character encodings.',
    long_description=long_description,
    url='http://change.me',
    author='Tom Elliott',
    author_email='tom.elliott@nyu.edu',
    license='LICENSE.txt',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ],
    keywords='scripting, csv, i18n, encoding',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['encoded_csv'],

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['chardet'],
    python_requires='~=3.6',

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    # package_data={
    #     'sample': ['package_data.dat'],
    # },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },
)
