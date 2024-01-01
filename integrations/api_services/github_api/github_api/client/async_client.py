from typing import Optional, List

import httpx
import asyncio
import time
import logging

from github_api.api.get_file_content import get_file_content_impl
from github_api.api.get_readme import get_readme_impl
from github_api.utils.logger import setup_logger
from github_api.api.code_search import code_search_impl
from github_api.api.repositories_search import search_repositories_impl
from github_api.api.get_rate_limits import get_rate_limits_impl


class AsyncGitHubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self, tokens: List[str], concurrency: int = 5, log_level=logging.INFO, max_retries: int = 2):
        self.tokens = tokens
        self.concurrency = concurrency
        self.max_retries = max_retries
        self.token_index = 0
        self.lock = asyncio.Lock()
        self.semaphore = asyncio.Semaphore(concurrency)
        self.logger = setup_logger(__name__, log_level)

    async def _get_client(self):
        async with self.lock:
            token = self.tokens[self.token_index]
            self.token_index = (self.token_index + 1) % len(self.tokens)
            return httpx.AsyncClient(base_url=self.BASE_URL, headers={"Authorization": f"token {token}"})

    async def fetch_github_api(self, endpoint: str, params: Optional[dict] = None, headers: Optional[dict] = None,
                               retries: int = 0) -> dict:
        async with self.semaphore:
            async with await self._get_client() as client:
                # 支持自定义请求头
                if headers:
                    client.headers.update(headers)
                url = f"{self.BASE_URL}{endpoint}"
                self.logger.debug(
                    f"Fetching URL: {url} with params: {params} with header: {client.headers.get('Authorization')}")
                response = await client.get(endpoint, params=params)

                if response.status_code == 403 and 'rate limit exceeded' in response.text:
                    if retries < self.max_retries:
                        await self._handle_rate_limit(client)
                        return await self.fetch_github_api(endpoint, params, headers, retries + 1)
                    else:
                        raise httpx.HTTPStatusError("Rate limit exceeded", request=response.request, response=response)

                response.raise_for_status()
                return response.json()

    async def _handle_rate_limit(self, client):
        rate_limit_info = await client.get('/rate_limit')
        rate_limit_info.raise_for_status()
        reset_time = rate_limit_info.json()['resources']['core']['reset']
        sleep_duration = max(0, reset_time - time.time())
        self.logger.info(f"Rate limit exceeded. Sleeping for {sleep_duration} seconds.")
        await asyncio.sleep(sleep_duration)

    async def search_code(self, query: str, per_page: int = 100, max_results: int = 1000, extra_params=None,
                          extra_headers=None) -> List[dict]:
        # if extra_params is None:
        #     extra_params = {"sort": "indexed", "order": "desc"}
        return await code_search_impl(self, query, per_page, max_results, extra_params, extra_headers)

    async def search_repositories(self, query: str, per_page: int = 100, max_results: int = 1000):
        return await search_repositories_impl(self, query, per_page, max_results)

    async def get_readme(self, owner, repo, ref=None):
        return await get_readme_impl(self, owner, repo, ref)

    async def get_file_content(self, url=None, repo_name=None, file_path=None, branch=None):
        return await get_file_content_impl(self, url, repo_name, file_path, branch)

    async def get_rate_limits(self) -> str:
        return await get_rate_limits_impl(self.fetch_github_api, self.tokens)
