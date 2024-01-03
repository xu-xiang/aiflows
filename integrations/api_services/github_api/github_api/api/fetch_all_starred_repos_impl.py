from typing import List


async def fetch_all_starred_repos_impl(client, username: str, max_repos: int = 1000, per_page: int = 100) -> List[dict]:
    """实现获取用户所有 star 的仓库"""
    endpoint = f"/users/{username}/starred"
    all_repos = []
    page = 1

    while True:
        response = await client.fetch_github_api(endpoint, params={"page": page, "per_page": per_page})
        all_repos.extend(response)
        if len(response) < per_page:
            break  # 达到最后一页或不足一页
        page += 1
        if max_repos and len(all_repos) >= max_repos:
            break  # 达到最大限制

    return all_repos[:max_repos]
