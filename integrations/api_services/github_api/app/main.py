from typing import Optional, Dict, Any

import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel
from github_api.client.async_client import AsyncGitHubClient
import logging
from utils import load_environment_variables, handle_exception

# 初始化 FastAPI 应用
app = FastAPI()

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 环境变量配置
tokens, concurrency = load_environment_variables()

client = AsyncGitHubClient(tokens, concurrency, log_level=logging.DEBUG)


# 输入模型
class SearchCodeRequest(BaseModel):
    keyword: str
    per_page: Optional[int] = 100
    max_results: Optional[int] = 1000
    extra_params: Optional[Dict[str, Any]] = None
    highlight: bool = False


class GetFileContentRequest(BaseModel):
    url: str = None
    repo_name: str = None
    file_path: str = None
    branch: str = None


class GetRepositoryReadmeRequest(BaseModel):
    owner: str
    repo: str
    ref: str = None


class SearchRepositoriesRequest(BaseModel):
    keyword: str
    per_page: int = 100
    max_results: int = 1000


@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    return handle_exception(request, exc)


@app.post("/search/code")
async def api_search_code(request: SearchCodeRequest):
    headers = {}
    if request.highlight:
        headers["Accept"] = "application/vnd.github.v3.text-match+json"
    results = await client.search_code(query=request.keyword, per_page=request.per_page,
                                       max_results=request.max_results, extra_params=request.extra_params,
                                       extra_headers=headers)
    return results


@app.post("/get/file_content")
async def api_get_file_content(request: GetFileContentRequest):
    content = await client.get_file_content(url=request.url, repo_name=request.repo_name, file_path=request.file_path,
                                            branch=request.branch)
    return {"content": content}


@app.post("/get/repository_readme")
async def api_get_repository_readme(request: GetRepositoryReadmeRequest):
    readme = await client.get_readme(owner=request.owner, repo=request.repo, ref=request.ref)
    return {"readme": readme}


@app.get("/get/rate_limits")
async def api_get_rate_limits():
    limits = await client.get_rate_limits()
    return {"rate_limits": limits}


@app.post("/search/repositories")
async def api_search_repositories(request: SearchRepositoriesRequest):
    results = await client.search_repositories(query=request.keyword, per_page=request.per_page,
                                               max_results=request.max_results)
    return results


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
