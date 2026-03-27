# GameBrain API Integration for watsonx Orchestrate

A complete integration between the GameBrain API and IBM watsonx Orchestrate, enabling AI agents to search for video games, retrieve detailed game information, and filter games by genre and platform.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Features](#features)
- [Setup & Configuration](#setup--configuration)
- [Usage](#usage)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Development](#development)

## Overview

This project provides four powerful tools for interacting with the GameBrain API:
- 🔍 **Search Games** - Find games by title or keyword
- 📋 **Get Game Details** - Retrieve comprehensive game information
- 🎮 **Filter by Genre** - Find games in specific genres
- 🎯 **Filter by Platform** - Find games for specific platforms

## Project Structure

```
gamebrain_project/
├── agents/
│   └── gamebrain_agent.yaml        # Agent configuration
├── connections/
│   └── gamebrain_connection.yaml   # API connection config
├── tools/
│   └── gamebrain_tools.py          # Tool implementations
├── tests/
│   └── test_gamebrain_tools.py     # Test suite
├── utils/
│   └── PROMPT.md                   # Implementation guide
└── README.md                       # This file
```

## Quick Start

### 1. Get Your API Key

Visit [GameBrain.co](https://gamebrain.co) to obtain your API key:
1. Sign up or log in to your account
2. Navigate to API settings
3. Generate or retrieve your API key

### 2. Configure the Connection

```bash
# Navigate to the project directory
cd gamebrain_project

# Configure the connection (first-time setup)
orchestrate connections configure connections/gamebrain_connection.yaml
```

When prompted, enter your GameBrain API key.

### 3. Import the Tools

```bash
# Import all tools
orchestrate tools import -f ./tools/gamebrain_tools.py -k python --app-id gamebrain_api
```

You should see:
```
[INFO] - Tool 'search_games' updated successfully
[INFO] - Tool 'get_game_details' updated successfully
[INFO] - Tool 'filter_games_by_genre' updated successfully
[INFO] - Tool 'filter_games_by_platform' updated successfully
```

### 4. Run the Agent

```bash
orchestrate agents run gamebrain_agent
```

Try queries like:
- "Search for zelda games"
- "Find strategy games"
- "Show me games for Nintendo Switch"
- "Get details for game ID 64591"

## Features

### 🔍 Search Games

Search for video games by title or keyword with optional platform filtering.

**Tool:** `search_games`

**Parameters:**
- `query` (str): Search term (e.g., "zelda", "mario", "minecraft")
- `limit` (int): Max results (default: 20, max: 50)
- `platform` (Optional[str]): Filter by platform (e.g., "ps5", "switch")

**Example Response:**
```json
{
    "success": true,
    "games": [
        {
            "id": 64591,
            "name": "Medieval II: Total War",
            "genre": "Tactical Turn-based Strategy",
            "year": 2006,
            "rating": {"mean": 0.944, "count": 12782},
            "platforms": [...]
        }
    ],
    "count": 10,
    "total_results": 395,
    "query": "medieval strategy"
}
```

### 📋 Get Game Details

Retrieve comprehensive information about a specific game.

**Tool:** `get_game_details`

**Parameters:**
- `game_id` (str): Unique game identifier (from search results)

**Returns:** Game details including name, year, genre, rating, platforms, screenshots, and more.

### 🎮 Filter by Genre

Find games in specific genres.

**Tool:** `filter_games_by_genre`

**Parameters:**
- `genre` (str): Genre name (case-insensitive)
- `limit` (int): Max results (default: 20, max: 50)

**Supported Genres:**
- Action, Adventure, RPG, Strategy
- Sports, Racing, Fighting, Shooter
- Puzzle, Platformer, Simulation
- Horror, Survival, Stealth

### 🎯 Filter by Platform

Find games available on specific platforms.

**Tool:** `filter_games_by_platform`

**Parameters:**
- `platform` (str): Platform name (case-insensitive)
- `limit` (int): Max results (default: 20, max: 50)

**Supported Platforms:**
- **PlayStation:** ps5, ps4, ps3, psvita
- **Xbox:** xbox-series-x, xbox-one, xbox-360
- **Nintendo:** switch, wii-u, 3ds
- **PC:** pc, windows, mac, linux
- **Mobile:** ios, android
- **Other:** stadia, steam-deck

## Setup & Configuration

### Connection Configuration

The connection is defined in `connections/gamebrain_connection.yaml`:

```yaml
spec_version: v1
kind: connection
app_id: gamebrain_api
environments:
    draft:
        kind: api_key
        type: team
        server_url: https://api.gamebrain.co/v1
    live:
        kind: api_key
        type: team
        server_url: https://api.gamebrain.co/v1
```

### Configuration Methods

#### Method 1: First-Time Setup (Recommended)

```bash
orchestrate connections configure connections/gamebrain_connection.yaml
```

This will:
- Read the connection configuration
- Prompt for your API key
- Store credentials securely
- Configure both draft and live environments

#### Method 2: Update Existing Credentials

```bash
# Update draft environment
orchestrate connections set-credentials gamebrain_api --environment draft

# Update live environment
orchestrate connections set-credentials gamebrain_api --environment live
```

### Verify Configuration

```bash
# List all connections
orchestrate connections list

# View connection details
orchestrate connections get gamebrain_api
```

## Usage

### Agent Configuration

The agent is configured in `agents/gamebrain_agent.yaml`:

```yaml
spec_version: v1
kind: native
name: gamebrain_agent
display_name: GameBrain Agent
llm: groq/openai/gpt-oss-120b
style: react
description: Agent for searching and retrieving video game information
tools:
  - search_games
  - get_game_details
  - filter_games_by_genre
  - filter_games_by_platform
```

### Example Queries

**Search for games:**
```
"Find games about medieval strategy"
"Search for zelda games on switch"
"Show me the top 5 mario games"
```

**Get game details:**
```
"Get details for game ID 64591"
"Tell me more about Medieval II: Total War"
```

**Filter by genre:**
```
"Find RPG games"
"Show me action games"
"List strategy games"
```

**Filter by platform:**
```
"What games are available for PS5?"
"Show me Nintendo Switch games"
"Find PC games"
```

## Testing

### Run the Test Suite

```bash
cd gamebrain_project
python tests/test_gamebrain_tools.py
```

The test suite validates:
- ✅ Connection configuration
- ✅ API authentication
- ✅ All 4 tools functionality
- ✅ Error handling
- ✅ Response structure
- ✅ watsonx Orchestrate conventions

### Expected Output

```
🚀 GAMEBRAIN API TOOLS TEST SUITE
================================================================================

✅ API Key configured: d5539618...3452

⚠️  NOTE: These tests will make actual API calls to GameBrain API

🔍 Testing search_games tool...
Test 1: Basic search for 'zelda'
Success: True
Count: 5
Total Results: 395
First Game: The Legend of Zelda: Breath of the Wild (ID: 12345)
...
```

## Troubleshooting

### Connection Issues

**Error:** "Failed to get GameBrain API connection"

**Solution:**
```bash
orchestrate connections configure connections/gamebrain_connection.yaml
```

### Authentication Errors

**Error:** "Authentication failed" (401)

**Causes:**
- Invalid API key
- Expired API key
- API key not set

**Solutions:**
1. Verify your API key at [GameBrain.co](https://gamebrain.co)
2. Update credentials:
   ```bash
   orchestrate connections set-credentials gamebrain_api --environment draft
   ```

### Tool Import Warnings

**Warning:** "Unable to properly parse parameter descriptions"

**Cause:** Docstring format doesn't match type hints

**Solution:** This has been fixed in the current version. Ensure you're using the latest `gamebrain_tools.py`.

### Timeout Errors

**Error:** "Request timed out"

**Causes:**
- Slow internet connection
- GameBrain API unavailability
- Network issues

**Solutions:**
- Check your internet connection
- Verify GameBrain API status
- Wait and retry (timeout is set to 10 seconds)

### Agent Not Finding Tools

**Issue:** Agent can't select the right tool

**Solutions:**
1. Verify tools are imported:
   ```bash
   orchestrate tools list --app-id gamebrain_api
   ```

2. Check agent configuration:
   ```bash
   orchestrate agents get gamebrain_agent
   ```

3. Ensure tool names match in YAML and Python files

## Development

### API Endpoints

**Base URL:** `https://api.gamebrain.co/v1`

**Endpoints:**
- `GET /games?query={query}&limit={limit}` - Search games
- `GET /games/{game_id}` - Get game details

**Authentication:**
```
x-api-key: your-api-key-here
```

### Adding New Tools

Follow the watsonx Orchestrate pattern:

```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import Dict, Any

@tool(
    name="tool_name",
    description="Clear description of what the tool does"
)
def tool_name(param: str) -> Dict[str, Any]:
    """
    Detailed description.
    
    Args:
        param (str): Parameter description
    
    Returns:
        Dict[str, Any]: Return value description
    """
    # Implementation
    return {"success": True, "data": "..."}
```

### Code Style Guidelines

- ✅ Type hints for all parameters and returns
- ✅ Concise docstrings matching type hints exactly
- ✅ Comprehensive error handling
- ✅ Input validation and sanitization
- ✅ Consistent return structures with `success` field
- ✅ Descriptive variable names

### Error Handling Pattern

All tools follow this pattern:

```python
try:
    # Validate inputs
    # Make API request
    # Parse response
    return {"success": True, "data": ...}
except requests.exceptions.Timeout:
    return {"success": False, "error": "Request timed out"}
except Exception as e:
    return {"success": False, "error": str(e)}
```

## Requirements

```
ibm-watsonx-orchestrate
requests
typing
```

## API Response Examples

### Search Response
```json
{
    "success": true,
    "games": [...],
    "count": 10,
    "total_results": 395,
    "query": "zelda"
}
```

### Game Details Response
```json
{
    "success": true,
    "game": {...},
    "id": 64591,
    "name": "Medieval II: Total War",
    "year": 2006,
    "genre": "Tactical Turn-based Strategy",
    "rating": {"mean": 0.944, "count": 12782},
    "platforms": [...]
}
```

### Error Response
```json
{
    "success": false,
    "error": "Authentication failed. Please check your API key."
}
```

## Best Practices

1. **Always validate inputs** - Check for empty strings, invalid ranges
2. **Use timeouts** - Set reasonable timeouts (10 seconds recommended)
3. **Limit results** - Cap large result sets for better performance
4. **Provide context** - Include helpful error messages
5. **Test thoroughly** - Validate both success and error cases
6. **Handle errors gracefully** - Return consistent error structures

## Support

For issues or questions:
1. Check this README's troubleshooting section
2. Review the implementation guide in `utils/PROMPT.md`
3. Run the test suite to diagnose issues
4. Consult watsonx Orchestrate documentation

## License

This project is part of the watsonx Orchestrate agent development kit.

---

**Last Updated:** 2026-03-27  
**Version:** 1.0.0  
**Status:** ✅ Production Ready

**Made with Bob** 🤖