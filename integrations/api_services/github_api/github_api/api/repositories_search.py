import asyncio


async def search_repositories_impl(client, query: str, per_page: int = 100, max_results: int = 1000):
    endpoint = "/search/repositories"
    first_page_response = await client.fetch_github_api(endpoint, {"q": query, "per_page": per_page})
    total_count = first_page_response.get('total_count', 0)
    total_pages = min(-(-total_count // per_page), -(-max_results // per_page))
    if total_pages <= 1:
        return first_page_response.get('items', [])
    tasks = [asyncio.create_task(client.fetch_github_api(endpoint, {"q": query, "per_page": per_page, "page": page}))
             for page in range(2, total_pages + 1)]
    responses = await asyncio.gather(*tasks)
    return [item for response in responses for item in response.get('items', [])]
