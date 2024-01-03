from .get_readme import get_readme_impl


async def repository_info_impl(client, owner: str, repo: str, include_readme: bool = False) -> dict:
    response = await client.fetch_github_api(f"/repos/{owner}/{repo}")

    if include_readme:
        readme_response = await get_readme_impl(client, owner, repo)
        response['readme'] = readme_response.get('decoded_content')

    return response
