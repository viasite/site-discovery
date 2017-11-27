## Upload to pypi
```
pip install twine
rm -rf build dist site_discovery.egg-info && python setup.py sdist bdist_wheel && twine upload dist/*
```
