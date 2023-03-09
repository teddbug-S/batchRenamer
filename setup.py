from setuptools import setup, find_packages

from src.batchRenamer import __version__

with open("README.md") as readme:
    long_description = readme.read()

setup(
    name="batchRenamer",
    version=__version__,
    author="Divine Darkey (teddbug-S)",
    author_email="teddbug47@gmail.com",
    maintainer="Divine Darkey (teddbug-S)",
    maintainer_email="teddbug47@gmail.com",
    long_description=long_description,
    url="https://github.com/teddbug-S/batchRenamer",
    project_urls={
        "Issues": "https://github.com/teddbug-S/batchRenamer/issues",
        "Pull Requests": "https://github.com/teddbug-S/batchRenamer/pulls"
    },
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
    ],
    package_dir={"": "src"},
    packages=find_packages("src"),
    python_requires=">=3.6",
    requires=["click"],
    entry_points={
        'console_scripts': [
            'batchRenamer = batchRenamer.__main__:main',
        ]
    }
)
