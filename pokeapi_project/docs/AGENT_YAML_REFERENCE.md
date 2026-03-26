# watsonx Orchestrate Agent YAML Reference Guide

## Overview
This guide provides a comprehensive reference for all available fields and configurations when defining native agents in watsonx Orchestrate using YAML files.

---

## Table of Contents
1. [Basic Structure](#basic-structure)
2. [Required Fields](#required-fields)
3. [Optional Fields](#optional-fields)
4. [Field Descriptions](#field-descriptions)
5. [Available Values](#available-values)
6. [Complete Examples](#complete-examples)
7. [Best Practices](#best-practices)

---

## Basic Structure

```yaml
spec_version: v1
kind: native
name: agent_name
display_name: "Agent Display Name"
llm: provider/developer/model_id
description: "Agent description"
model_type: chat
icon: |
  <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64">
    <!-- SVG content here -->
  </svg>
welcome_content:
  welcome_message: "Welcome message"
  description: "Welcome description"
tags:
  - tag1
  - tag2
style: conversational
instructions: "System instructions for the agent"
starter_prompts:
  - "Example prompt 1"
  - "Example prompt 2"
tools:
  - tool_name_1
  - tool_name_2
knowledge:
  - knowledge_base_name
flows:
  - flow_name
collaborators:
  - collaborator_agent_1
  - collaborator_agent_2
```

---

## Required Fields

### Minimum Configuration
The following fields are **required** for a valid agent:

```yaml
spec_version: v1
kind: native
name: my_agent
llm: watsonx/ibm/granite-3-8b-instruct
```

---

## Optional Fields

All other fields are optional but recommended for better user experience and agent functionality.

---

## Field Descriptions

### `spec_version`
- **Type**: String
- **Required**: Yes
- **Default**: `v1`
- **Description**: The schema version of the agent specification format
- **Available Values**: 
  - `v1` (current version)

**Example:**
```yaml
spec_version: v1
```

---

### `kind`
- **Type**: String
- **Required**: Yes
- **Description**: Specifies the type of agent
- **Available Values**:
  - `native` - Agent runs on IBM's infrastructure with IBM LLMs
  - `external` - Agent connects to external services
  - `watsonx_assistant` - Integration with watsonx Assistant

**Example:**
```yaml
kind: native
```

---

### `name`
- **Type**: String
- **Required**: Yes
- **Description**: Unique internal identifier for the agent (used programmatically)
- **Constraints**: 
  - Must be unique within your environment
  - Use lowercase, underscores, no spaces
  - Should be descriptive but concise

**Example:**
```yaml
name: customer_support_agent
```

---

### `display_name`
- **Type**: String
- **Required**: No (but highly recommended)
- **Description**: Human-readable name shown to users in the UI
- **Constraints**: Can include spaces, special characters, emojis

**Example:**
```yaml
display_name: "Customer Support Agent 🤖"
```

---

### `llm`
- **Type**: String
- **Required**: Yes
- **Format**: `provider/developer/model_id`
- **Description**: Specifies which Large Language Model powers the agent
- **Available Providers**:
  - `watsonx` - IBM watsonx.ai models
  - `openai` - OpenAI models
  - `groq` - Groq models
  - `anthropic` - Anthropic Claude models
  - `google` - Google models
  - `azure-ai` - Azure AI models
  - `azure-openai` - Azure OpenAI models
  - `bedrock` - AWS Bedrock models
  - `mistral-ai` - Mistral AI models
  - `openrouter` - OpenRouter models
  - `x-ai` - x.ai models
  - `ollama` - Ollama local models

**Popular watsonx Models:**
```yaml
# IBM Granite models
llm: watsonx/ibm/granite-3-8b-instruct
llm: watsonx/ibm/granite-3-2b-instruct
llm: watsonx/ibm/granite-20b-multilingual

# Meta Llama models
llm: watsonx/meta-llama/llama-3-3-70b-instruct
llm: watsonx/meta-llama/llama-3-1-70b-instruct
llm: watsonx/meta-llama/llama-3-1-8b-instruct

# Mistral models
llm: watsonx/mistralai/mistral-large-2
llm: watsonx/mistralai/mixtral-8x7b-instruct-v01
```

**Other Providers:**
```yaml
# OpenAI
llm: openai/openai/gpt-4o
llm: openai/openai/gpt-4-turbo

# Anthropic
llm: anthropic/anthropic/claude-3-5-sonnet-20241022

# Groq
llm: groq/openai/gpt-oss-120b
```

---

### `description`
- **Type**: String
- **Required**: No (but highly recommended)
- **Description**: Brief explanation of the agent's purpose and capabilities
- **Best Practices**:
  - Keep it concise (1-2 sentences)
  - Clearly state what the agent does
  - Mention key capabilities or domains

**Example:**
```yaml
description: "Agent specialized in customer support for e-commerce, handling order inquiries, returns, and product questions."
```

---

### `model_type`
- **Type**: String
- **Required**: No
- **Default**: `chat`
- **Description**: Specifies the interaction model for the agent
- **Available Values**:
  - `chat` - Conversational interactions (most common)

**Example:**
```yaml
model_type: chat
```

---

### `welcome_content`
- **Type**: Object
- **Required**: No (but recommended for better UX)
- **Description**: Configures the welcome experience when users first interact with the agent
- **Properties**:
  - `welcome_message` (String): Greeting shown when conversation starts
  - `description` (String): Additional context in the welcome screen

**Example:**
```yaml
welcome_content:
  welcome_message: "👋 Hello! I'm your customer support assistant. How can I help you today?"
  description: "I can help you with orders, returns, product information, and general inquiries."
```

---

### `tags`
- **Type**: Array of Strings
- **Required**: No
- **Description**: Metadata labels for categorizing and organizing agents
- **Use Cases**:
  - Searching and filtering agents
  - Grouping related agents
  - Organizing by technology, domain, or purpose

**Example:**
```yaml
tags:
  - customer-service
  - e-commerce
  - ibm
  - watsonx
  - production
```

---

### `style`
- **Type**: String
- **Required**: No
- **Default**: `conversational`
- **Description**: Defines how the agent follows instructions and behaves
- **Available Values**:
  - `conversational` - Natural, friendly conversation style
  - `task_oriented` - Focused on completing specific tasks efficiently

**Example:**
```yaml
style: conversational
```

**Comparison:**

| Style | Behavior | Best For |
|-------|----------|----------|
| `conversational` | More natural, engaging dialogue; may ask clarifying questions | Customer support, general assistance, exploratory conversations |
| `task_oriented` | Direct, efficient task completion; minimal small talk | Automation, data processing, specific workflows |

---

### `instructions`
- **Type**: String (can be multi-line)
- **Required**: No (but highly recommended)
- **Description**: System-level instructions that guide the agent's behavior
- **Also Known As**: `system_instructions`
- **Best Practices**:
  - Be specific and clear
  - Define the agent's role and personality
  - Set boundaries and limitations
  - Include formatting preferences
  - Specify how to handle edge cases

**Example:**
```yaml
instructions: |
  You are a helpful customer support agent for an e-commerce platform.
  
  Your responsibilities:
  - Answer questions about orders, shipping, and returns
  - Provide product information and recommendations
  - Escalate complex issues to human agents
  
  Guidelines:
  - Always be polite and professional
  - If you don't know something, admit it and offer to connect them with a specialist
  - Keep responses concise but informative
  - Use bullet points for lists
  - Never make up order numbers or tracking information
```

---

### `starter_prompts`
- **Type**: Array of Strings
- **Required**: No
- **Description**: Pre-defined prompts shown to users to help them get started
- **Also Known As**: `chat_starters`
- **Best Practices**:
  - Provide 3-5 example prompts
  - Cover different use cases
  - Make them specific and actionable
  - Use natural language

**Example:**
```yaml
starter_prompts:
  - "Where is my order #12345?"
  - "I need to return an item"
  - "Tell me about your shipping policies"
  - "What's the status of my refund?"
  - "I have a question about a product"
```

---

### `tools`
- **Type**: Array of Strings
- **Required**: No
- **Description**: List of tool names that the agent can use
- **Note**: Tools must be defined separately in the `tools/` directory
- **Use Cases**:
  - API integrations
  - Database queries
  - External service calls
  - Custom functions

**Example:**
```yaml
tools:
  - order_lookup_tool
  - shipping_tracker
  - product_search
  - refund_processor
```

**Tool Definition Location:**
```
project/
├── agents/
│   └── my_agent.yaml
└── tools/
    ├── order_lookup_tool.yaml
    ├── shipping_tracker.yaml
    └── product_search.yaml
```

---

### `knowledge`
- **Type**: Array of Strings
- **Required**: No
- **Description**: List of knowledge base names the agent can access
- **Note**: Knowledge bases must be defined separately in the `knowledge/` directory
- **Use Cases**:
  - Document search
  - FAQ retrieval
  - Policy information
  - Product catalogs

**Example:**
```yaml
knowledge:
  - company_policies
  - product_catalog
  - faq_database
```

**Knowledge Base Location:**
```
project/
├── agents/
│   └── my_agent.yaml
└── knowledge/
    ├── company_policies/
    ├── product_catalog/
    └── faq_database/
```

---

### `flows`
- **Type**: Array of Strings
- **Required**: No
- **Description**: List of agentic workflow names the agent can execute
- **Note**: Flows must be defined separately in the `flows/` directory
- **Use Cases**:
  - Multi-step processes
  - Complex workflows
  - Conditional logic
  - Human-in-the-loop processes

**Example:**
```yaml
flows:
  - order_processing_flow
  - refund_workflow
  - escalation_flow
```

**Flow Definition Location:**
```
project/
├── agents/
│   └── my_agent.yaml
└── flows/
    ├── order_processing_flow.yaml
    ├── refund_workflow.yaml
    └── escalation_flow.yaml
```

---

### `collaborators`
- **Type**: Array of Strings
- **Required**: No
- **Description**: List of other agent names that this agent can delegate tasks to
- **Note**: Collaborator agents must be imported/deployed separately
- **Use Cases**:
  - Multi-agent architectures
  - Domain-specific expertise
  - Task specialization
  - Complex problem decomposition
  - Load distribution

**How It Works:**
When the primary agent receives a request, it can analyze the task and decide to delegate specific subtasks to specialized collaborator agents. The collaborator agents process their assigned tasks and return results to the primary agent, which then synthesizes the final response.

**Example:**
```yaml
collaborators:
  - tech_support_agent
  - billing_specialist_agent
  - sales_agent
```

**Multi-Agent Architecture:**
```
Primary Agent (Orchestrator)
├── Delegates technical issues → tech_support_agent
├── Delegates billing questions → billing_specialist_agent
└── Delegates sales inquiries → sales_agent
```

**Best Practices:**
- Give each collaborator a clear, specific role
- Ensure collaborator descriptions clearly state their expertise
- Avoid circular dependencies (Agent A → Agent B → Agent A)
- Test delegation logic thoroughly
- Monitor which collaborators are being used

**Collaborator Agent Requirements:**
- Must be a valid agent (native or external)
- Must be imported/deployed in the same environment
- Should have clear, specific descriptions for routing
- Can have their own tools, knowledge, and flows

---

### `icon`
- **Type**: String (SVG format)
- **Required**: No
- **Description**: An SVG-format string of an icon for the agent, displayed in the UI and channels
- **Format**: Must be a valid SVG string
- **Restrictions**:
  - Must be in SVG format
  - Must be square shape
  - Width and height must be between 64 and 100 pixels
  - Maximum file size: 200 KB

**Simple Example:**
```yaml
icon: |
  <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">
    <circle cx="32" cy="32" r="30" fill="#4A90E2"/>
    <text x="32" y="40" font-size="32" text-anchor="middle" fill="white">🤖</text>
  </svg>
```

**Complex Example (from SVG file):**
```yaml
icon: |
  <svg height="80" width="80" version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 511.985 511.985">
    <path style="fill:#ED5564;" d="M491.859,156.348c-12.891-30.483-31.342-57.865-54.842-81.372c-23.516-23.5-50.904-41.96-81.373-54.85c-31.56-13.351-65.091-20.125-99.652-20.125c-34.554,0-68.083,6.773-99.645,20.125c-30.483,12.89-57.865,31.351-81.373,54.85c-23.499,23.507-41.959,50.889-54.85,81.372C6.774,187.91,0,221.44,0,255.993c0,34.56,6.773,68.091,20.125,99.652c12.89,30.469,31.351,57.857,54.85,81.357c23.507,23.516,50.889,41.967,81.373,54.857c31.562,13.344,65.091,20.125,99.645,20.125c34.561,0,68.092-6.781,99.652-20.125c30.469-12.891,57.857-31.342,81.373-54.857c23.5-23.5,41.951-50.889,54.842-81.357c13.344-31.561,20.125-65.092,20.125-99.652C511.984,221.44,505.203,187.91,491.859,156.348z"/>
    <path style="fill:#434A54;" d="M255.992,170.66c-52.936,0-95.997,43.069-95.997,95.997s43.062,95.988,95.997,95.988s95.996-43.061,95.996-95.988C351.988,213.729,308.928,170.66,255.992,170.66z M255.992,309.335c-23.522,0-42.663-19.156-42.663-42.678c0-23.523,19.14-42.663,42.663-42.663c23.531,0,42.654,19.14,42.654,42.663C298.646,290.178,279.523,309.335,255.992,309.335z"/>
  </svg>
```

**Preparing SVG from External Sources:**

When using SVG from sources like SVG Repo, you need to:

1. **Remove XML declaration**: Delete `<?xml version="1.0" encoding="iso-8859-1"?>`
2. **Remove comments**: Delete `<!-- ... -->` lines
3. **Set dimensions**: Add `width="80" height="80"` (or 64-100px)
4. **Keep viewBox**: Preserve the `viewBox` attribute for proper scaling
5. **Simplify if needed**: Remove unnecessary paths to reduce file size
6. **Test size**: Ensure final size is under 200 KB

**Best Practices:**
- Keep the SVG simple for better performance
- Use square dimensions (e.g., 64x64, 80x80, 100x100)
- Optimize SVG to reduce file size (use tools like SVGO)
- Test icon appearance at different sizes
- Use inline SVG string (not file path)
- Remove unnecessary metadata and comments
- Preserve the `viewBox` for proper scaling

**SVG Optimization Tools:**
- [SVGOMG](https://jakearchibald.github.io/svgomg/) - Online SVG optimizer
- [SVGO](https://github.com/svg/svgo) - Node.js-based SVG optimizer

**Alternative:** You can also upload icons via the watsonx Orchestrate API using the `Create Or Update Icon For Agent` endpoint.

---

## Available Values

### Complete Field Reference Table

| Field | Type | Required | Default | Available Values |
|-------|------|----------|---------|------------------|
| `spec_version` | String | Yes | - | `v1` |
| `kind` | String | Yes | - | `native`, `external`, `watsonx_assistant` |
| `name` | String | Yes | - | Any valid identifier |
| `display_name` | String | No | - | Any string |
| `llm` | String | Yes | - | See LLM section |
| `description` | String | No | - | Any string |
| `model_type` | String | No | `chat` | `chat` |
| `welcome_content` | Object | No | - | See welcome_content section |
| `tags` | Array | No | `[]` | Array of strings |
| `style` | String | No | `conversational` | `conversational`, `task_oriented` |
| `instructions` | String | No | - | Multi-line string |
| `starter_prompts` | Array | No | `[]` | Array of strings |
| `tools` | Array | No | `[]` | Array of tool names |
| `knowledge` | Array | No | `[]` | Array of knowledge base names |
| `flows` | Array | No | `[]` | Array of flow names |
| `collaborators` | Array | No | `[]` | Array of agent names |
| `icon` | String | No | - | SVG string (64-100px, max 200KB) |

---

## Complete Examples

### Example 1: Minimal Agent
```yaml
spec_version: v1
kind: native
name: simple_agent
llm: watsonx/ibm/granite-3-8b-instruct
```

---

### Example 2: Basic Conversational Agent
```yaml
spec_version: v1
kind: native
name: customer_support_agent
display_name: "Customer Support Assistant"
llm: watsonx/ibm/granite-3-8b-instruct
description: "Helpful assistant for customer inquiries and support"
model_type: chat
welcome_content:
  welcome_message: "Hello! How can I assist you today?"
  description: "I'm here to help with your questions and concerns."
tags:
  - customer-service
  - support
```

---

### Example 3: Advanced Agent with All Features
```yaml
spec_version: v1
kind: native
name: advanced_ecommerce_agent
display_name: "E-Commerce Expert 🛍️"
llm: watsonx/meta-llama/llama-3-3-70b-instruct
description: "Comprehensive e-commerce assistant handling orders, products, and customer service"
model_type: chat
icon: |
  <svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 80 80">
    <rect width="80" height="80" rx="12" fill="#4A90E2"/>
    <text x="40" y="55" font-size="40" text-anchor="middle" fill="white">🛍️</text>
  </svg>

welcome_content:
  welcome_message: "Welcome to our store! I'm your personal shopping assistant."
  description: "I can help you find products, track orders, process returns, and answer any questions about our services."

tags:
  - e-commerce
  - customer-service
  - sales
  - watsonx
  - production

style: conversational

instructions: |
  You are an expert e-commerce assistant for a premium online retail store.
  
  Your primary responsibilities:
  1. Help customers find products that match their needs
  2. Provide detailed product information and comparisons
  3. Track order status and shipping information
  4. Process returns and refunds according to company policy
  5. Answer questions about policies, shipping, and payment methods
  
  Personality and tone:
  - Be friendly, professional, and enthusiastic
  - Show genuine interest in helping customers
  - Use emojis sparingly to add warmth
  - Be patient with confused or frustrated customers
  
  Guidelines:
  - Always verify order numbers before providing sensitive information
  - If you cannot find information, offer to escalate to a human agent
  - Suggest related products when appropriate
  - Keep responses concise but complete
  - Use bullet points for lists and comparisons
  - Never make up product details, prices, or availability
  - Always confirm before processing returns or refunds
  
  When handling complaints:
  - Acknowledge the customer's frustration
  - Apologize for any inconvenience
  - Offer concrete solutions
  - Escalate if the issue is beyond your capabilities

starter_prompts:
  - "Show me your best-selling products"
  - "Where is my order #12345?"
  - "I want to return an item"
  - "Do you have any sales or promotions?"
  - "Compare these two products for me"

tools:
  - order_lookup_tool
  - product_search_tool
  - inventory_checker
  - shipping_tracker
  - refund_processor
  - recommendation_engine

knowledge:
  - product_catalog
  - shipping_policies
  - return_policy
  - faq_database
  - promotion_rules

flows:
  - order_processing_flow
  - return_workflow
  - complaint_escalation_flow

collaborators:
  - technical_support_specialist
  - billing_specialist
```

---

### Example 4: Task-Oriented Agent
```yaml
spec_version: v1
kind: native
name: data_processor_agent
display_name: "Data Processing Agent"
llm: watsonx/ibm/granite-3-8b-instruct
description: "Automated agent for data processing and analysis tasks"
model_type: chat
style: task_oriented

instructions: |
  You are a data processing agent focused on efficiency and accuracy.
  
  Your tasks:
  - Process data files according to specifications
  - Perform data validation and quality checks
  - Generate reports and summaries
  - Execute scheduled data workflows
  
  Guidelines:
  - Be direct and concise
  - Focus on task completion
  - Report errors clearly
  - Provide status updates for long-running tasks

tools:
  - data_validator
  - file_processor
  - report_generator

flows:
  - data_pipeline_flow
  - validation_workflow
```

---

### Example 5: Multi-Language Support Agent
```yaml
spec_version: v1
kind: native
name: multilingual_support_agent
display_name: "Global Support Assistant 🌍"
llm: watsonx/ibm/granite-20b-multilingual
description: "Multilingual customer support agent supporting English, Spanish, French, German, and Japanese"
model_type: chat

welcome_content:
  welcome_message: "Hello! Hola! Bonjour! Hallo! こんにちは! How can I help you today?"
  description: "I speak multiple languages and can assist you in your preferred language."

tags:
  - multilingual
  - global-support
  - customer-service

instructions: |
  You are a multilingual customer support agent.
  
  Supported languages:
  - English
  - Spanish (Español)
  - French (Français)
  - German (Deutsch)
  - Japanese (日本語)
  
  Guidelines:
  - Detect the customer's language from their first message
  - Respond in the same language throughout the conversation
  - If unsure about the language, ask politely
  - Maintain the same level of professionalism in all languages
  - Use culturally appropriate greetings and expressions

starter_prompts:
  - "I need help with my order"
  - "Necesito ayuda con mi pedido"
  - "J'ai besoin d'aide avec ma commande"
  - "Ich brauche Hilfe bei meiner Bestellung"
  - "注文について助けが必要です"

tools:
  - translation_tool
  - order_lookup_tool
  - multilingual_knowledge_search
```

---

## Best Practices

### 1. Naming Conventions
- **name**: Use lowercase with underscores (e.g., `customer_support_agent`)
- **display_name**: Use proper capitalization and spaces (e.g., `"Customer Support Agent"`)
- Keep names descriptive but concise

### 2. Instructions
- Be specific about the agent's role and capabilities
- Include personality traits and tone guidelines
- Define boundaries and limitations
- Provide examples of desired behavior
- Use multi-line format with `|` for readability

### 3. LLM Selection
- **Granite 3-8B**: Good balance of performance and cost for most use cases
- **Llama 3.3-70B**: Better for complex reasoning and nuanced conversations
- **Granite-20B-Multilingual**: Best for multi-language support
- Consider cost, latency, and capability requirements

### 4. Welcome Content
- Make the welcome message friendly and inviting
- Clearly state what the agent can do
- Set appropriate expectations
- Keep it concise (1-2 sentences each)

### 5. Starter Prompts
- Provide 3-5 diverse examples
- Cover main use cases
- Use natural, conversational language
- Make them specific and actionable

### 6. Tags
- Use consistent naming conventions
- Include relevant categories (domain, technology, environment)
- Keep tags lowercase with hyphens
- Don't overuse tags (5-10 is usually sufficient)

### 7. Tools, Knowledge, and Flows
- Only include what the agent actually needs
- Ensure referenced resources exist in your project
- Document dependencies clearly
- Test integrations thoroughly

### 8. Style Selection
- Use `conversational` for customer-facing agents
- Use `task_oriented` for automation and backend processes
- Consider your use case and user expectations

### 9. Testing
- Test with various user inputs
- Verify tool and knowledge base integrations
- Check multi-turn conversations
- Validate error handling
- Test edge cases

### 10. Documentation
- Keep this reference handy
- Document custom configurations
- Maintain version history
- Share knowledge with your team

---

## Additional Resources

### Official Documentation
- [watsonx Orchestrate ADK Documentation](https://developer.watson-orchestrate.ibm.com/)
- [Authoring Native Agents](https://developer.watson-orchestrate.ibm.com/agents/build_agent)
- [Agent Descriptions and Instructions](https://developer.watson-orchestrate.ibm.com/agents/descriptions)
- [Choosing Agent Styles](https://developer.watson-orchestrate.ibm.com/agents/agent_styles)

### Related Topics
- Tools: Define custom tools for your agents
- Knowledge Bases: Create searchable knowledge repositories
- Agentic Workflows: Build complex multi-step processes
- LLM Management: Configure and manage language models

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-25 | Initial comprehensive reference guide |

---

## Questions or Issues?

If you have questions about agent configuration or encounter issues:
1. Check the official documentation
2. Review the examples in this guide
3. Test with minimal configurations first
4. Gradually add complexity

---

**Happy Agent Building! 🚀**