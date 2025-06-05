format:
	@python3 -m venv venv
	black wifipumpkin3 setup.py

test:
	@python3 -m venv venv
	python3 -m unittest -v

test_coverage:
	@python3 -m venv venv
	python3 -m coverage run -m tests
	python3 -m coverage report
	python3 -m unittest -v

install:
	@python3 -m venv venv
	@pip install --upgrade pip setuptools wheel
	@pip install build
	find . -name '*.pyc' -delete
	@python3 -m build

install_env:
	@python3 -m venv venv
	#python3 -m pip install PyQt5==5.14
	#python3 -c "from PyQt5.QtCore import QSettings; print('done')"
	find . -name '*.pyc' -delete
	python3 -m pip install .

install_dev:
	@python3 -m venv venv
	pip3 uninstall wifipumpkin3
	find . -name '*.pyc' -delete
	@python3 -m build

clean:
	@rm -rf build dist README MANIFEST *.egg-info
	@rm -rf *.egg-info build/ dist/ __pycache__/
	@python3 setup.py clean --all

distclean: clean
	rm -rf .venv venv/
