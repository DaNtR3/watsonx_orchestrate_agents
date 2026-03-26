# PokéAPI Connection and Tool Setup Guide

## Overview
This guide explains step-by-step how to connect your watsonx Orchestrate agent to the PokéAPI (https://pokeapi.co), a free RESTful API for Pokémon data. This guide is based on the actual IBM watsonx Orchestrate ADK source code and provides the correct implementation patterns.

---

## Table of Contents
1. [Understanding Connections](#understanding-connections)
2. [Connection Types in watsonx Orchestrate](#connection-types-in-watsonx-orchestrate)
3. [PokéAPI Connection Setup](#pokeapi-connection-setup)
4. [Tool Implementation](#tool-implementation)
5. [Configuration and Import](#configuration-and-import)
6. [Testing Your Tools](#testing-your-tools)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Understanding Connections

### What is a Connection?
A **connection** in watsonx Orchestrate is a secure way to manage credentials and configuration for external APIs. It stores:
- Where the API is located (base URL)
- How to authenticate (credentials)
- Environment-specific configurations (draft vs live)

### Why Use Connections?

**Without Connection (Bad):**
```python
def get_pokemon():
    # Hardcoded URL - BAD!
    url = "https://pokeapi.co/api/v2/pokemon/pikachu"
    response = requests.get(url)
```

**With Connection (Good):**
```python
from ibm_watsonx_orchestrate.run import connections

@tool(expected_credentials=[...])
def get_pokemon():
    creds = connections.key_value(APP_ID)
    base_url = creds.get('url')  # Retrieved from connection
    response = requests.get(f"{base_url}/pokemon/pikachu")
```

**Benefits:**
- ✅ **Security**: No hardcoded URLs or credentials
- ✅ **Flexibility**: Change API settings without code changes
- ✅ **Reusability**: Multiple tools share the same connection
- ✅ **Environment-specific**: Different configs for draft/live

---

## Connection Types in watsonx Orchestrate

Based on the IBM watsonx Orchestrate ADK source code (`src/ibm_watsonx_orchestrate/agent_builder/connections/types.py`), these are the **ONLY** supported connection types:

### Available ConnectionType Enum Values:

```python
class ConnectionType(str, Enum):
    BASIC_AUTH = 'basic_auth'
    BEARER_TOKEN = 'bearer_token'
    API_KEY_AUTH = 'api_key_auth'
    OAUTH2_AUTH_CODE = 'oauth2_auth_code'
    OAUTH2_PASSWORD = 'oauth2_password'
    OAUTH2_CLIENT_CREDS = 'oauth2_client_creds'
    OAUTH_ON_BEHALF_OF_FLOW = 'oauth_on_behalf_of_flow'
    OAUTH2_TOKEN_EXCHANGE = 'oauth2_token_exchange'
    KEY_VALUE = 'key_value_creds'
```

### ⚠️ Important: NO_AUTH Does Not Exist

**There is NO `NO_AUTH` connection type in watsonx Orchestrate.**

For public APIs that don't require authentication (like PokéAPI), use **`KEY_VALUE`** connection type to store the base URL.

### Connection Type Usage Table:

| ConnectionType | Use Case | Python Function | Returns |
|----------------|----------|-----------------|---------|
| `BASIC_AUTH` | Username/password | `connections.basic_auth(app_id)` | `.url`, `.username`, `.password` |
| `BEARER_TOKEN` | Token-based auth | `connections.bearer_token(app_id)` | `.url`, `.token` |
| `API_KEY_AUTH` | API key auth | `connections.api_key_auth(app_id)` | `.url`, `.api_key` |
| `OAUTH2_*` | OAuth flows | `connections.oauth2_*` | `.url`, `.access_token` |
| **`KEY_VALUE`** | **Public APIs / Custom** | `connections.key_value(app_id)` | **dict with custom keys** |

### KEY_VALUE Connection (For Public APIs)

The `KEY_VALUE` connection type is special:
- Returns a **dictionary** (not an object with properties)
- Can store any custom key-value pairs
- Perfect for public APIs that only need a URL
- Access values using `.get('key')` method

```python
# KEY_VALUE returns a dict
creds = connections.key_value('my-app-id')
base_url = creds.get('url')  # Access like a dictionary
custom_value = creds.get('custom_key')
```

---

## PokéAPI Connection Setup

### Step 1: Understanding PokéAPI

**PokéAPI Characteristics:**
- 🌐 **Base URL**: `https://pokeapi.co/api/v2`
- 🔓 **Authentication**: None required (public API)
- 📊 **Rate Limit**: ~100 requests per minute per IP
- 📚 **Documentation**: https://pokeapi.co/docs/v2
- 💰 **Cost**: Completely free

### Step 2: Create Connection YAML File

**File Location:** `connections/pokeapi_connection.yaml`

```yaml
# PokéAPI Connection Configuration
#
# This connection is for the PokéAPI (https://pokeapi.co)
# PokéAPI is a free, public API that doesn't require authentication
#
# Connection Type: KEY_VALUE (for public APIs with no authentication)
# Base URL: https://pokeapi.co/api/v2
#
# Note: watsonx Orchestrate does not have a NO_AUTH connection type.
# For public APIs, use KEY_VALUE to store the base URL.

spec_version: 1.0.0
kind: connection
app_id: pokeapi-connection

# Environment configurations
environments:
  # Draft environment configuration
  draft:
    kind: key_value
    type: team
  
  # Live environment configuration (optional)
  # Uncomment when ready to deploy to production
  # live:
  #   kind: key_value
  #   type: team
```

### Step 3: Connection File Explained

#### `spec_version: 1.0.0`
- Schema version for the connection file
- Always use `1.0.0` for current watsonx Orchestrate
- **Required field**

#### `kind: connection`
- Declares this YAML file as a connection resource
- Must be exactly `connection` (not `agent`, `tool`, etc.)
- **Required field at top level**

#### `app_id: pokeapi-connection`
- **Unique identifier** for this connection
- Used in Python tools to reference this connection
- Must be unique across your environment
- Use kebab-case naming convention
- **Required field**

#### `environments:` Section
- Contains environment-specific configurations
- **Required field** - must have at least one environment
- Supports `draft` and `live` environments

#### `draft:` Configuration
- Configuration for the **draft environment**
- Where you develop and test your agent
- Nested under `environments:`

#### `kind: key_value` (inside draft)
- The connection type (maps to `ConnectionType.KEY_VALUE`)
- For public APIs without authentication
- Stores custom key-value pairs
- Can also use `kv` as shorthand

#### `type: team`
- **team**: Credentials shared across all users
- **member**: Each user provides their own credentials
- For public APIs, always use `team`

---

## Tool Implementation

### Step 1: Understanding the Tool Structure

Here's the complete pattern for using connections in Python tools:

```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType, ExpectedCredentials
from ibm_watsonx_orchestrate.run import connections
import requests
from typing import Dict, Any

# Define the connection app_id
POKEAPI_APP_ID = 'pokeapi-connection'

@tool(
    name="get_pokemon_info",
    description="Retrieves detailed information about a Pokémon",
    expected_credentials=[
        ExpectedCredentials(app_id=POKEAPI_APP_ID, type=ConnectionType.KEY_VALUE)
    ]
)
def get_pokemon_info(pokemon_name: str) -> Dict[str, Any]:
    """
    Fetches Pokémon information from PokéAPI.
    
    Args:
        pokemon_name: Name or ID of the Pokémon
        
    Returns:
        Dictionary with Pokémon data or error message
    """
    try:
        # Step 1: Retrieve connection credentials
        creds = connections.key_value(POKEAPI_APP_ID)
        
        # Step 2: Get base URL from connection (KEY_VALUE returns a dict)
        base_url = creds.get('url')
        
        if not base_url:
            return {
                "error": "Connection configuration error: 'url' not found",
                "success": False
            }
        
        # Step 3: Build full URL and make request
        url = f"{base_url}/pokemon/{pokemon_name.lower()}"
        response = requests.get(url, timeout=10)
        
        # Step 4: Handle response
        if response.status_code == 404:
            return {"error": f"Pokémon '{pokemon_name}' not found", "success": False}
        
        response.raise_for_status()
        data = response.json()
        
        # Step 5: Return formatted data
        return {
            "success": True,
            "name": data["name"],
            "id": data["id"],
            "types": [t["type"]["name"] for t in data["types"]],
            # ... more fields
        }
        
    except requests.exceptions.Timeout:
        return {"error": "Request timed out", "success": False}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}", "success": False}
```

### Step 2: Key Components Explained

#### 1. Import Statements

```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType, ExpectedCredentials
from ibm_watsonx_orchestrate.run import connections
```

- `tool`: Decorator to register functions as tools
- `ConnectionType`: Enum of available connection types
- `ExpectedCredentials`: Class for declaring required connections
- `connections`: Module with functions to retrieve connection credentials

#### 2. Connection App ID

```python
POKEAPI_APP_ID = 'pokeapi-connection'
```

- Must match the `app_id` in your connection YAML file
- Use a constant to avoid typos
- Shared across all tools using this connection

#### 3. Expected Credentials Declaration

```python
expected_credentials=[
    ExpectedCredentials(app_id=POKEAPI_APP_ID, type=ConnectionType.KEY_VALUE)
]
```

**Important Notes:**
- ✅ **DO**: Use `ExpectedCredentials` class (proper type)
- ❌ **DON'T**: Use dict like `{"app_id": ..., "type": ...}` (causes type errors)
- The `expected_credentials` parameter tells watsonx Orchestrate:
  - Which connection this tool needs
  - What type of authentication to expect
  - Validates connection exists at import time

#### 4. Retrieving Connection Credentials

```python
creds = connections.key_value(POKEAPI_APP_ID)
base_url = creds.get('url')
```

**For KEY_VALUE connections:**
- Returns a **dictionary** (not an object)
- Access values using `.get('key')` method
- The 'url' key must be set when configuring the connection

**For other connection types:**
```python
# API Key
creds = connections.api_key_auth(APP_ID)
url = creds.url
api_key = creds.api_key

# Bearer Token
creds = connections.bearer_token(APP_ID)
url = creds.url
token = creds.token

# Basic Auth
creds = connections.basic_auth(APP_ID)
url = creds.url
username = creds.username
password = creds.password
```

### Step 3: Complete Tool Examples

See the `tools/poke_tool.py` file for three complete examples:
1. `get_pokemon_info` - Fetch detailed Pokémon data
2. `search_pokemon_by_type` - Find Pokémon by type
3. `get_pokemon_evolution_chain` - Get evolution chains

All three tools follow the same pattern:
1. Declare `expected_credentials` with `ExpectedCredentials`
2. Retrieve credentials using `connections.key_value()`
3. Get base URL from credentials dict
4. Make API requests using the base URL
5. Handle errors gracefully

---

## Configuration and Import

### Step 1: Configure the Connection

Set the base URL for the connection:

```bash
orchestrate connections configure -a pokeapi-connection -k url -v https://pokeapi.co/api/v2
```

**Command Breakdown:**
- `-a pokeapi-connection`: The app_id from your YAML file
- `-k url`: The key name (must be 'url' for our tools)
- `-v https://pokeapi.co/api/v2`: The PokéAPI base URL

### Step 2: Import the Connection

```bash
orchestrate connections import -f connections/pokeapi_connection.yaml
```

### Step 3: Verify Connection

```bash
orchestrate connections list
```

You should see:
```
APP_ID               AUTH_TYPE    TYPE    CREDENTIALS_SET
pokeapi-connection   key_value    team    ✅
```

### Step 4: Import the Tools

```bash
orchestrate tools import -k python -f tools/poke_tool.py --app-id pokeapi-connection
```

**Command Breakdown:**
- `-k python`: Tool kind (Python-based tool)
- `-f tools/poke_tool.py`: Path to your tool file
- `--app-id pokeapi-connection`: Links tools to the connection

### Step 5: Verify Tools

```bash
orchestrate tools list
```

You should see all three tools:
- `get_pokemon_info`
- `search_pokemon_by_type`
- `get_pokemon_evolution_chain`

---

## Testing Your Tools

### Test 1: Get Pokémon Info

```bash
orchestrate tools test get_pokemon_info --pokemon_name pikachu
```

Expected output:
```json
{
  "success": true,
  "name": "Pikachu",
  "id": 25,
  "types": ["electric"],
  "stats": {
    "hp": 35,
    "attack": 55,
    "defense": 40,
    "special-attack": 50,
    "special-defense": 50,
    "speed": 90
  },
  ...
}
```

### Test 2: Search by Type

```bash
orchestrate tools test search_pokemon_by_type --pokemon_type fire
```

### Test 3: Evolution Chain

```bash
orchestrate tools test get_pokemon_evolution_chain --pokemon_name charmander
```

Expected output:
```json
{
  "success": true,
  "pokemon": "Charmander",
  "evolution_chain": ["charmander", "charmeleon", "charizard"],
  "chain_length": 3
}
```

---

## Best Practices

### 1. Connection Management

#### ✅ DO:
```python
# Use ExpectedCredentials class
expected_credentials=[
    ExpectedCredentials(app_id=APP_ID, type=ConnectionType.KEY_VALUE)
]

# Retrieve credentials at runtime
creds = connections.key_value(APP_ID)
base_url = creds.get('url')

# Check if URL exists
if not base_url:
    return {"error": "Connection not configured", "success": False}
```

#### ❌ DON'T:
```python
# Don't use dict (causes type errors)
expected_credentials=[
    {"app_id": APP_ID, "type": ConnectionType.KEY_VALUE}
]

# Don't hardcode URLs
HARDCODED_URL = "https://pokeapi.co/api/v2"  # BAD!

# Don't skip error checking
base_url = creds.get('url')  # What if it's None?
url = f"{base_url}/pokemon/pikachu"  # Could crash!
```

### 2. Tool Design

#### ✅ DO:
```python
@tool(
    name="descriptive_tool_name",
    description="Clear description of what the tool does",
    expected_credentials=[ExpectedCredentials(...)]
)
def tool_function(param: str) -> Dict[str, Any]:
    """
    Detailed docstring explaining:
    - What the tool does
    - Parameters and their types
    - Return value structure
    - Example usage
    """
    try:
        # Implementation with error handling
        pass
    except Exception as e:
        return {"error": str(e), "success": False}
```

#### ❌ DON'T:
```python
@tool()  # Missing name, description, credentials
def tool():  # No type hints
    # No docstring
    # No error handling
    return data  # Inconsistent return format
```

### 3. Error Handling Pattern

Always return consistent error format:

```python
try:
    # Your logic here
    return {"success": True, "data": result}
except requests.exceptions.Timeout:
    return {"error": "Request timed out", "success": False}
except requests.exceptions.RequestException as e:
    return {"error": f"API error: {str(e)}", "success": False}
except Exception as e:
    return {"error": f"Unexpected error: {str(e)}", "success": False}
```

### 4. Response Structure

Use consistent response format:

```python
# Success response
{
    "success": True,
    "data": {...},
    "metadata": {...}
}

# Error response
{
    "success": False,
    "error": "Clear error message"
}
```

### 5. Connection Configuration Checklist

- [ ] Connection YAML file created with correct `app_id`
- [ ] Connection uses `key_value` kind for public APIs
- [ ] Connection configured with `orchestrate connections configure`
- [ ] Connection imported with `orchestrate connections import`
- [ ] Connection verified with `orchestrate connections list`
- [ ] Tools reference correct `app_id` constant
- [ ] Tools use `ExpectedCredentials` class (not dict)
- [ ] Tools retrieve credentials with `connections.key_value()`
- [ ] Tools check if URL exists before using it
- [ ] Tools imported with `--app-id` flag
- [ ] Tools tested with `orchestrate tools test`

---

## Troubleshooting

### Issue 1: Type Error with expected_credentials

**Error:**
```
Argument of type "list[dict[str, str | ConnectionType]]" cannot be assigned to parameter "expected_credentials"
```

**Solution:**
Use `ExpectedCredentials` class, not dict:

```python
# ❌ Wrong
expected_credentials=[{"app_id": APP_ID, "type": ConnectionType.KEY_VALUE}]

# ✅ Correct
from ibm_watsonx_orchestrate.agent_builder.connections import ExpectedCredentials

expected_credentials=[
    ExpectedCredentials(app_id=APP_ID, type=ConnectionType.KEY_VALUE)
]
```

### Issue 2: Connection Not Found

**Error:**
```
Connection 'pokeapi-connection' not found
```

**Solutions:**
1. Check connection is imported:
   ```bash
   orchestrate connections list
   ```

2. Verify app_id matches in YAML and Python:
   ```yaml
   # connections/pokeapi_connection.yaml
   app_id: pokeapi-connection
   ```
   ```python
   # tools/poke_tool.py
   POKEAPI_APP_ID = 'pokeapi-connection'  # Must match!
   ```

3. Configure the connection:
   ```bash
   orchestrate connections configure -a pokeapi-connection -k url -v https://pokeapi.co/api/v2
   ```

### Issue 3: URL Not Found in Credentials

**Error:**
```
Connection configuration error: 'url' not found in connection credentials
```

**Solution:**
Configure the 'url' key:

```bash
orchestrate connections configure -a pokeapi-connection -k url -v https://pokeapi.co/api/v2
```

### Issue 4: Tool Import Fails

**Error:**
```
Tool import failed: expected_credentials validation error
```

**Solutions:**
1. Ensure connection exists before importing tools
2. Use correct ConnectionType for your connection kind
3. Import tools with `--app-id` flag:
   ```bash
   orchestrate tools import -k python -f tools/poke_tool.py --app-id pokeapi-connection
   ```

### Issue 5: AttributeError on Credentials

**Error:**
```
AttributeError: 'dict' object has no attribute 'url'
```

**Solution:**
KEY_VALUE connections return a dict, not an object:

```python
# ❌ Wrong (for KEY_VALUE)
creds = connections.key_value(APP_ID)
url = creds.url  # AttributeError!

# ✅ Correct (for KEY_VALUE)
creds = connections.key_value(APP_ID)
url = creds.get('url')  # Use dict access

# ✅ Correct (for other types like API_KEY_AUTH)
creds = connections.api_key_auth(APP_ID)
url = creds.url  # These return objects with properties
```

---

## Summary

### What We Learned

1. **No NO_AUTH Type**: watsonx Orchestrate doesn't have a `NO_AUTH` connection type
2. **Use KEY_VALUE**: For public APIs, use `ConnectionType.KEY_VALUE`
3. **KEY_VALUE Returns Dict**: Access values with `.get('key')`, not `.property`
4. **ExpectedCredentials Class**: Always use the class, not a dict
5. **Connection Pattern**: Declare → Retrieve → Validate → Use

### Complete Workflow

```
1. Create connection YAML with KEY_VALUE kind
   ↓
2. Import connection: orchestrate connections import
   ↓
3. Configure URL: orchestrate connections configure -k url -v <url>
   ↓
4. Create Python tools with ExpectedCredentials
   ↓
5. Import tools: orchestrate tools import --app-id <app-id>
   ↓
6. Test tools: orchestrate tools test <tool-name>
   ↓
7. Add tools to agent YAML
   ↓
8. Update agent: orchestrate agents update
```

### Key Takeaways

- ✅ Always use `ExpectedCredentials` class in `expected_credentials`
- ✅ Use `ConnectionType.KEY_VALUE` for public APIs
- ✅ Retrieve credentials with `connections.key_value(app_id)`
- ✅ Access URL with `creds.get('url')` for KEY_VALUE
- ✅ Check if URL exists before using it
- ✅ Handle errors gracefully with try/except
- ✅ Return consistent response format

---

## Additional Resources

- **watsonx Orchestrate Documentation**: https://developer.watson-orchestrate.ibm.com
- **PokéAPI Documentation**: https://pokeapi.co/docs/v2
- **IBM watsonx Orchestrate ADK Source**: https://github.com/IBM/ibm-watsonx-orchestrate-adk
- **Connection Types Reference**: See `src/ibm_watsonx_orchestrate/agent_builder/connections/types.py`
- **Example Tools**: See `examples/agent_builder/customer_care/tools/servicenow/`

---

**Last Updated**: Based on IBM watsonx Orchestrate ADK source code analysis (2024)