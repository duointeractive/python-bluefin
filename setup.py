from setuptools import setup
import bluefin

DESCRIPTION = "A simple Bluefin Payment System API."

LONG_DESCRIPTION = None
try:
    LONG_DESCRIPTION = open('README.rst').read()
except:
    pass

version_str = '%d.%d' % (bluefin.VERSION[0], bluefin.VERSION[1])

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    name='bluefin',
    version=version_str,
    packages=[
        'bluefin',
        'bluefin.directmode',
        'bluefin.dataretrieval',
    ],
    install_requires=['requests'],
    author='Gregory Taylor',
    author_email='gtaylor@duointeractive.com',
    url='https://github.com/duointeractive/python-bluefin/',
    license='MIT',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    platforms=['any'],
    classifiers=CLASSIFIERS,
)
