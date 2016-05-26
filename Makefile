
define next_tag = 
# Bastardized shell call to get the next minor version
$(shell python3 -c 'import laptime, re; v=re.search(r"(\d+)\.(\d+)\.(\d+)", laptime.__version__); v=[int(a) for a in v.groups()]; v[-1] += 1; print(".".join(str(a) for a in v))')
endef


tag:
	@git diff-index --quiet HEAD -- || (printf "Please commit your changes first.\n\n"; exit 1)
	git tag -a "$(next_tag)" -m "version $(next_tag)"
	git push && git push --tags


test:
	py.test

coverage:
	coverage run -m pytest
	coverage html
	firefox coverage_report/index.html

.PHONY: test coverage tag

