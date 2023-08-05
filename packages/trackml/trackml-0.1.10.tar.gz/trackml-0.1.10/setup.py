import setuptools

setuptools.setup(
    name="trackml",
    version="0.1.10",
    url="https://github.com/track-ml/python-client/",

    author="Gideon",
    author_email="Gideon@semantica-labs.com",

    description="An opinionated, minimal cookiecutter template for Python packages",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),


    install_requires=["websocket-client>=0.44.0","requests>=2.18.4"],
    test_requires=['websocket-server'],
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
