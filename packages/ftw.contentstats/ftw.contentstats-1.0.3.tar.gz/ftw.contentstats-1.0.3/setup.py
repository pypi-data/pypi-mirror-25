from setuptools import find_packages
from setuptools import setup
import os

version = '1.0.3'

tests_require = [
    'ftw.builder',
    'ftw.testbrowser',
    'ftw.testing',
    'plone.app.testing',
    'plone.testing',
    'transaction',
    'unittest2',
    'zope.configuration',
    'freezegun',
    'requests_toolbelt',
]

extras_require = {
    'tests': tests_require,
}


setup(
    name='ftw.contentstats',
    version=version,
    description='Collect and display content statistics for Plone sites',
    long_description=open("README.rst").read() + "\n" + open(
        os.path.join("docs", "HISTORY.txt")).read(),

    # Get more strings from
    # http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    keywords='ftw content stats statistics',
    author='4teamwork AG',
    author_email='mailto:info@4teamwork.ch',
    url='https://github.com/4teamwork/ftw.contentstats',
    license='GPL2',

    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['ftw'],
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'Plone',
        'Products.CMFCore',
        'Products.CMFPlone',
        'Products.GenericSetup',
        'plone.api',
        'setuptools',
        'zope.i18nmessageid',
        'tzlocal',
        'pytz',
        'requests',
        'path.py >= 6.2',
    ],

    tests_require=tests_require,
    extras_require=extras_require,

    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone

    [console_scripts]
    dump-content-stats = ftw.contentstats.console:dump_stats_cmd
    """,
)
