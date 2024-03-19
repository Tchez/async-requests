import asyncio, time, base64
from service import AsyncRequestService


async def main():
    service = AsyncRequestService(
        "http://localhost:8000",
        max_at_once=10,
        max_per_second=10,
    )

    credentials = base64.b64encode(f"user:password".encode("utf-8")).decode("utf-8")
    headers = {"Authorization": f"Basic {credentials}"}

    requests = [
        {
            "method": "POST",
            "url": "/get-context",
            "body": {"user_id": f"user_{i}", "question": "Produto para carrapato"},
            "headers": headers,
        }
        for i in range(45)
    ]

    def process_response(index, response):
        print(f"Requisição {index + 1} -> tempo total {response['time']:.2f} segundos")

    initial_time = time.time()
    await service.execute_requests(requests, process_response)
    final_time = time.time()
    print(f"Tempo total de execução: {final_time - initial_time:.2f} segundos")


asyncio.run(main())
