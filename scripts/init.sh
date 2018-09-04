#!/bin/bash
venv_name="site_discovery"
#source virtualenvwrapper.sh

# go to virtualenv or create it
workon "$venv_name" || { mkvirtualenv "$venv_name" && workon "$venv_name" && pip install -e . && pip install twine }
