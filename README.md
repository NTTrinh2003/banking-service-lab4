# Banking AI-Agent — Triển khai đa dịch vụ (gRPC + Docker)

Project 4 — Applications of NLP in Industry. Một AI agent hỗ trợ khách hàng cho
ngân hàng, được tách từ bản prototype chạy cục bộ thành một hệ thống nhiều
container có thể tái lập (reproducible).

## 1. Kiến trúc microservice

```
        Customer
           │ HTTP
           ▼
   ┌───────────────┐        ┌────────────────────┐
   │   frontend    │  HTTP  │      backend       │
   │  (Streamlit)  │ ─────► │  (FastAPI gateway) │
   │   :8501       │        │      :8000         │
   └───────────────┘        └─────────┬──────────┘
                                       │ gRPC :50051
                                       ▼
                              ┌────────────────────┐
                              │   intent-service   │
                              │   (gRPC server)    │
                              │      :50051        │
                              └─────────┬──────────┘
                                        │ HTTP
        backend và intent-service đều   │
        gọi Ollama qua HTTP ────────────┴─────► Ollama (gpt-oss:20b)
```

**Luồng xử lý bên trong backend (agentic pipeline):**

`intent (qua gRPC) → priority + policy → draft (qua Ollama) → validation → router`

### Vai trò của từng container

| Container        | Vai trò |
|------------------|---------|
| `frontend`       | Giao diện Streamlit. Gửi tin nhắn của khách hàng tới backend, hiển thị câu trả lời và toàn bộ trace. Chỉ giao tiếp với backend. |
| `backend`        | **API Gateway** viết bằng FastAPI. Điều phối toàn bộ workflow: gọi `intent-service` qua gRPC, chạy các node priority/policy/validation/router, gọi Ollama để sinh draft, và trả về kết quả có cấu trúc. |
| `intent-service` | Microservice **gRPC** độc lập. Phân loại tin nhắn thành intent bằng Ollama, trả về `{intent, confidence, reason}`. |
| Ollama           | Phục vụ mô hình `gpt-oss:20b` cho việc phân loại intent và sinh câu trả lời. Chạy riêng (ví dụ trên Colab, được expose qua Pinggy). |

## 2. Yêu cầu môi trường

- Docker + Docker Compose.
- Một **Ollama** đang chạy với mô hình `gpt-oss:20b`. Cách đơn giản nhất là dùng
  notebook `Ollama.ipynb` trên Google Colab: nó sẽ cài Ollama, tải mô hình, và
  expose ra ngoài bằng Pinggy tunnel
  (`ssh -p 443 -R0:localhost:11434 qr@a.pinggy.io`). Hãy copy URL công khai mà nó
  in ra (dạng `https://xxxx.a.free.pinggy.link`).

## 3. Cấu hình URL của Ollama

```bash
cp .env.example .env
# mở .env và đặt OLLAMA_BASE_URL bằng URL Pinggy của bạn
```

> Lưu ý quan trọng: bên trong một container, `localhost` chính là container đó,
> không phải máy của bạn hay Colab. URL của Ollama phải truy cập được từ bên trong
> các container — đó là lý do ta dùng URL công khai của Pinggy.

## 4. Sinh mã gRPC từ file .proto

Các file stub đã có sẵn trong dự án, nhưng nếu cần sinh lại (ví dụ sau khi sửa
`.proto`):

```bash
cd intent_service
make            # chạy grpc_tools.protoc -> intent_service_pb2.py, intent_service_pb2_grpc.py
```

Backend dùng một bản sao của các stub này trong `backend/app/clients/intent_grpc/`.
Nếu sinh lại, hãy copy chúng sang đó và sửa dòng import ở đầu file
`intent_service_pb2_grpc.py` thành `from . import intent_service_pb2 as ...`.

(Dockerfile của intent-service cũng chạy `make` lúc build, nên image luôn khớp với
`.proto` hiện tại.)

> Ghi chú phiên bản: các stub được sinh bằng protobuf 6.x, vì vậy `requirements.txt`
> dùng `grpcio==1.80.0` và `grpcio-tools==1.80.0` để runtime protobuf khớp với mã đã sinh.

## 5. Build các Docker image

```bash
docker compose build
```

## 6. Chạy toàn bộ hệ thống

```bash
docker compose up
```

Sau đó truy cập:

- Giao diện frontend: http://localhost:8501
- API docs:           http://localhost:8000/docs

## 7. Gọi trực tiếp API Gateway

```bash
# kiểm tra trạng thái
curl http://localhost:8000/health

# xem cấu hình
curl http://localhost:8000/config

# chạy toàn bộ agent
curl -X POST http://localhost:8000/run-agent \
  -H "Content-Type: application/json" \
  -d '{"message": "I lost my credit card, please block it"}'
```

Kết quả trả về gồm `final_reply`, hành động định tuyến `action`, và toàn bộ `trace`
(intent → priority → policy → draft → validation → router).

## 8. Kiểm thử riêng intent-service (tùy chọn)

```bash
cd intent_service
pip install -r requirements.txt
python server.py            # cửa sổ terminal 1
python client.py "I cannot transfer money"   # cửa sổ terminal 2
```

## Ghi chú / phương án thay thế

- **Dùng mô hình LoRA từ Lab 2 thay cho Ollama để phân loại intent:** chỉ cần thay
  phần thân của `intent_service/app/nodes/intent_node.py` để load và chạy mô hình
  Llama-3.2-1B đã fine-tune. Hợp đồng gRPC và mọi phần còn lại giữ nguyên — đó chính
  là lợi ích của việc tách dịch vụ. Lưu ý khi đó image sẽ cần trọng số mô hình (và
  tốt nhất là GPU), nên mặc định dự án dùng Ollama.
- Nếu Ollama chạy ngay trên máy của bạn (không phải Colab), đặt
  `OLLAMA_BASE_URL=http://host.docker.internal:11434` trong `.env`.
