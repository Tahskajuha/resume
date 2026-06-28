.ONESHELL:
.PHONY: builder master

builder:
	source devEnv/bin/activate
	python3 generator.py $(ARGS)
	pdflatex -interaction=batchmode -output-directory=build build/resume.tex
	cp build/resume.pdf .
	deactivate

master: ARGS=-P capstone cryptscribe gamescope gan greeter ims llm msp430 opusrx rstreamer rsubmix resume \
             -S frontend backend database linux android networking reverse_engineering machine_learning embedded visualization security
master: builder
