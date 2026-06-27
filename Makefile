.ONESHELL:
.PHONY: builder

builder:
	source devEnv/bin/activate
	python3 generator.py $(ARGS)
	pdflatex -interaction=batchmode -output-directory=build build/resume.tex
	cp build/resume.pdf .
	deactivate
