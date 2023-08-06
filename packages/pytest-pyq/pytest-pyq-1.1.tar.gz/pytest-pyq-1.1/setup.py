"""Pytest fixture "q" for pyq

Once this package is installed, you can use "q" fixture
in your pytest tests::

    def test_pyq(q):
        q.test = [1, 2, 3]
        assert q.test.count == 3
"""
from setuptools import setup

VERSION = '1.1'
setup(
    name="pytest-pyq",
    description=__doc__.split('\n\n', 1)[0],
    long_description=__doc__,
    py_modules=['pytest_pyq'],
    version=VERSION,
    url='http://pyq.enlnt.com',
    author='Enlightenment Research, LLC',
    author_email='pyq@enlnt.com',
    license='BSD',
    zip_safe=True,
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Programming Language :: Python',
                 'Topic :: Software Development :: Quality Assurance',
                 'Topic :: Software Development :: Testing',
                 ],
    # the following makes a plugin available to py.test
    entry_points={
        'pytest11': [
            'pytest_pyq = pytest_pyq',
        ],
    },
)

