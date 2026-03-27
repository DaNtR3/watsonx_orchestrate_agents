from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType
from ibm_watsonx_orchestrate.run import connections
import requests
from typing import Dict, Any, Optional

MY_APP_ID = 'gamebrain_api'
DEFAULT_TIMEOUT = 10
MAX_RESULTS = 20

def _get_connection_details() -> tuple[str, Dict[str, str]]:
    """
    Get connection details (URL and headers) from watsonx Orchestrate connection.
    
    Returns:
        Tuple of (base_url, headers_dict)
    """
    try:
        conn = connections.api_key_auth(MY_APP_ID)
        url = conn.url
        api_key = conn.api_key
        
        headers = {
            'x-api-key': api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        return url, headers
    except Exception as e:
        raise ValueError(f"Failed to get GameBrain API connection: {str(e)}. Please configure the connection in watsonx Orchestrate.")


@tool(
    name="search_games",
    description="Searches for video games by title or keyword using the GameBrain API",
    expected_credentials=[
        {"app_id": MY_APP_ID, "type": ConnectionType.API_KEY_AUTH}
    ]
)
def search_games(query: str, limit: int = 20, platform: Optional[str] = None) -> Dict[str, Any]:
    """
    Searches for video games matching the query term.
    
    This tool retrieves games based on title, keyword, or game name.
    Optionally filter results by gaming platform.
    
    Args:
        query (str): Search term (game title, keyword, or game name). Examples: "zelda", "mario", "minecraft", "final fantasy"
        limit (int): Maximum number of results to return (default: 20, max: 50)
        platform (Optional[str]): Filter by platform (e.g., "ps5", "xbox", "pc", "switch"). Defaults to None.
    
    Returns:
        Dict[str, Any]: A dictionary containing success status, games list, count, query, and optional platform/error fields
    """
    
    try:
        # Validate and sanitize inputs
        query = query.strip()
        if not query:
            return {
                "error": "Search query cannot be empty. Please provide a game title or keyword.",
                "success": False
            }
        
        # Limit results to reasonable range
        limit = max(1, min(limit, 50))
        
        # Get connection details (URL and headers with API key)
        base_url, headers = _get_connection_details()
        
        # Build API URL and parameters
        url = f"{base_url}/games"
        params = {
            "query": query,
            "limit": limit
        }
        
        # Add platform filter if provided
        if platform:
            params["platform"] = platform.lower().strip()
        
        # Make API request with authentication headers
        response = requests.get(url, params=params, headers=headers, timeout=DEFAULT_TIMEOUT)
        
        # Handle 404 - no results found
        if response.status_code == 404:
            return {
                "success": True,
                "games": [],
                "count": 0,
                "query": query,
                "total_results": 0,
                "message": f"No games found matching '{query}'"
            }
        
        # Handle 401 - unauthorized (invalid API key)
        if response.status_code == 401:
            return {
                "error": "Authentication failed. Please check your GAMEBRAIN_API_KEY is valid.",
                "success": False
            }
        
        # Raise exception for other HTTP errors
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        # Extract games list from 'results' field
        games = data.get("results", [])
        total_results = data.get("total_results", len(games))
        
        result = {
            "success": True,
            "games": games,
            "count": len(games),
            "total_results": total_results,
            "query": query
        }
        
        if platform:
            result["platform"] = platform
        
        if total_results > limit:
            result["note"] = f"Showing first {limit} of {total_results} results. Increase limit for more games."
        
        return result
        
    except ValueError as e:
        # API key not configured
        return {
            "error": str(e),
            "success": False
        }
    except requests.exceptions.Timeout:
        return {
            "error": "Request timed out. The GameBrain API might be slow or unavailable. Please try again.",
            "success": False
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to search games: {str(e)}",
            "success": False
        }
    except KeyError as e:
        return {
            "error": f"Unexpected response format from API: missing key {str(e)}",
            "success": False
        }
    except Exception as e:
        return {
            "error": f"An unexpected error occurred: {str(e)}",
            "success": False
        }


@tool(
    name="get_game_details",
    description="Retrieves detailed information about a specific video game by its ID",
    expected_credentials=[
        {"app_id": MY_APP_ID, "type": ConnectionType.API_KEY_AUTH}
    ]
)
def get_game_details(game_id: str) -> Dict[str, Any]:
    """
    Fetches comprehensive information about a specific game.
    
    This tool retrieves detailed data including description, release dates, platforms, genres, ratings, and media.
    
    Args:
        game_id (str): The unique identifier for the game (typically obtained from search_games results)
    
    Returns:
        Dict[str, Any]: A dictionary containing success status, game data, id, name, title, and optional fields like year, genre, rating, platforms, screenshots
    """
    
    try:
        # Validate input
        game_id = str(game_id).strip()
        if not game_id:
            return {
                "error": "Game ID cannot be empty. Please provide a valid game identifier.",
                "success": False
            }
        
        # Get connection details (URL and headers with API key)
        base_url, headers = _get_connection_details()
        
        # Build API URL
        url = f"{base_url}/games/{game_id}"
        
        # Make API request with authentication headers
        response = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)
        
        # Handle 404 - game not found
        if response.status_code == 404:
            return {
                "error": f"Game with ID '{game_id}' not found. Please verify the game ID is correct.",
                "success": False
            }
        
        # Handle 401 - unauthorized
        if response.status_code == 401:
            return {
                "error": "Authentication failed. Please check your GAMEBRAIN_API_KEY is valid.",
                "success": False
            }
        
        # Raise exception for other HTTP errors
        response.raise_for_status()
        
        # Parse JSON response
        game_data = response.json()
        
        result = {
            "success": True,
            "game": game_data,
            "id": game_data.get("id", game_id),
            "name": game_data.get("name", "Unknown"),
            "title": game_data.get("name", "Unknown")  # Alias for compatibility
        }
        
        # Add optional fields if available
        optional_fields = [
            "short_description", "year", "genre", "image", "link",
            "rating", "platforms", "screenshots", "micro_trailer",
            "gameplay", "adult_only"
        ]
        
        for field in optional_fields:
            if field in game_data:
                result[field] = game_data[field]
        
        return result
        
    except ValueError as e:
        # API key not configured
        return {
            "error": str(e),
            "success": False
        }
    except requests.exceptions.Timeout:
        return {
            "error": "Request timed out. The GameBrain API might be slow or unavailable. Please try again.",
            "success": False
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch game details: {str(e)}",
            "success": False
        }
    except KeyError as e:
        return {
            "error": f"Unexpected response format from API: missing key {str(e)}",
            "success": False
        }
    except Exception as e:
        return {
            "error": f"An unexpected error occurred: {str(e)}",
            "success": False
        }


