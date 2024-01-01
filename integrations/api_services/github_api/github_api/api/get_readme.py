import base64


async def get_readme_impl(client, owner, repo, ref=None):
    endpoint = f"/repos/{owner}/{repo}/readme"
    params = {}
    if ref:
        params['ref'] = ref

    response = await client.fetch_github_api(endpoint, params)

    # 解码 Base64 编码的 README 内容
    if 'content' in response:
        decoded_content = base64.b64decode(response['content']).decode('utf-8')
        response['decoded_content'] = decoded_content

    return response
