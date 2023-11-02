
# define the name of the virtual environment directory
VENV := venv

# default target, when make executed without arguments
all: venv

venv: requirements.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt
	@echo "Virtual environment created. Activate it with the following command:"
	@echo "source $(VENV)/bin/activate"

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

.PHONY: all venv run clean