@tool(
    name="filter_games_by_genre",
    description="Finds video games by genre category (action, rpg, strategy, etc.)",
    expected_credentials=[
        {"app_id": MY_APP_ID, "type": ConnectionType.API_KEY_AUTH}
    ]
)
def filter_games_by_genre(genre: str, limit: int = 20) -> Dict[str, Any]:
    """
    Retrieves games filtered by a specific genre.
    
    This tool searches for games in categories like Action, Adventure, RPG, Strategy, Sports, Racing, Fighting, Shooter, Puzzle, Platformer, Simulation, Horror, Survival, and Stealth.
    
    Args:
        genre (str): Genre name (e.g., "action", "rpg", "strategy", "sports"). Case-insensitive.
        limit (int): Maximum number of results to return (default: 20, max: 50)
    
    Returns:
        Dict[str, Any]: A dictionary containing success status, genre, games list, count, total_results, and optional error/note fields
    """
    
    try:
        # Validate and sanitize inputs
        genre = genre.lower().strip()
        if not genre:
            return {
                "error": "Genre cannot be empty. Please provide a valid genre (e.g., 'action', 'rpg', 'strategy').",
                "success": False
            }
        
        # Limit results to reasonable range
        limit = max(1, min(limit, 50))
        
        # Get connection details (URL and headers with API key)
        base_url, headers = _get_connection_details()
        
        # Build API URL and parameters - use query parameter with genre keyword
        url = f"{base_url}/games"
        params = {
            "query": genre,
            "limit": limit
        }
        
        # Make API request with authentication headers
        response = requests.get(url, params=params, headers=headers, timeout=DEFAULT_TIMEOUT)
        
        # Handle 404 - genre not found or no games
        if response.status_code == 404:
            return {
                "success": True,
                "genre": genre,
                "games": [],
                "count": 0,
                "total_results": 0,
                "message": f"No games found in genre '{genre}'. Common genres: action, adventure, rpg, strategy, sports, racing, puzzle."
            }
        
        # Handle 401 - unauthorized
        if response.status_code == 401:
            return {
                "error": "Authentication failed. Please check your GAMEBRAIN_API_KEY is valid.",
                "success": False
            }
        
        # Raise exception for other HTTP errors
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        # Extract games list from 'results' field
        games = data.get("results", [])
        total_results = data.get("total_results", len(games))
        
        result = {
            "success": True,
            "genre": genre.capitalize(),
            "games": games,
            "count": len(games),
            "total_results": total_results
        }
        
        if total_results > limit:
            result["note"] = f"Showing first {limit} of {total_results} results. Increase limit for more games."
        
        return result
        
    except ValueError as e:
        # API key not configured
        return {
            "error": str(e),
            "success": False
        }
    except requests.exceptions.Timeout:
        return {
            "error": "Request timed out. The GameBrain API might be slow or unavailable. Please try again.",
            "success": False
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to filter games by genre: {str(e)}",
            "success": False
        }
    except Exception as e:
        return {
            "error": f"An unexpected error occurred: {str(e)}",
            "success": False
        }


