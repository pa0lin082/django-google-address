test:
	@python google_address/tests/runtests.py

clean-pycache:
	@rm -r **/__pycache__

clean: clean-pycache

.PHONY: clean


