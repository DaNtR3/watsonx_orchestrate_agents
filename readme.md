# watsonx Orchestrate Custom Agents Repository

This repository contains custom agents developed for IBM watsonx Orchestrate. These agents demonstrate best practices for building AI-powered assistants that can interact with external APIs, use tools, and provide intelligent responses.

## 📋 Overview

watsonx Orchestrate is IBM's platform for building and deploying AI agents that can automate tasks, answer questions, and integrate with various services. This repository serves as a collection of example agents and reusable patterns for agent development.

## 🗂️ Repository Structure

```
watsonx_orchestrate_agents/
├── readme.md                          # This file
├── pokeapi_project/                   # Example: PokéAPI Agent
│   ├── agents/
│   │   └── poke_agent.yaml           # Agent configuration
│   ├── tools/
│   │   └── poke_tool.py              # Python tools for PokéAPI
│   ├── docs/
│   │   ├── AGENT_ARCHITECTURE.md     # Architecture guide
│   │   ├── AGENT_YAML_REFERENCE.md   # YAML configuration reference
│   │   └── POKEAPI_CONNECTION_GUIDE.md # Connection setup guide
│   └── .gitignore
└── gamebrain_project/                 # Example: GameBrain API Agent
    ├── agents/
    │   └── gamebrain_agent.yaml      # Agent configuration
    ├── connections/
    │   └── gamebrain_connection.yaml # API connection config
    ├── tools/
    │   └── gamebrain_tools.py        # Python tools for GameBrain API
    ├── tests/
    │   └── test_gamebrain_tools.py   # Test suite
    ├── utils/
    │   └── PROMPT.md                 # Implementation guide
    └── README.md                     # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- IBM watsonx Orchestrate account
- watsonx Orchestrate CLI installed
- Python 3.8+ (for Python-based tools)
- Basic understanding of YAML and Python

### Installation

1. **Clone this repository**
   ```bash
   git clone <repository-url>
   cd watsonx_orchestrate_agents
   ```

2. **Install watsonx Orchestrate CLI**
   ```bash
   pip install ibm-watsonx-orchestrate
   ```

3. **Authenticate with watsonx Orchestrate**
   ```bash
   orchestrate login
   ```

## 📦 Available Projects

### 1. PokéAPI Agent

A fully functional agent that interacts with the [PokéAPI](https://pokeapi.co) to provide Pokémon information.

**Features:**
- 🔍 Look up detailed Pokémon information by name or ID
- 🎯 Search for Pokémon by type (fire, water, electric, etc.)
- 🔄 Display evolution chains for Pokémon species

**Quick Start:**
```bash
cd pokeapi_project

# Import the agent
orchestrate agents import -f agents/poke_agent.yaml

# Configure and import connection
orchestrate connections import -f connections/pokeapi_connection.yaml
orchestrate connections configure -a pokeapi-connection -k url -v https://pokeapi.co/api/v2

# Import tools
orchestrate tools import -k python -f tools/poke_tool.py --app-id pokeapi-connection

# Test the agent
orchestrate agents chat poke_agent
```

**Documentation:**
- [Agent Architecture Guide](pokeapi_project/docs/AGENT_ARCHITECTURE.md) - Comprehensive guide to agent components and design patterns
- [YAML Reference](pokeapi_project/docs/AGENT_YAML_REFERENCE.md) - Complete reference for agent configuration
- [Connection Setup Guide](pokeapi_project/docs/POKEAPI_CONNECTION_GUIDE.md) - Step-by-step guide for API connections

### 2. GameBrain API Agent

A production-ready agent that integrates with the [GameBrain API](https://gamebrain.co) to search and retrieve video game information.

**Features:**
- 🔍 Search for video games by title or keyword with platform filtering
- 📋 Get comprehensive game details (ratings, platforms, screenshots, etc.)
- 🎮 Filter games by genre (Action, RPG, Strategy, Sports, etc.)
- 🎯 Filter games by platform (PS5, Xbox, PC, Switch, etc.)

**Quick Start:**
```bash
cd gamebrain_project

# Configure the connection (enter your API key when prompted)
orchestrate connections configure connections/gamebrain_connection.yaml

# Import tools
orchestrate tools import -f ./tools/gamebrain_tools.py -k python --app-id gamebrain_api

# Import and run the agent
orchestrate agents import -f agents/gamebrain_agent.yaml
orchestrate agents run gamebrain_agent
```

**Example Queries:**
- "Search for zelda games"
- "Find strategy games"
- "Show me games for Nintendo Switch"
- "Get details for game ID 64591"

**Documentation:**
- [Complete Project README](gamebrain_project/README.md) - Full setup guide, features, and troubleshooting

## 🏗️ Agent Architecture

watsonx Orchestrate agents consist of several key components:

### Core Components

1. **Agent** - The main AI assistant powered by an LLM
2. **Tools** - Functions that extend agent capabilities (API calls, data processing, etc.)
3. **Knowledge Bases** - Document repositories for RAG (Retrieval-Augmented Generation)
4. **Flows** - Multi-step workflows with conditional logic
5. **Connections** - Secure credential management for external services
6. **Collaborators** - Other agents that can be delegated tasks

### Agent Configuration (YAML)

```yaml
spec_version: v1
kind: native
name: my_agent
display_name: "My Agent"
llm: watsonx/ibm/granite-3-8b-instruct
description: "Agent description"
instructions: "System instructions for the agent"
tools:
  - tool_name_1
  - tool_name_2
