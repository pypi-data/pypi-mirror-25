from setuptools import setup
import codecs

setup(
    name='superpowers',
    description=(
        'Scala-like map for Python, do [1, 2, 3].map(_*3)'
    ),
    version='0.1.1',
    license='BSD',
    author='Teemu',
    author_email='teemu.on.ihminen@gmail.com',
    py_modules=['superpowers'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['forbiddenfruit'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
