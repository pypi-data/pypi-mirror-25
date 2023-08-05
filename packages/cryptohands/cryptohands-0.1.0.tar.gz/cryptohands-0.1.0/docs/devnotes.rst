.. highlight:: shell

=================
Development Notes
=================

A collection point for information about the development process for future collaborators


Release Process
---------------

This assumes you have virtualenvwrapper, git, and appropriate python versions installed, as well as the necessary test environment:

- update History.rst
- update setup.py
- check requirements.txt and requirements_dev.txt
- Commit all changes
- in bash::

    mktmpenv --python=python3.5
    cd ProjectDir
    pip install -e .[dev]
    tox
    # Fix issues
    python setup.py build_sphinx
    # check docs in build/sphinx/html/index.html
    # Commit any minor changes, else retest
    bumpversion patch|minor|major
    # Check version has updated correctly
    python setup.py sdist bdist_wheel
    deactivate
    mktmpenv
    pip install pip install path/to/projectname-version-etc.whl  # for example
    # Run appropriate tests, such as usage tests etc.
    deactivate
    # You may have to reactivate your original virtualenv
    twine upload dist/*
    # You may get a file exists error, check you're not trying to reupload an existing version
    git push --follow-tags

- check build in TravisCI
- check docs on ReadTheDocs
- check release published on Github and PyPi
