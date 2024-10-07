PROTOBUF_FOLDER = ../grpc-proto
PROTOBUF_FILE_PATH = $(PROTOBUF_FOLDER)/stt.proto
PROTOBUF_OUTPUT = ./generated/protobuf/

COLOR_LIGHT_GREEN=\e[1;32m
COLOR_LIGHT_BLUE=\e[1;34m
COLOR_NC=\e[0m

protobuf: $(PROTOBUF_FILE_PATH)
	./.venv/bin/python3 -m grpc_tools.protoc -I$(PROTOBUF_FOLDER) \
		--python_out=$(PROTOBUF_OUTPUT) --pyi_out=$(PROTOBUF_OUTPUT) --grpc_python_out=$(PROTOBUF_OUTPUT) \
		$(PROTOBUF_FILE_PATH)

setup:
	python3 -m venv .venv
	./.venv/bin/pip install -r ./requirements.txt -q
	make protobuf
	echo "$(COLOR_LIGHT_GREEN)--$(COLOR_NC)"
	echo "$(COLOR_LIGHT_GREEN)-- run $(COLOR_LIGHT_BLUE)'source .venv/bin/activate'$(COLOR_LIGHT_GREEN) to enter the virtual enviroment$(COLOR_NC)"
	echo "$(COLOR_LIGHT_GREEN)--$(COLOR_NC)"
