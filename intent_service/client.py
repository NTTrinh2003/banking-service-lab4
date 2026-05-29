# Quick manual test:  python client.py "I lost my credit card"
import sys

import grpc

import intent_service_pb2
import intent_service_pb2_grpc


def main():
    message = sys.argv[1] if len(sys.argv) > 1 else "I cannot transfer money to my friend"
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = intent_service_pb2_grpc.IntentServiceStub(channel)
        response = stub.IntentRecognizer(
            intent_service_pb2.IntentRequest(message=message)
        )
    print("message:    ", message)
    print("intent:     ", response.intent)
    print("confidence: ", response.confidence)
    print("reason:     ", response.reason)


if __name__ == "__main__":
    main()
