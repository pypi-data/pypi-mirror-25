from setuptools import setup, find_packages


with open('README.rst', 'r') as f:
    README = f.read()


setup(
    name = "fawrapper",
    version = "0.1.0a5",
    packages = find_packages(),
    description = 'A wrapper for the Fieldaware API',
    long_description = README,
    author = 'Johnny Kirchman',
    author_email = 'Jkirch86@gmail.com',
    license = 'MIT',
    url = 'https://github.com/J-Kirch/fawrapper',
    python_requires = '>3.6',
    install_requires = ['requests'],
    setup_requires = ['pytest-runner'],
    tests_require = ['pytest', 'vcrpy', 'pytest-vcr'],
    keywords = [],
    classifiers = [],
)
