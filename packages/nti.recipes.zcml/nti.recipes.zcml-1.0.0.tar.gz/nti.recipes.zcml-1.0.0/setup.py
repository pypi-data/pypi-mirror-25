import os
from setuptools import setup, find_packages


entry_points = {
    "zc.buildout" : [
        'default = nti.recipes.zcml:ZCML'
    ],
}

here = os.path.dirname(__file__)

def read(*rnames):
    with open(os.path.join(here, *rnames)) as f:
        return f.read()

setup(
    name='nti.recipes.zcml',
    version='1.0.0',
    author='Jason Madden',
    author_email='open-source@nextthought.com',
    description="zc.buildout recipes for writing ZCML",
    long_description=(
        read('src', 'nti', 'recipes', 'zcml', 'README.rst')
        + '\n\n' +
        read('CHANGES.rst')
    ),
    license='APACHE 2.0',
    keywords='buildout zcml',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Natural Language :: English',
        'Framework :: Buildout',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['nti', 'nti.recipes'],
    install_requires=[
        'setuptools',
        'zc.buildout >= 2.9.4',
    ],
    extras_require={
        'test': [
            # we import zc.buildout's 'test' package. It does have a
            # 'test' extra, but we really don't want all the things
            # that drags in, so we just list what's necessary for our
            # own tests to run.
            'manuel',
            'zope.testing',
            'zope.testrunner'
        ],
    },
    url='http://github.com/NextThought/nti.recipes.zcml',
    entry_points=entry_points,
    include_package_data=True,
    zip_safe=False,
)
