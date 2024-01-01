from typing import List, Optional, Dict, Any
import asyncio


async def code_search_impl(client, query: str, per_page: int = 100, max_results: int = 1000,
                           extra_params: Optional[Dict[str, Any]] = None, extra_headers: Optional[dict] = None) -> List[dict]:
    # 处理额外的参数
    search_params = {"q": query, "per_page": per_page}
    if extra_params:
        search_params.update(extra_params)
    # 获取第一页数据和总计数
    first_page_response = await client.fetch_github_api("/search/code", {**search_params, "page": 1},
                                                        headers=extra_headers)
    total_count = first_page_response.get('total_count', 0)

    # 计算总页数，考虑最大结果限制
    total_pages = min(-(-total_count // per_page), -(-max_results // per_page))

    # 如果只有一页，直接返回结果
    if total_pages <= 1:
        return first_page_response.get('items', [])

    # 并行获取剩余页的数据
    tasks = [asyncio.create_task(client.fetch_github_api("/search/code", {**search_params, "page": page}))
             for page in range(2, total_pages + 1)]  # 从第二页开始
    responses = await asyncio.gather(*tasks)
    all_items = first_page_response.get('items', [])
    for response in responses:
        all_items.extend(response.get('items', []))
    return all_items
