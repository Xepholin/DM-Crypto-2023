run:
	python3.11 src/main.py enc 000000 000000
	python3.11 src/main.py dec bb57e6 000000

mitm:
	python 3.11 src/main.py mitm ea82ec 4b8784 113da5 8b0074

clean:
	-rm -rf src/__pycache__