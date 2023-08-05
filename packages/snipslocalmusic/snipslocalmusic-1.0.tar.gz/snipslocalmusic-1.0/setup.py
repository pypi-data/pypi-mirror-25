from setuptools import setup

setup(
    name='snipslocalmusic',
    version='1.0',
    description='Local music player skill for Snips',
    author='Michael Fester',
    author_email='michael.fester@gmail.com',
    url='https://github.com/snipsco/snips-skill-localmusic',
    download_url='',
    license='MIT',
    install_requires=['pygame'],
    test_suite="tests",
    keywords=['snips'],
    package_data={'snipslocalmusic': ['Snipsspec']},
    packages=['snipslocalmusic'],
    include_package_data=True,
)
