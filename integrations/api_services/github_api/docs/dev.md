# 开发指南：FastAPI 项目中新增 API 接口

本开发指南提供了在 FastAPI 项目中新增 API 接口的标准流程，以下步骤将指导您如何从创建接口逻辑开始，到定义路由，以及进行测试和文档更新。

## 1. 创建接口逻辑

首先，您需要创建接口的核心逻辑。这通常涉及到调用外部服务或执行业务逻辑。

### 示例：

假设您要添加一个用于搜索 GitHub 代码的接口：

1. 新增文件 github_api/api/code_search.py。

2. 实现功能：在 code_search.py 中实现 code_search_impl 方法。

```python
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
```

## 2. 修改客户端类

在客户端类中添加一个方法，该方法将调用您刚刚创建的接口逻辑。

### 示例：

修改 `github_api/client/async_client.py` ：

```python
# github_api/client/async_client.py

from github_api.api.code_search import code_search_impl


class AsyncGitHubClient:
    # 现有代码...

    async def search_code(self, query: str, per_page: int = 100, max_results: int = 1000, extra_params=None,
                          extra_headers=None):
        return await code_search_impl(self, query, per_page, max_results, extra_params, extra_headers)

```

## 3. 定义 Pydantic 模型

创建 Pydantic 模型来处理输入数据。这将用于验证和解析进入 API 的数据。

### 示例：

```python
# 在适当的文件中定义模型

from pydantic import BaseModel


class SearchCodeRequest(BaseModel):
    keyword: str
    per_page: int
    max_results: int
    extra_params: dict
    highlight: bool

```

## 4. 定义 FastAPI 路由

在 FastAPI 应用中定义一个新的路由，使用 Pydantic 模型作为输入，并调用客户端类中的方法。

### 示例：

```python
# 在 main.py 或适当的路由模块中

from fastapi import FastAPI
from your_model_module import SearchCodeRequest


@app.post("/search/code")
async def api_search_code(request: SearchCodeRequest):
    return await client.search_code(query=request.keyword, per_page=request.per_page, max_results=request.max_results,
                                    extra_params=request.extra_params, extra_headers=request.highlight)
```

## 5. 添加 HTTP 测试

为新的接口添加 HTTP 测试用例，以便于进行接口测试。

### 示例：

在 app/test/github_api_test.http 中添加：

```python
###
# 测试搜索代码的接口
POST
{{host}} / search / code
Content - Type: application / json

{
    "keyword": "CVE-2022-24990",
    "per_page": 100,
    "max_results": 1000,
    "extra_params": {},
    "highlight": true
}
```
运行FastAPI服务并完成接口测试
```bash
python main.py
```

## 6. 更新文档

执行脚本或手动更新项目的 README 文档，以包含新添加的接口信息。

### 示例：

在 `utils` 目录下执行 `json2markdown.py` 来生成更新后的 Readme 文档。

```bash
python json2markdown.py

```

这将读取 JSON 格式的 API 信息，并转换为 Markdown 格式的文档。

