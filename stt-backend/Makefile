PYTHON = ./.venv/bin/python3

PROTOBUF_FOLDER = ../grpc-proto
PROTOBUF_FILE_PATH = $(PROTOBUF_FOLDER)/stt.proto
PROTOBUF_OUTPUT = ./generated/protobuf/

COLOR_LIGHT_GREEN=\e[1;32m
COLOR_LIGHT_BLUE=\e[1;34m
COLOR_NC=\e[0m

setup:
	python3 -m venv .venv
	poetry install
	echo "$(COLOR_LIGHT_GREEN)--$(COLOR_NC)"
	echo "$(COLOR_LIGHT_GREEN)-- run $(COLOR_LIGHT_BLUE)'source .venv/bin/activate'$(COLOR_LIGHT_GREEN) to enter the virtual enviroment$(COLOR_NC)"
	echo "$(COLOR_LIGHT_GREEN)--$(COLOR_NC)"

run:
	poetry run python3 main.py
