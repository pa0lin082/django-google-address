test:
	@python ovp_core/tests/runtests.py

lint:
	@pylint ovp_core

clean-pycache:
	@rm -r **/__pycache__

clean: clean-pycache

.PHONY: clean


