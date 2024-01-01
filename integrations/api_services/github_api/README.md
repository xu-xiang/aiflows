# GitHub API FastAPI Documentation

## API Overview
This FastAPI application provides several endpoints to interact with. The API version is `0.1.0`.

### Endpoints

#### 1. POST `/search/code`
   - **Summary**: Api Search Code
   - **Request**: Requires a JSON body with schema `SearchCodeRequest`.
     - `keyword` (string): Keyword for search.
     - `per_page` (integer, optional, default=100): Number of results per page.
     - `max_results` (integer, optional, default=1000): Maximum number of results.
     - `extra_params` (object, optional): Additional parameters for search.
     - `highlight` (boolean, optional, default=false): Highlight search results.
   - **Responses**:
     - `200`: Successful Response
     - `422`: Validation Error

#### 2. POST `/get/file_content`
   - **Summary**: Api Get File Content
   - **Request**: Requires a JSON body with schema `GetFileContentRequest`.
     - `url` (string): URL of the file.
     - `repo_name` (string): Repository name.
     - `file_path` (string): Path to the file.
     - `branch` (string): Repository branch.
   - **Responses**:
     - `200`: Successful Response
     - `422`: Validation Error

#### 3. POST `/get/repository_readme`
   - **Summary**: Api Get Repository Readme
   - **Request**: Requires a JSON body with schema `GetRepositoryReadmeRequest`.
     - `owner` (string): Owner of the repository.
     - `repo` (string): Repository name.
     - `ref` (string): Reference branch or tag.
   - **Responses**:
     - `200`: Successful Response
     - `422`: Validation Error

#### 4. GET `/get/rate_limits`
   - **Summary**: Api Get Rate Limits
   - **Responses**:
     - `200`: Successful Response

#### 5. POST `/search/repositories`
   - **Summary**: Api Search Repositories
   - **Request**: Requires a JSON body with schema `SearchRepositoriesRequest`.
     - `keyword` (string): Keyword for search.
     - `per_page` (integer, default=100): Number of results per page.
     - `max_results` (integer, default=1000): Maximum number of results.
   - **Responses**:
     - `200`: Successful Response
     - `422`: Validation Error

### Schemas
- `GetFileContentRequest`: Request schema for getting file content.
- `GetRepositoryReadmeRequest`: Request schema for getting repository readme.
- `HTTPValidationError`: Schema for HTTP validation errors.
- `SearchCodeRequest`: Request schema for searching code.
- `SearchRepositoriesRequest`: Request schema for searching repositories.
- `ValidationError`: Schema for validation errors.

## Usage

### Running the API
To start the FastAPI server, run:
```bash
uvicorn main:app --reload
```

Replace `main:app` with the actual module and app instance names.

### Interacting with the API
You can interact with the API by sending HTTP requests to the endpoints listed above. Each endpoint might require specific request parameters or body as described.

## Contributing
Contributions to this API are welcome. Please follow the standard procedures for submitting issues or pull requests.