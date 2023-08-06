init:
	touch CHANGES.rst
	touch LICENSE.rst
	touch MANIFEST.in
	touch README.rst
	touch setup.py
	mkdir -p ono
	touch ono/__init__.py
	mkdir -p tests

distribution:
	python3 setup.py sdist --formats=gztar bdist_wheel

upload:
	twine upload dist/*

