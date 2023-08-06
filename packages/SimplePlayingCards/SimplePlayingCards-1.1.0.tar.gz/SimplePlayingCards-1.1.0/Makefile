scripts=setup.py playingcards.py

all: clean local test

test:
	python3 -xm unittest discover

clean:
	rm -rf dist/ build/ *.pyc

local:$(scripts)
	pip3 install -e ./ --user


dist:$(scripts) clean
	python3 setup.py sdist bdist_wheel
	gpg --detach-sign -a dist/*.tar.gz
	gpg --detach-sign -a dist/*.whl

upload:
	twine upload dist/SimplePlayingCards*tar.gz dist/Simple*whl dist/SimplePlayingCards*asc
