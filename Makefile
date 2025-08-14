
all: build

test:
	uv run pytest -s

build:
	uv build

publish:
	uv publish

publish-test:
	uv publish --repository testpypi

clean:
	rm -rf ./build ./*.egg-info ./dist

.PHONY: all build publish publish-test clean test