@tool(
    name="filter_games_by_platform",
    description="Finds video games available on a specific gaming platform (PS5, Xbox, PC, Switch, etc.)",
    expected_credentials=[
        {"app_id": MY_APP_ID, "type": ConnectionType.API_KEY_AUTH}
    ]
)
def filter_games_by_platform(platform: str, limit: int = 20) -> Dict[str, Any]:
    """
    Retrieves games available on a specific gaming platform.
    
    Supported platforms include PlayStation (ps5, ps4, ps3, psvita), Xbox (xbox-series-x, xbox-one, xbox-360), Nintendo (switch, wii-u, 3ds), PC (pc, windows, mac, linux), Mobile (ios, android), and Other (stadia, steam-deck).
    
    Args:
        platform (str): Platform name (e.g., "ps5", "xbox", "pc", "switch"). Case-insensitive.
        limit (int): Maximum number of results to return (default: 20, max: 50)
    
    Returns:
        Dict[str, Any]: A dictionary containing success status, platform, games list, count, total_results, and optional error/note fields
    """
    
    try:
        # Validate and sanitize inputs
        platform = platform.lower().strip()
        if not platform:
            return {
                "error": "Platform cannot be empty. Please provide a valid platform (e.g., 'ps5', 'xbox', 'pc', 'switch').",
                "success": False
            }
        
        # Limit results to reasonable range
        limit = max(1, min(limit, 50))
        
        # Get connection details (URL and headers with API key)
        base_url, headers = _get_connection_details()
        
        # Build API URL and parameters - use query parameter with platform keyword
        url = f"{base_url}/games"
        params = {
            "query": platform,
            "limit": limit
        }
        
        # Make API request with authentication headers
        response = requests.get(url, params=params, headers=headers, timeout=DEFAULT_TIMEOUT)
        
        # Handle 404 - platform not found or no games
        if response.status_code == 404:
            return {
                "success": True,
                "platform": platform,
                "games": [],
                "count": 0,
                "total_results": 0,
                "message": f"No games found for platform '{platform}'. Common platforms: ps5, xbox, pc, switch, ps4, xbox-one."
            }
        
        # Handle 401 - unauthorized
        if response.status_code == 401:
            return {
                "error": "Authentication failed. Please check your GAMEBRAIN_API_KEY is valid.",
                "success": False
            }
        
        # Raise exception for other HTTP errors
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        # Extract games list from 'results' field
        games = data.get("results", [])
        total_results = data.get("total_results", len(games))
        
        result = {
            "success": True,
            "platform": platform.upper() if len(platform) <= 4 else platform.capitalize(),
            "games": games,
            "count": len(games),
            "total_results": total_results
        }
        
        if total_results > limit:
            result["note"] = f"Showing first {limit} of {total_results} results. Increase limit for more games."
        
        return result
        
    except ValueError as e:
        # API key not configured
        return {
            "error": str(e),
            "success": False
        }
    except requests.exceptions.Timeout:
        return {
            "error": "Request timed out. The GameBrain API might be slow or unavailable. Please try again.",
            "success": False
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to filter games by platform: {str(e)}",
            "success": False
        }
    except Exception as e:
        return {
            "error": f"An unexpected error occurred: {str(e)}",
            "success": False
        }