from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIREMENTS = ['argparse', 'packaging', 'requests']

setup(
    name="pychk",
    version="1.0.1",
    description="A command line tool for developers to check if their project dependencies have known vulnerabilities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ayushpriya10/pychk",
    author="Ayush Priya",
    author_email="ayushpriya10@gmail.com",
    packages=find_packages(include=[
        "pychk"
    ]),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            'pychk = pychk.main:run_app'
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License ",
        "Programming Language :: Python :: 3.6",
    ],
    python_requires='>=3.6',
    install_requires=REQUIREMENTS,
    keywords='pip requirements security SAST sast vulnerability dependencies dependency vulnerable'
)