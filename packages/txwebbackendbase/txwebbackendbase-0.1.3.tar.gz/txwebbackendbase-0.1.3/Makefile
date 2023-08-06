.PHONY: build

MODULE:=txwebbackendbase

all: dev style checks build dists test-unit

dev:
	@echo "Setting up development environment"
	@pipenv install --dev

install-local:
	@pipenv install

install-system:
	@pipenv install --system

style: isort autopep8 yapf

isort:
	@pipenv run isort -y

autopep8:
	@pipenv run autopep8 --in-place --recursive setup.py $(MODULE)

yapf:
	@pipenv run yapf --style .yapf --recursive -i $(MODULE)

checks: sdist flake8 pylint

flake8:
	@pipenv run python setup.py flake8

pylint:
	@pipenv run pylint --rcfile=.pylintrc --output-format=colorized $(MODULE)

build: dists

run-local:
	@echo "Starting Dopplerr on http://localhost:$(TEST_PORT) ..."
	@pipenv run $(MODULE) --port $(TEST_PORT) --verbose --logfile "debug.log" --mapping tv=Series --languages $(SUBDLSRC_LANGUAGES)

shell:
	@echo "Shell"
	@pipenv shell

test-unit:
	@pipenv run pytest $(MODULE)

test-coverage:
	pipenv run py.test -v --cov $(MODULE) --cov-report term-missing

dists: sdist bdist wheels

sdist:
	@pipenv run python setup.py sdist

bdist:
	@pipenv run python setup.py bdist

wheels:
	@echo "Creating distribution wheel"
	@pipenv run python setup.py bdist_wheel

pypi-publish: build
	@echo "Publishing to Pypy"
	@pipenv run python setup.py upload -r pypi

update:
	@echo "Updating dependencies..."
	@pipenv update

githook:style

push: githook
	@git push origin --tags

# aliases to gracefully handle typos on poor dev's terminal
check: checks
devel: dev
develop: dev
dist: dists
install: install-system
pypi: pypi-publish
styles: style
test: test-unit
wheel: wheels
