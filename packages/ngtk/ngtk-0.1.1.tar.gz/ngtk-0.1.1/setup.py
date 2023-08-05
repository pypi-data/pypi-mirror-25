from setuptools import setup

setup(
    name="ngtk",
    version='0.1.1',
    py_modules=['ngtk.cli'],
    description='A command line toolkit for ngrok.',
    author='DJ Strasser',
    author_email='test_test_test_test@gmail.com',
    url='https://github.com/Jigsaw-Jams/ngtk',
    install_requires=[
        'Click',
        'requests',
        'crayons'
    ],
    entry_points='''
        [console_scripts]
        ngtk=ngtk.cli:cli
    ''',
)