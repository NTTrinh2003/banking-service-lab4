from concurrent import futures

import grpc

import intent_service_pb2
import intent_service_pb2_grpc
from app.core.settings import settings
from app.nodes.intent_node import predict_intent


class IntentServiceServicer(intent_service_pb2_grpc.IntentServiceServicer):
    def IntentRecognizer(self, request, context):
        prediction = predict_intent(request.message)
        return intent_service_pb2.IntentResponse(
            intent=prediction.intent,
            confidence=prediction.confidence,
            reason=prediction.reason,
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    intent_service_pb2_grpc.add_IntentServiceServicer_to_server(
        IntentServiceServicer(), server
    )
    # bind on 0.0.0.0 so other containers can reach it
    bind_addr = f"0.0.0.0:{settings.GRPC_PORT}"
    server.add_insecure_port(bind_addr)
    server.start()
    print(f"[intent-service] gRPC server listening on {bind_addr}", flush=True)
    print(f"[intent-service] Ollama: {settings.OLLAMA_BASE_URL} "
          f"model={settings.INTENT_MODEL_NAME}", flush=True)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
