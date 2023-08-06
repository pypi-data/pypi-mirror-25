from setuptools import setup

setup(
    name='alvin_test_package',
    version='0.0.1',
    description='A test project',
    url='https://github.com/alvinhui/alvin_test_package',
    author='Alvin Hui',
    author_email='alvinxwt@gmail.com',
    license='MIT',
    install_requires=[
        "numpy>=1.13",
    ],
    packages=['alvin_test_package']
)