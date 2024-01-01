import re
import base64


async def get_file_content_impl(client, url=None, repo_name=None, file_path=None, branch=None):
    # 从 URL 中提取仓库名和文件路径
    if url:
        # 仅匹配标准 GitHub 文件 URL 格式
        match = re.search(r"github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.+)", url)
        if match:
            repo_user, repo_name, branch, file_path = match.groups()
            repo_name = f"{repo_user}/{repo_name}"
        else:
            # 非标准 GitHub 文件 URL 格式
            raise NotImplementedError(
                "Only standard GitHub file URLs are supported(html_url). Please use the format: "
                "'https://github.com/[username]/[repository]/blob/[branch]/[file-path]'."
            )

    if not repo_name or not file_path:
        raise ValueError("Repository name and file path are required.")

    endpoint = f"/repos/{repo_name}/contents/{file_path}"
    params = {"ref": branch} if branch else {}
    response = await client.fetch_github_api(endpoint, params)
    content = response.get('content')
    return base64.b64decode(content).decode('utf-8') if content else None
