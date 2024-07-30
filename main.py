import asyncio, time, base64
from service import AsyncRequestService
from settings import Settings

settings = Settings()


async def main():
    service = AsyncRequestService(
        base_url=settings.BASE_URL,
        max_at_once=settings.MAX_AT_ONCE,
        max_per_second=settings.MAX_PER_SECOND,
    )

    # credentials = base64.b64encode(f"admin:asdf@1234".encode("utf-8")).decode(
    #     "utf-8"
    # )
    # headers = {"Authorization": f"Basic {credentials}"}

    requests = [
        {
            "method": settings.METHOD,
            "url": settings.ENDPOINT,
            "body": settings.BODY,
            "headers": settings.HEADERS,
        }
        for i in range(settings.TOTAL_REQUESTS)
    ]

    def process_response(index, response):
        print(
            f"Requisição {index + 1} -> tempo total {response['time']:.2f} segundos"
        )

    initial_time = time.time()
    await service.execute_requests(requests, process_response)
    final_time = time.time()
    print(f"Tempo total de execução: {final_time - initial_time:.2f} segundos")


asyncio.run(main())
