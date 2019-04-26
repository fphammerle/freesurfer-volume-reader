import setuptools

setuptools.setup(
    name='freesurfer-volume-reader',
    use_scm_version=True,
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
        # TODO add classifiers
        'Programming Language :: Python',
    ],
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'freesurfer-volume-reader = freesurfer_volume_reader:main',
        ],
    },
    install_requires=[
        'pandas',
    ],
    setup_requires=[
        'setuptools_scm',
    ],
    tests_require=[
        'pylint>=2.3.0',
        'pytest',
    ],
)
