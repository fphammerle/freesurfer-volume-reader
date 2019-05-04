import setuptools

import freesurfer_volume_reader


LONG_DESCRIPTION = freesurfer_volume_reader.__doc__.strip()

setuptools.setup(
    name='freesurfer-volume-reader',
    use_scm_version=True,
    description=LONG_DESCRIPTION.split(sep='\n', maxsplit=1)[0],
    long_description=LONG_DESCRIPTION,
    author='Fabian Peter Hammerle',
    author_email='fabian@hammerle.me',
    url='https://github.com/fphammerle/freesurfer-volume-reader',
    # TODO add license
    keywords=[
        'brain',
        'freesurfer',
        'hippocampus',
        'neuroimaging',
        'reader',
        'subfields',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Utilities',
    ],
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'freesurfer-volume-reader = freesurfer_volume_reader.__main__:main',
        ],
    },
    install_requires=[
        # pandas.DataFrame.drop(columns=[...], ...)
        'pandas>=0.21.0,<1',
    ],
    setup_requires=[
        'setuptools_scm',
    ],
    tests_require=[
        'pylint>=2.3.0,<3',
        'pytest<5',
        'pytest-cov<3,>=2',
        'pytest-timeout<2',
    ],
)
