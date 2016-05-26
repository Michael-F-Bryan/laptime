# A shell pipeline that'll correctly get the next patch version
next_version = $(shell \
	python3 -c 'import laptime; print(laptime.__version__)' | \
	cut -d "+" -f 1 | \
	awk -F "." '{patch = $$3 + 1; print($$1 "." $$2 "." patch) }' )



tag:
	@git diff-index --quiet HEAD -- || (printf 'Please commit your changes first.\n\n'; exit 1)
	@echo New version: $(next_version)
	git tag -a "$(next_version)" -m "version $(next_version)"
	git push 
	git push --tags

test:
	py.test

# Alias for test
tests: test

coverage:
	coverage run -m pytest
	coverage html
	firefox coverage_report/index.html

.PHONY: test coverage tag


