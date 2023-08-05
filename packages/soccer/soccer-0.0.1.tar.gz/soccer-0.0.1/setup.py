import setuptools

setuptools.setup(
    name="soccer",
    version="0.0.1",
    url="https://github.com/hhllcks/soccer",

    author="Hendrik Hilleckes",
    author_email="hhllcks@gmail.com",

    description="A soccer data framework",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
