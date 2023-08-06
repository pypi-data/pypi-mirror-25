.PHONY: clean-pyc clean-build docs venv


test:
	@nosetests -s

bench:
	@python tests/bench.py

coverage:
	@rm -f .coverage
	@nosetests --with-coverage --cover-package=guidemd --cover-html

clean: clean-build clean-pyc clean-docs

dist: clean-build
	@python setup.py sdist bdist_wheel

clean-build:
	-@rm -fr build/
	-@rm -fr *.egg-info
	-@rm -fr dist/

clean-pyc:
	-@find . -name '*.pyc' -exec rm -f {} +
	-@find . -name '*.pyo' -exec rm -f {} +
	-@find . -name '*~' -exec rm -f {} +
	-@find . -name '__pycache__' -exec rm -fr {} +

clean-docs:
	@rm -fr  docs/_build

docs:
	@$(MAKE) -C docs html

rtd:
	curl -X POST http://readthedocs.org/build/guidemd

publish:
	@twine upload dist/*


.PHONY: build
