#!/bin/bash
coverage run --rcfile=.coveragerc tests/testsuite.py && coverage html

