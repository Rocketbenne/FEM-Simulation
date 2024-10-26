# define the name of the virtual environment directory
VENV := venv
# use venv if it exists, else use global python3
PYTHON = $(if $(wildcard $(VENV)/bin/python), $(VENV)/bin/python, python3)

# Detect targets that start with 'run_'
RUN_TARGETS = $(shell ls | grep -E '^run_[0-9]+')

# default target, when make executed without arguments
all: venv

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt

# venv is a shortcut target
venv: $(VENV)/bin/activate

run_%:
	$(PYTHON) source/main.py --name $* $(ARGS_$*)

# Command-line arguments for each test case
ARGS_noInputs = 
ARGS_allDirichletSameValue = --left_bound "[100, 'Dirichlet']" --top_bound "[100, 'Dirichlet']" --right_bound "[100, 'Dirichlet']" --bottom_bound "[100, 'Dirichlet']"
ARGS_horizontalAscending = --width 10 --height 10 --nodes_per_axis 11 --left_bound "[0,'Dirichlet']" --top_bound "[0,'Neumann']" --right_bound "[100,'Dirichlet']" --bottom_bound "[0,'Neumann']"
ARGS_differentMatTensor = --mat_tensor [[1,1],[1,1]]
ARGS_hotLineInMiddle = --nodes_per_axis 9 --left_bound "[0, 'Dirichlet']" --right_bound "[0, 'Dirichlet']" --line_start [55,0] --line_end [55,100] --line_value 100 --line_points 20
ARGS_hotDotInMiddle = --nodes_per_axis 9 --left_bound "[0, 'Dirichlet']" --top_bound "[0, 'Dirichlet']" --right_bound "[0, 'Dirichlet']" --bottom_bound "[0, 'Dirichlet']" --line_start [55,55] --line_end [55,55] --line_value 100 --line_points 1

# runs all the testcases
testbench: 
	make run_noInputs
	make run_allDirichletSameValue
	make run_horizontalAscending
	make run_differentMatTensor
	make run_hotLineInMiddle
	make run_hotDotInMiddle

# 
referenceCheck_%:
	$(PYTHON) tests/main.py --name $*

validation:
	make referenceCheck_noInputs
	make referenceCheck_allDirichletSameValue
	make referenceCheck_horizontalAscending
	make referenceCheck_differentMatTensor
	make referenceCheck_hotLineInMiddle
	make referenceCheck_hotDotInMiddle


clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

.PHONY: all venv run clean testbench run_% validation referenceCheck_%

# TODO cmd still arguments missing 