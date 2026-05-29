GRPC_SOURCES = intent_service_pb2.py intent_service_pb2_grpc.py

all: $(GRPC_SOURCES)

# Regenerate the gRPC Python code whenever the .proto changes.
# -I.            : look for imports in the current directory
# --python_out=. : generate the message classes (intent_service_pb2.py)
# --grpc_python_out=. : generate the client stub + server base class (intent_service_pb2_grpc.py)
$(GRPC_SOURCES): intent_service.proto
	python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. intent_service.proto

clean:
	rm -f $(GRPC_SOURCES)
