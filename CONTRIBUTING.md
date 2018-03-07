## Developer install
```
source virtualenvwrapper.sh
mkvirtualenv site-discovery
workon site-discovery
cd site-discovery
pip install -e .
```


## Generate changelog

```
conventional-changelog -p angular -i CHANGELOG.md -s -r 0
```



## Upload to pypi

```
pip install twine
rm -rf build dist site_discovery.egg-info && python setup.py sdist bdist_wheel && twine upload dist/*
```

#### error in setup command: Error parsing /home/popstas/projects/python/site-discovery/setup.cfg: ImportError: No module named tasks
Use `pbr==3.0.1` version.