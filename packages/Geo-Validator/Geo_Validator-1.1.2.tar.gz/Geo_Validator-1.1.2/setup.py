from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
here = path.abspath(path.dirname(__file__))
setup (
    name = 'Geo_Validator',
    version ='1.1.2',
    description='Validates Lat/Long coords with address',
    long_description = 'Validates Lat/Long coords with address',
    url='https://github.com/Cheff789/GeoValidator',
    author='R. P. H.',
    author_email='rhaynes09@yahoo.com',
    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='latitude longitude address',
    packages=find_packages(),
    package_data={
    'GeoValidator': ['config.cfg'],
    },
    install_requires=['googlemaps'],
    python_requires='>=3',
    entry_points={
    'console_scripts': [
        'geofencingValidator=GeoValidator:main',
    ],
},
)