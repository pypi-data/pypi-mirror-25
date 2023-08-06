from setuptools import setup, find_packages


setup(
    name='vaquero',
    version='0.0.3',
    description="A tool for iterative and interactive data wrangling.",
    long_description="See: `github repo <https://github.com/jbn/vaquero>`_.",
    url="https://github.com/jbn/vaquero",
    author="John Bjorn Nelson",
    author_email="jbn@pathdependent.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ],
    keywords=["data analysis", "data science", "elt"],
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    install_requires=[
        'jmespath',
        'numpy',
        'pandas',
    ]
)
