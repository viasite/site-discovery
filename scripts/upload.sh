#!/bin/bash
#source virtualenvwrapper.sh

# go to virtualenv or create it
workon site-discovery || \
    mkvirtualenv site-discovery && \
    workon site-discovery && \
    pip install -e . && \
    pip install twine \


# upload
rm -rf build dist site_discovery.egg-info && \
python setup.py sdist bdist_wheel && \
twine upload "dist/*"
