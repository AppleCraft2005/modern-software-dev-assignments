# Regional Indonesia MCP Server 🇮🇩

A Model Context Protocol (MCP) server that wraps the [goapi.io](https://goapi.io/) Regional Indonesia API. This server allows MCP-aware clients (such as Claude Desktop and Cursor) to retrieve structured data about provinces, cities, and regencies in Indonesia.

This project uses **STDIO transport** for local deployment and implements **Authentication** by securely passing the API key via environment variables. It also features robust error handling for API timeouts, rate limits, and empty responses.

## Prerequisites

1. **Python 3.10+**: It is recommended to use a virtual environment (e.g., Conda).
2. **API Key**: Register a free account at [goapi.io](https://goapi.io/) to obtain your `api_key`.
3. **Dependencies**: 
   Install the required Python packages by running:
   ```bash
   pip install mcp httpx
   ```

## Environment Setup & Run Instructions (Local STDIO)

Since this server uses STDIO transport, it is designed to be executed directly by an MCP client rather than running standalone. However, to test it manually via the MCP Inspector, you can run:

**Windows (CMD/PowerShell):**
```cmd
set GOAPI_KEY=[INSERT_YOUR_API]
npx @modelcontextprotocol/inspector python server/main.py
```

**Mac/Linux:**
```bash
export GOAPI_KEY=[INSERT_YOUR_API]
npx @modelcontextprotocol/inspector python server/main.py
```

## Configuring the MCP Client (Claude Desktop)

To use this server with Claude Desktop, update your Claude Desktop configuration file. 

1. Open the configuration file located at:
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   - **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
2. Add the following configuration under the `"mcpServers"` object. Make sure to replace the paths and API key with your actual local paths:

```json
{
  "mcpServers": {
    "regional-indonesia": {
      "command": "[INSERT_PYTHON_CONDA_PATH]",
      "args": [
        "[INSERT_main.py_PROJECT_PATH]"
      ],
      "env": {
        "GOAPI_KEY": "[INSERT_YOUR_API]"
      }
    }
  }
}
```
3. Save the file and completely restart Claude Desktop. Then check setting > Developer, it should be 'running' by now

## Example Invocation Flow in Claude Desktop

Once configured, you can trigger the tools using natural language prompts in Claude Desktop. 

**User Prompt:**
> "Tolong carikan ID provinsi Kalimantan Selatan, lalu cari daftar kotanya."

**Expected Behavior:**
1. Claude automatically calls `get_provinsi` to search for the ID of "Kalimantan Selatan".
2. Claude automatically passes the retrieved ID into the `get_kota` tool.
3. Claude synthesizes the final JSON response into a natural language reply, listing the cities and regencies found in that province.

## Tool Reference

### 1. `get_provinsi`
- **Description:** Retrieves a complete list of all provinces in Indonesia along with their unique IDs. Used primarily to find the ID of a specific province.
- **Parameters:** None.
- **Example Output (Snippet):**
  ```json
  [
    {"id": "61", "name": "Kalimantan Barat"},
    {"id": "62", "name": "Kalimantan Tengah"},
    {"id": "63", "name": "Kalimantan Selatan"}
  ]
  ```

### 2. `get_kota`
- **Description:** Retrieves a complete list of regencies and cities (Kabupaten/Kota) for a specific province.
- **Parameters:** - `provinsi_id` (string): The unique ID of the province (obtained from `get_provinsi`).
- **Example Input:** `{"provinsi_id": "63"}`
- **Example Output (Snippet):**
  ```json
  [
    {"id": "63.71", "provinsi_id": "63", "name": "Kota Banjarmasin"},
    {"id": "63.72", "provinsi_id": "63", "name": "Kota Banjarbaru"}
  ]
  ```