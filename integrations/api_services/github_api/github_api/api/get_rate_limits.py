# rate_limits_impl.py
import asyncio
from typing import List


async def get_rate_limits_impl(fetch_github_api, tokens: List[str]) -> str:
    """获取 GitHub API 的限速信息"""

    async def fetch_limit_data(token_index):
        try:
            rate_limit_data = await fetch_github_api('/rate_limit')
            limits = rate_limit_data['resources']
            formatted_limit = f"Token {token_index + 1}: "
            for category, limit_info in limits.items():
                remaining = limit_info['remaining']
                limit = limit_info['limit']
                formatted_limit += f"{category.capitalize()} {remaining}/{limit}; "
            return formatted_limit
        except Exception as e:
            return f"Token {token_index + 1}: Error - {str(e)}"

    tasks = [fetch_limit_data(index) for index, _ in enumerate(tokens)]
    results = await asyncio.gather(*tasks)

    formatted_limits = "GitHub API Rate Limits: \n" + "\n".join(results)
    return formatted_limits
