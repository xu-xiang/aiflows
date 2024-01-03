# GitHub API FastAPI Documentation

## Install

```bash
docker run --name github_api -d -p 10002:9000 -e TOKENS='token1,token2,token3,token4'  registry.cn-hangzhou.aliyuncs.com/aiflows/github_api
```

## API Overview

This FastAPI application provides several endpoints to interact with. The API version is `0.1.0`.

### Endpoints

#### POST `/search/code`

- **Summary**: Api Search Code
- **Request Body**:
    - Content Type: `application/json`
    - Schema: `#/components/schemas/SearchCodeRequest`
        - `keyword`: Keyword (string)
        - `per_page`: Per Page ()
        - `max_results`: Max Results ()
        - `extra_params`: Extra Params ()
        - `highlight`: Highlight (boolean)
- **Responses**:
    - `200`: Successful Response
    - `422`: Validation Error
        - Schema: `#/components/schemas/HTTPValidationError`
        - `detail`: Detail (array)

#### POST `/get/file_content`

- **Summary**: Api Get File Content
- **Request Body**:
    - Content Type: `application/json`
    - Schema: `#/components/schemas/GetFileContentRequest`
        - `url`: Url (string)
        - `repo_name`: Repo Name (string)
        - `file_path`: File Path (string)
        - `branch`: Branch (string)
- **Responses**:
    - `200`: Successful Response
    - `422`: Validation Error
        - Schema: `#/components/schemas/HTTPValidationError`
        - `detail`: Detail (array)

#### POST `/get/repository_readme`

- **Summary**: Api Get Repository Readme
- **Request Body**:
    - Content Type: `application/json`
    - Schema: `#/components/schemas/GetRepositoryReadmeRequest`
        - `owner`: Owner (string)
        - `repo`: Repo (string)
        - `ref`: Ref (string)
- **Responses**:
    - `200`: Successful Response
    - `422`: Validation Error
        - Schema: `#/components/schemas/HTTPValidationError`
        - `detail`: Detail (array)

#### GET `/get/rate_limits`

- **Summary**: Api Get Rate Limits
- **Responses**:
    - `200`: Successful Response

#### POST `/search/repositories`

- **Summary**: Api Search Repositories
- **Request Body**:
    - Content Type: `application/json`
    - Schema: `#/components/schemas/SearchRepositoriesRequest`
        - `keyword`: Keyword (string)
        - `per_page`: Per Page (integer)
        - `max_results`: Max Results (integer)
- **Responses**:
    - `200`: Successful Response
    - `422`: Validation Error
        - Schema: `#/components/schemas/HTTPValidationError`
        - `detail`: Detail (array)

#### POST `/user/starred`

- **Summary**: Fetch User Starred Repos
- **Request Body**:
    - Content Type: `application/json`
    - Schema: `#/components/schemas/StarredReposRequest`
        - `username`: Username (string)
        - `max_repos`: Max Repos ()
        - `per_page`: Per Page (integer)
- **Responses**:
    - `200`: Successful Response
    - `422`: Validation Error
        - Schema: `#/components/schemas/HTTPValidationError`
        - `detail`: Detail (array)

#### POST `/get/repository_info`

- **Summary**: Api Get Repository Info
- **Request Body**:
    - Content Type: `application/json`
    - Schema: `#/components/schemas/RepositoryInfoRequest`
        - `owner`: Owner (string)
        - `repo`: Repo (string)
        - `include_readme`: Include Readme (boolean)
- **Responses**:
    - `200`: Successful Response
    - `422`: Validation Error
        - Schema: `#/components/schemas/HTTPValidationError`
        - `detail`: Detail (array)

