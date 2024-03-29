import os

import setuptools


with open("README.rst", "r") as readme:
    LONG_DESCRIPTION = readme.read()

setuptools.setup(
    name="freesurfer-volume-reader",
    use_scm_version={
        "write_to": os.path.join("freesurfer_volume_reader", "version.py"),
        # `version` triggers pylint C0103
        # 2 newlines after import & 2 spaces before # for black
        "write_to_template": "# pylint: disable=missing-module-docstring\nimport typing\n\n"
        + '__version__: typing.Optional[str] = "{version}"\n',
    },
    description="Python script & library to read hippocampal subfield volumes"
    "computed by Freesurfer & ASHS",
    long_description=LONG_DESCRIPTION,
    author="Fabian Peter Hammerle",
    author_email="fabian@hammerle.me",
    url="https://github.com/fphammerle/freesurfer-volume-reader",
    # TODO add license
    keywords=[
        "brain",
        "freesurfer",
        "hippocampus",
        "neuroimaging",
        "reader",
        "subfields",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        # .github/workflows/python.yml
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Utilities",
    ],
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "freesurfer-volume-reader = freesurfer_volume_reader.__main__:main"
        ]
    },
    python_requires=">=3.7",  # python<3.7 untested
    install_requires=[
        # >=0.21.0 pandas.DataFrame.drop(columns=[...], ...)
        # <0.23 untested
        "pandas>=0.23.0,<2"
    ],
    setup_requires=["setuptools_scm"],
    tests_require=["pytest<5", "pytest-timeout<2"],
)
