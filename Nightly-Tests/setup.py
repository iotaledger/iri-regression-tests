from distutils.core import setup

setup(
    name='Nightly-Tests',
    version='0.1.0',
    author='DyrellC',
    py_modules=['Performance-Tests', 'utils'],
    license='LICENSE.txt',
    description='Nightly Tests for IRI',
    install_requires=[
        "PyOTA == 2.0.7",
        "psutil == 5.6.1",
        "matplotlib == 2.2.4"
    ],
)
