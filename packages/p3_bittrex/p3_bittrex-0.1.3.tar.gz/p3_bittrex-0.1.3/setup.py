
from setuptools import setup


setup(
    name="p3_bittrex",
    packages=['p3_bittrex'],
    modules=['bittrex'],
    version="0.1.3",
    description="Bittrex API pacakge",
    author="Andy Hsieh",
    author_email="andy.hsieh@hotmail.com",
    license='LICENSE.txt',
    url='https://github.com/bealox/p3-bittrex',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
        'Topic :: Office/Business :: Financial',
    ],
    install_requires=[
        "requests >= 2.18.3",
        'setuptools'
    ]

)