```

### Tool Implementation (Python)

```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType, ExpectedCredentials
from ibm_watsonx_orchestrate.run import connections

@tool(
    name="my_tool",
    description="Tool description",
    expected_credentials=[
        ExpectedCredentials(app_id="my-connection", type=ConnectionType.KEY_VALUE)
    ]
)
def my_tool(param: str) -> dict:
    """Tool implementation"""
    creds = connections.key_value("my-connection")
    base_url = creds.get('url')
    # Tool logic here
    return {"success": True, "data": result}
```

## 📚 Documentation

Each project includes comprehensive documentation:

- **Architecture Guides** - Understanding agent components and relationships
- **YAML References** - Complete field descriptions and examples
- **Connection Guides** - Setting up API integrations
- **Best Practices** - Patterns and recommendations

## 🛠️ Development Workflow

### Creating a New Agent

1. **Define the agent's purpose**
   - What problem does it solve?
   - What APIs or services will it use?
   - What tools does it need?

2. **Create the agent YAML**
   ```yaml
   spec_version: v1
   kind: native
   name: my_new_agent
   llm: watsonx/ibm/granite-3-8b-instruct
   description: "Agent description"
   instructions: "Detailed instructions"
   ```

3. **Create required tools**
   - Implement Python functions with `@tool` decorator
   - Define expected credentials
   - Handle errors gracefully

4. **Set up connections**
   - Create connection YAML files
   - Configure credentials
   - Import connections

5. **Test and iterate**
   - Test tools individually
   - Test agent conversations
   - Refine instructions and responses

6. **Deploy**
   - Import to watsonx Orchestrate
   - Share with users
   - Monitor and improve

## 🔑 Key Concepts

### Connection Types

watsonx Orchestrate supports various authentication methods:

- `KEY_VALUE` - For public APIs or custom configurations
- `API_KEY_AUTH` - API key authentication
- `BEARER_TOKEN` - Bearer token authentication
- `BASIC_AUTH` - Username/password authentication
- `OAUTH2_*` - Various OAuth 2.0 flows

### LLM Selection

Choose the right model for your use case:

- **Granite 3-8B** - Good balance of performance and cost
- **Llama 3.3-70B** - Better for complex reasoning
- **Granite-20B-Multilingual** - Multi-language support

### Agent Styles

- **Conversational** - Natural, friendly dialogue (customer-facing)
- **Task-oriented** - Efficient task completion (automation)

## 📖 Best Practices

### Agent Design
- ✅ Write clear, specific instructions
- ✅ Define agent personality and tone
- ✅ Set boundaries and limitations
- ✅ Provide example prompts (starter_prompts)
- ✅ Use descriptive names and descriptions

### Tool Design
- ✅ Use `ExpectedCredentials` class (not dicts)
- ✅ Retrieve credentials at runtime
- ✅ Handle errors gracefully
- ✅ Return consistent response formats
- ✅ Include detailed docstrings

### Connection Management
- ✅ Never hardcode URLs or credentials
- ✅ Use appropriate connection types
- ✅ Validate credentials before use
- ✅ Configure environment-specific settings

### Testing
- ✅ Test tools individually first
- ✅ Test multi-turn conversations
- ✅ Verify error handling
- ✅ Test edge cases
- ✅ Monitor agent performance

## 🤝 Contributing

Contributions are welcome! To add a new agent project:

1. Create a new directory with a descriptive name
2. Include all necessary files (agents/, tools/, docs/)
3. Provide comprehensive documentation
4. Follow the established patterns and best practices
5. Test thoroughly before submitting

## 📝 License

[Specify your license here]

## 🔗 Resources

- [watsonx Orchestrate Documentation](https://developer.watson-orchestrate.ibm.com/)
- [IBM watsonx Orchestrate ADK](https://github.com/IBM/ibm-watsonx-orchestrate-adk)
- [Agent Builder Guide](https://developer.watson-orchestrate.ibm.com/agents/build_agent)
- [Tool Development Guide](https://developer.watson-orchestrate.ibm.com/tools/overview)

## 💡 Example Use Cases

- **Customer Support** - Automated assistance with orders, returns, FAQs
- **Data Analysis** - Query databases, generate reports, visualize data
- **API Integration** - Connect to external services (weather, news, etc.)
- **Task Automation** - Schedule tasks, process workflows, send notifications
- **Knowledge Management** - Search documents, answer questions, provide insights

## 🆘 Support

For issues or questions:
- Check the project-specific documentation
- Review the [watsonx Orchestrate documentation](https://developer.watson-orchestrate.ibm.com/)
- Open an issue in this repository

## 🎯 Roadmap

Future additions to this repository may include:
- [x] GameBrain API agent (video game information)
- [ ] Weather API agent
- [ ] Database query agent
- [ ] Multi-agent collaboration examples
- [ ] Advanced workflow patterns
- [ ] Knowledge base integration examples
- [ ] Custom UI components

---

**Happy Agent Building! 🚀**