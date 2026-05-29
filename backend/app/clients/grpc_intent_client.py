import grpc

from app.clients.intent_grpc import intent_service_pb2, intent_service_pb2_grpc
from app.core.settings import settings


class GrpcIntentClient:
    def __init__(self, target: str | None = None):
        self.target = target or settings.intent_service_target

    def recognize(self, message: str):
        with grpc.insecure_channel(self.target) as channel:
            stub = intent_service_pb2_grpc.IntentServiceStub(channel)
            resp = stub.IntentRecognizer(
                intent_service_pb2.IntentRequest(message=message)
            )
        return resp.intent, resp.confidence, resp.reason
