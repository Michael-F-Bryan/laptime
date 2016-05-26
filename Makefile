
test:
	coverage run -m pytest
	coverage html
	firefox coverage_report/index.html

.PHONY: test

