import httpx


def fetch_openapi_data(url):
    try:
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        print(f"An HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None


def generate_markdown(api_json):
    markdown = "# GitHub API FastAPI Documentation\n\n"

    # Installation
    markdown += "## Install\n\n```bash\ndocker run --name github_api -d -p 10002:9000 -e TOKENS='token1,token2,token3,token4'  registry.cn-hangzhou.aliyuncs.com/aiflows/github_api\n```\n\n"

    # API Overview
    markdown += "## API Overview\n\nThis FastAPI application provides several endpoints to interact with. The API version is `0.1.0`.\n\n"

    # Endpoints
    markdown += "### Endpoints\n\n"
    for path, methods in api_json['paths'].items():
        for method, details in methods.items():
            markdown += f"#### {method.upper()} `{path}`\n\n"
            markdown += f"- **Summary**: {details['summary']}\n"
            if 'requestBody' in details:
                markdown += "- **Request Body**:\n"
                for content_type, schema in details['requestBody']['content'].items():
                    markdown += f"    - Content Type: `{content_type}`\n"
                    schema_ref = schema['schema']['$ref']
                    markdown += f"    - Schema: `{schema_ref}`\n"
                    markdown += describe_schema(schema_ref, api_json['components']['schemas'])
            markdown += "- **Responses**:\n"
            for status, response in details['responses'].items():
                markdown += f"    - `{status}`: {response['description']}\n"
                for content_type, schema in response.get('content', {}).items():
                    schema_ref = schema.get('schema', {}).get('$ref')
                    if schema_ref:
                        markdown += f"        - Schema: `{schema_ref}`\n"
                        markdown += describe_schema(schema_ref, api_json['components']['schemas'])
            markdown += "\n"

    return markdown


def describe_schema(ref, schemas):
    ref = ref.split('/')[-1]
    schema = schemas.get(ref)
    if not schema:
        return "    - No detailed schema information available.\n"

    description = ""
    for prop, prop_details in schema.get('properties', {}).items():
        description += f"        - `{prop}`: {prop_details.get('title', '')} ({prop_details.get('type', '')})\n"
    return description


# Example usage
api_url = 'http://127.0.0.1:9000/openapi.json'
api_json_data = fetch_openapi_data(api_url)

if api_json_data:
    markdown_output = generate_markdown(api_json_data)

    # Output to a file or print
    with open('../README.md', 'w') as md_file:
        md_file.write(markdown_output)
else:
    print("Failed to fetch API data.")
