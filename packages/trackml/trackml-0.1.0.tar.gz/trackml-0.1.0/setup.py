import setuptools

setuptools.setup(
    name="trackml",
    version="0.1.0",
    url="https://github.com/borntyping/cookiecutter-pypackage-minimal",

    author="Gideon",
    author_email="Gideon@semantica-labs.com",

    description="An opinionated, minimal cookiecutter template for Python packages",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=["websocket"],
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
