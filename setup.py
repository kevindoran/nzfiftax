import setuptools

setuptools.setup(
    name='nzfiftax',
    packages=['nzfiftax'],
    # This sets the directory, src, to be the root package (denoted by '').
    # It should be possible to do this:
    # package_dir={'micronet': 'src/micronet'}
    # But this doesn't work with editable installs, as described here.
    # https://stackoverflow.com/questions/19602582/pip-install-editable-links-to-wrong-path
    # Possibly related to the  long open bug:
    # https://github.com/pypa/setuptools/issues/230
    # So, the package must be added at the root level.
    package_dir={'': 'src'}
)

