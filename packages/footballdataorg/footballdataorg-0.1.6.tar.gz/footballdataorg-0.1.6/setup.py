import setuptools

setuptools.setup(
    name="footballdataorg",
    version="0.1.6",
    url="https://github.com/hhllcks/footballdataorg",

    author="Hendrik Hilleckes",
    author_email="hhllcks@gmail.com",

    description="A wrapper for the football-data.org api",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[
          'requests',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6'
    ],
)
