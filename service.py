import time

from typing import List, Dict, Callable, Any
from httpx import AsyncClient
from aiometer import run_all
from functools import partial


class AsyncRequestService:
    def __init__(self, base_url: str, max_at_once: int = 5, max_per_second: int = 10):
        """
        Inicializa o serviço de requisições assíncronas.

        :param base_url: URL base para as requisições HTTP.
        :param max_at_once: Número máximo de requisições concorrentes.
        :param max_per_second: Número máximo de requisições por segundo.
        """
        self.base_url = base_url
        self.max_at_once = max_at_once
        self.max_per_second = max_per_second

    async def fetch(
        self,
        session: AsyncClient,
        method: str,
        url: str,
        body: Any = None,
        headers: Dict[str, str] = None,
        params: Dict[str, str] = None,
    ) -> Any:
        """
        Executa uma requisição HTTP assíncrona com o método especificado e mede o tempo de execução.

        :return: Um dicionário com a resposta da requisição e o tempo de execução.
        """
        start_time = time.time()
        response = await session.request(
            method=method, url=url, json=body, headers=headers, params=params
        )
        end_time = time.time()
        total_time = end_time - start_time
        return {"response": response.json(), "time": total_time}

    async def execute_requests(
        self, requests: List[Dict], process_response: Callable = None
    ):
        async with AsyncClient(base_url=self.base_url, timeout=30) as session:
            tasks = [
                partial(
                    self.fetch,
                    session,
                    request["method"],
                    request["url"],
                    request.get("body"),
                    request.get("headers"),
                    request.get("params"),
                )
                for request in requests
            ]
            responses = await run_all(
                tasks, max_at_once=self.max_at_once, max_per_second=self.max_per_second
            )

            if process_response:
                for index, response in enumerate(responses):
                    process_response(index, response)
