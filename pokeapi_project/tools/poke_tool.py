from ibm_watsonx_orchestrate.agent_builder.tools import tool
import requests
from typing import Dict, Any

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"


@tool(
    name="get_pokemon_info",
    description="Retrieves detailed information about a specific Pokémon by name or ID from the PokéAPI"
)
def get_pokemon_info(pokemon_name: str) -> Dict[str, Any]:
    """
    Fetches comprehensive information about a Pokémon from the PokéAPI.
    
    This tool retrieves data including:
    - Basic stats (HP, Attack, Defense, Speed, etc.)
    - Types (Fire, Water, Grass, etc.)
    - Abilities
    - Height and weight
    - Sprite images
    
    Args:
        pokemon_name (str): The name or ID of the Pokémon (e.g., "pikachu", "charizard", "25")
                           Case-insensitive, accepts both names and numeric IDs
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - name: Pokémon name
            - id: National Pokédex number
            - types: List of types (e.g., ["electric"])
            - stats: Dictionary of base stats
            - abilities: List of abilities
            - height: Height in decimeters
            - weight: Weight in hectograms
            - sprite: URL to the official artwork
            - error: Error message if the Pokémon is not found
    
    Example:
        >>> get_pokemon_info("pikachu")
        {
            "name": "pikachu",
            "id": 25,
            "types": ["electric"],
            "stats": {"hp": 35, "attack": 55, ...},
            ...
        }
    """
    
    try:
        # Convert to lowercase for API compatibility
        pokemon_name = pokemon_name.lower().strip()
        
        # Build the full URL using the hardcoded base URL
        url = f"{POKEAPI_BASE_URL}/pokemon/{pokemon_name}"
        
        # Make the API request
        response = requests.get(url, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 404:
            return {
                "error": f"Pokémon '{pokemon_name}' not found. Please check the spelling or try a different name.",
                "success": False
            }
        
        # Raise an exception for other HTTP errors
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # Extract and format the relevant information
        pokemon_info = {
            "success": True,
            "name": data["name"].capitalize(),
            "id": data["id"],
            "types": [type_info["type"]["name"] for type_info in data["types"]],
            "stats": {
                stat["stat"]["name"]: stat["base_stat"]
                for stat in data["stats"]
            },
            "abilities": [
                ability["ability"]["name"]
                for ability in data["abilities"]
            ],
            "height": data["height"],  # in decimeters (1 dm = 10 cm)
            "weight": data["weight"],  # in hectograms (1 hg = 100 g)
            "sprite": data["sprites"]["other"]["official-artwork"]["front_default"],
            "base_experience": data["base_experience"]
        }
        
        return pokemon_info
        
    except requests.exceptions.Timeout:
        return {
            "error": "Request timed out. The PokéAPI might be slow or unavailable.",
            "success": False
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch Pokémon data: {str(e)}",
            "success": False
        }
    except KeyError as e:
        return {
            "error": f"Unexpected data format from API: missing key {str(e)}",
            "success": False
        }
    except Exception as e:
        return {
            "error": f"An unexpected error occurred: {str(e)}",
            "success": False
        }


@tool(
    name="search_pokemon_by_type",
    description="Searches for all Pokémon of a specific type (e.g., fire, water, electric)"
)
def search_pokemon_by_type(pokemon_type: str) -> Dict[str, Any]:
    """
    Retrieves a list of all Pokémon that have a specific type.
    
    Args:
        pokemon_type (str): The type to search for (e.g., "fire", "water", "electric", "grass")
                           Case-insensitive
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - type: The type that was searched
            - count: Number of Pokémon with this type
            - pokemon: List of Pokémon names with this type (limited to first 20)
            - error: Error message if the type is not found
    
    Example:
        >>> search_pokemon_by_type("electric")
        {
            "type": "electric",
            "count": 68,
            "pokemon": ["pikachu", "raichu", "magnemite", ...],
            ...
        }
    """
    
    try:
        # Convert to lowercase for API compatibility
        pokemon_type = pokemon_type.lower().strip()
        
        # Build the full URL using the hardcoded base URL
        url = f"{POKEAPI_BASE_URL}/type/{pokemon_type}"
        
        # Make the API request
        response = requests.get(url, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 404:
            return {
                "error": f"Type '{pokemon_type}' not found. Valid types include: normal, fire, water, electric, grass, ice, fighting, poison, ground, flying, psychic, bug, rock, ghost, dragon, dark, steel, fairy",
                "success": False
            }
        
        response.raise_for_status()
        data = response.json()
        
        # Extract Pokémon names (limit to first 20 for readability)
        all_pokemon = [p["pokemon"]["name"] for p in data["pokemon"]]
        
        result = {
            "success": True,
            "type": pokemon_type.capitalize(),
            "count": len(all_pokemon),
            "pokemon": all_pokemon[:20],  # First 20 Pokémon
            "total_available": len(all_pokemon),
            "showing": min(20, len(all_pokemon))
        }
        
        if len(all_pokemon) > 20:
            result["note"] = f"Showing first 20 of {len(all_pokemon)} Pokémon with type {pokemon_type}"
        
        return result
        
    except requests.exceptions.Timeout:
        return {
            "error": "Request timed out. The PokéAPI might be slow or unavailable.",
            "success": False
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch type data: {str(e)}",
            "success": False
        }
    except Exception as e:
        return {
            "error": f"An unexpected error occurred: {str(e)}",
            "success": False
        }


@tool(
    name="get_pokemon_evolution_chain",
    description="Retrieves the evolution chain for a Pokémon species"
)
def get_pokemon_evolution_chain(pokemon_name: str) -> Dict[str, Any]:
    """
    Fetches the complete evolution chain for a Pokémon.
    
    Args:
        pokemon_name (str): The name of the Pokémon (e.g., "charmander", "pikachu")
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - pokemon: The queried Pokémon name
            - evolution_chain: List of evolution stages
            - error: Error message if not found
    
    Example:
        >>> get_pokemon_evolution_chain("charmander")
        {
            "pokemon": "charmander",
            "evolution_chain": ["charmander", "charmeleon", "charizard"],
            ...
        }
    """
    
    try:
        pokemon_name = pokemon_name.lower().strip()
        
        # First, get the species data using the hardcoded base URL
        species_url = f"{POKEAPI_BASE_URL}/pokemon-species/{pokemon_name}"
        species_response = requests.get(species_url, timeout=10)
        
        if species_response.status_code == 404:
            return {
                "error": f"Pokémon species '{pokemon_name}' not found.",
                "success": False
            }
        
        species_response.raise_for_status()
        species_data = species_response.json()
        
        # Get the evolution chain URL
        evolution_chain_url = species_data["evolution_chain"]["url"]
        
        # Fetch the evolution chain
        evolution_response = requests.get(evolution_chain_url, timeout=10)
        evolution_response.raise_for_status()
        evolution_data = evolution_response.json()
        
        # Parse the evolution chain
        def parse_chain(chain_data):
            """Recursively parse the evolution chain"""
            evolutions = [chain_data["species"]["name"]]
            
            if chain_data.get("evolves_to"):
                for evolution in chain_data["evolves_to"]:
                    evolutions.extend(parse_chain(evolution))
            
            return evolutions
        
        evolution_list = parse_chain(evolution_data["chain"])
        
        return {
            "success": True,
            "pokemon": pokemon_name.capitalize(),
            "evolution_chain": evolution_list,
            "chain_length": len(evolution_list)
        }
        
    except requests.exceptions.Timeout:
        return {
            "error": "Request timed out. The PokéAPI might be slow or unavailable.",
            "success": False
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch evolution data: {str(e)}",
            "success": False
        }
    except Exception as e:
        return {
            "error": f"An unexpected error occurred: {str(e)}",
            "success": False
        }