#!/usr/bin/env bash
pip install -r requirements.txt && pip install -e .[dev,test]

pre-commit install && pre-commit run --all-files
