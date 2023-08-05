from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='pyhttpclient',
    version='0.1.3',
    description='Python helper of http request',
    long_description='Python helper of http request',
    url='https://github.com/sillyemperor/http',
    author='Wang Jiang',
    author_email='sillyemperor@163.com',
    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='http get post',
    packages=['http'],
    install_requires=[],
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={},
)
