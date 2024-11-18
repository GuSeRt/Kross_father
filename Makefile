
VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
ACTIVATE = . $(VENV)/bin/activate


.PHONY: all install test clean

# Цель по умолчанию - установить зависимости и запустить тесты
all: install test


$(VENV):
	python3 -m venv $(VENV)


install: $(VENV)
	$(ACTIVATE) && $(PIP) install -r requirements.txt

test:
	$(ACTIVATE) && python3 -m unittest discover tests/

# Очистка временных файлов
clean:
	rm -rf $(VENV)
