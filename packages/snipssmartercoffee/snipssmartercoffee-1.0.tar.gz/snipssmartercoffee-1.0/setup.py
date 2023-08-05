from setuptools import setup

setup(
    name='snipssmartercoffee',
    version='1.0',
    description='Smarter Coffee skill for Snips',
    author='Michael Fester',
    author_email='michael.fester@gmail.com',
    url='https://github.com/snipsco/snips-skill-smarter-coffee',
    download_url='',
    license='MIT',
    install_requires=[],
    test_suite="tests",
    keywords=['snips'],
    packages=['snipssmartercoffee'],
    package_data={'snipssmartercoffee': ['Snipsspec']},
    include_package_data=True,
)
