from setuptools import setup

def readme():
    with open('README.rst') as readme:
        return readme.read()

setup(
        name = 'QuiCalc',
        version = '0.1',
        description = 'Simple Terminal Calculator',
        long_description = readme(),
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python :: 3.5',
            'Topic :: Scientific/Engineering :: Mathematics',
            'License :: OSI Approved :: MIT License'
            ],
        keywords = 'tools math terminal python calculator',
        author = 'Abhishta Gatya',
        author_email = 'abhishtagatya@yahoo.com',
        license = 'MIT',
        packages = ['bin'],
        scripts = ['bin/calc'],
        python_requires = '>=3',
        include_package_data = True,
        zip_safe = False
        )
