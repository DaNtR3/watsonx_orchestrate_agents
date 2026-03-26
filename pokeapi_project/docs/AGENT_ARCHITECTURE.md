# watsonx Orchestrate Agent Architecture Guide

## Overview
This guide explains the architecture and relationships between all components in watsonx Orchestrate: Agents, Tools, Flows, Knowledge Bases, Connections, and Collaborators. Understanding these relationships is crucial for building effective AI agents.

---

## Table of Contents
1. [High-Level Architecture](#high-level-architecture)
2. [Core Components](#core-components)
3. [Component Relationships](#component-relationships)
4. [Project Structure](#project-structure)
5. [How Agents Use Resources](#how-agents-use-resources)
6. [Building an Agent: Step-by-Step](#building-an-agent-step-by-step)
7. [Advanced Patterns](#advanced-patterns)
8. [Best Practices](#best-practices)

---

## High-Level Architecture

```
                                    ┌─────────────────┐
                                    │   👤 USER       │
                                    └────────┬────────┘
                                             │
                                             │ Interacts with
                                             ▼
                    ┌────────────────────────────────────────────┐
                    │          🤖 AGENT (Central Hub)            │
                    │                                            │
                    │  • Orchestrates all interactions           │
                    │  • Makes decisions                         │
                    │  • Maintains context                       │
                    └─┬──────┬──────┬──────┬──────┬─────────────┘
                      │      │      │      │      │
         ┌────────────┘      │      │      │      └────────────┐
         │                   │      │      │                   │
         ▼                   ▼      ▼      ▼                   ▼
    ┌─────────┐      ┌──────────┐ ┌──────────┐      ┌──────────────┐
    │ 🧠 LLM  │      │ 🔧 TOOLS │ │ 📚 KNOW- │      │ 🤝 COLLABO-  │
    │  Model  │      │          │ │   LEDGE  │      │    RATORS    │
    └─────────┘      └────┬─────┘ └────┬─────┘      └──────────────┘
                          │            │
                          │            │
                          ▼            ▼
                   ┌─────────────┐ ┌──────────┐
                   │ 🔌 CONNECT- │ │ 📄 DOCS  │
                   │    IONS     │ │ 🔍 RAG   │
                   └──────┬──────┘ └──────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │ 🌐 EXTERNAL │
                   │    APIs     │
                   └─────────────┘

         ┌──────────────────────────────────────┐
         │     🔄 AGENTIC WORKFLOWS (FLOWS)     │
         │                                      │
         │  ┌──────┐  ┌──────┐  ┌──────┐      │
         │  │Agent │  │Tool  │  │Cond. │      │
         │  │Node  │  │Node  │  │Node  │      │
         │  └──────┘  └──────┘  └──────┘      │
         └──────────────────────────────────────┘
```

**Component Relationships:**
- **Agent** is the central orchestrator
- **LLM** provides intelligence and language understanding
- **Tools** extend capabilities with external actions
- **Knowledge** provides context through document search
- **Flows** enable complex multi-step processes
- **Collaborators** are specialized agents for specific tasks
- **Connections** securely manage credentials for external APIs

---

## Core Components

### 1. 🤖 **Agent**
The central AI entity that orchestrates all interactions.

**Key Characteristics:**
- Powered by an LLM (Large Language Model)
- Has a specific role and personality (defined by instructions)
- Can use multiple resources (tools, knowledge, flows, collaborators)
- Maintains conversation context
- Makes decisions about which resources to use

**Types:**
- **Native Agent**: Runs on IBM infrastructure
- **External Agent**: Connects to external AI services
- **watsonx Assistant Agent**: Integration with watsonx Assistant

---

### 2. 🔧 **Tools**
Executable functions that extend agent capabilities.

**Key Characteristics:**
- Perform specific actions (API calls, calculations, data processing)
- Can be OpenAPI-based or Python-based
- May require connections for authentication
- Have defined inputs and outputs
- Can be called by agents or flows

**Types:**
- **OpenAPI Tools**: REST API integrations
- **Python Tools**: Custom Python functions
- **Built-in Tools**: Pre-configured system tools

---

### 3. 📚 **Knowledge Bases**
Searchable repositories of information using RAG (Retrieval-Augmented Generation).

**Key Characteristics:**
- Store documents, PDFs, text files
- Use vector embeddings for semantic search
- Provide context to agents
- Support multiple document formats
- Enable "chat with documents" functionality

**Use Cases:**
- Company policies and procedures
- Product documentation
- FAQs and help articles
- Technical manuals
- Historical data

---

### 4. 🔄 **Agentic Workflows (Flows)**
Multi-step processes with conditional logic and control flow.

**Key Characteristics:**
- Define complex, multi-step operations
- Support conditional branching (if-then-else)
- Can include loops and parallel execution
- Combine agents, tools, and built-in nodes
- Support human-in-the-loop interactions

**Node Types:**
- **Agent Nodes**: Call other agents
- **Tool Nodes**: Execute tools
- **Conditional Nodes**: Branch based on conditions
- **Loop Nodes**: Repeat operations
- **Human Input Nodes**: Request user input
- **Generative Prompt Nodes**: Direct LLM calls

---

### 5. 🔌 **Connections**
Secure credential management for external services.

**Key Characteristics:**
- Store authentication credentials securely
- Support multiple auth methods (API Key, OAuth, Basic Auth)
- Can be shared across multiple tools
- Environment-specific (dev, staging, production)
- Managed separately from code

**Authentication Types:**
- API Key
- Bearer Token
- Basic Authentication
- OAuth 2.0
- Custom Headers

---

### 6. 🤝 **Collaborator Agents**
Other agents that can be called by a primary agent.

**Key Characteristics:**
- Specialized agents for specific tasks
- Enable multi-agent architectures
- Can be native or external agents
- Receive delegated tasks from primary agent
- Return results to calling agent

**Use Cases:**
- Domain-specific expertise
- Task specialization
- Load distribution
- Modular architecture

---

## Component Relationships

### Detailed Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         AGENT ECOSYSTEM                                 │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │              🤖 AGENT (my_agent.yaml)                            │  │
│  │                                                                  │  │
│  │  Configuration:                                                  │  │
│  │  ├─ 🧠 LLM: granite-3-8b-instruct                               │  │
│  │  ├─ 📝 Instructions: System prompt                              │  │
│  │  └─ 🎨 Style: conversational                                    │  │
│  └────┬─────────┬──────────┬──────────┬────────────────────────────┘  │
│       │         │          │          │                               │
│       ▼         ▼          ▼          ▼                               │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐                       │
│  │ TOOLS  │ │KNOWL-  │ │ FLOWS  │ │COLLABO-  │                       │
│  │        │ │ EDGE   │ │        │ │ RATORS   │                       │
│  └───┬────┘ └───┬────┘ └───┬────┘ └──────────┘                       │
│      │          │          │                                          │
│      │          │          │                                          │
│  ┌───▼──────────▼──────────▼────────────────────────────────────┐    │
│  │                                                               │    │
│  │  TOOL DEPENDENCIES:                                           │    │
│  │  ┌──────────────┐        ┌──────────────┐                    │    │
│  │  │ 🔧 Tool 1    │        │ 🔧 Tool 2    │                    │    │
│  │  │  (OpenAPI)   │        │  (Python)    │                    │    │
│  │  └──────┬───────┘        └──────┬───────┘                    │    │
│  │         │                       │                             │    │
│  │         ▼                       ▼                             │    │
│  │  ┌──────────────┐        ┌──────────────┐                    │    │
│  │  │🔌 Connection │        │🔌 Connection │                    │    │
│  │  │   (API Key)  │        │   (OAuth2)   │                    │    │
│  │  └──────┬───────┘        └──────┬───────┘                    │    │
│  │         │                       │                             │    │
│  │         └───────┬───────────────┘                             │    │
│  │                 ▼                                             │    │
│  │          🌐 External APIs                                     │    │
│  │                                                               │    │
│  │  KNOWLEDGE STRUCTURE:                                         │    │
│  │  ┌──────────────────────────────────┐                        │    │
│  │  │ 📚 Knowledge Base 1 (Policies)   │                        │    │
│  │  │  ├─ 📄 Documents (PDF, DOCX)     │                        │    │
│  │  │  └─ 🔍 Vector Index (Embeddings) │                        │    │
│  │  └──────────────────────────────────┘                        │    │
│  │                                                               │    │
│  │  FLOW STRUCTURE:                                              │    │
│  │  ┌────────────────────────────────────────┐                  │    │
│  │  │ 🔄 Flow 1 (Workflow)                   │                  │    │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────┐ │                  │    │
│  │  │  │📦 Agent  │→ │📦 Tool   │→ │📦Cond│ │                  │    │
│  │  │  │   Node   │  │   Node   │  │ Node │ │                  │    │
│  │  │  └──────────┘  └──────────┘  └──────┘ │                  │    │
│  │  └────────────────────────────────────────┘                  │    │
│  └───────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### Relationship Matrix

| Component | Can Use | Can Be Used By | Requires |
|-----------|---------|----------------|----------|
| **Agent** | Tools, Knowledge, Flows, Collaborators, LLM | Flows (as nodes), Other Agents (as collaborators) | LLM |
| **Tool** | Connections | Agents, Flows | - |
| **Knowledge Base** | Documents, Vector Index | Agents | Documents |
| **Flow** | Agents, Tools, Built-in Nodes | Agents | - |
| **Connection** | External APIs | Tools | Credentials |
| **Collaborator** | All agent resources | Primary Agent | - |

---

## Project Structure

### Standard Directory Layout

```
my_project/
├── agents/                          # Agent definitions
│   ├── main_agent.yaml             # Primary agent
│   ├── specialist_agent.yaml       # Collaborator agent
│   └── support_agent.yaml          # Another collaborator
│
├── tools/                           # Tool definitions
│   ├── api_tools/
│   │   ├── weather_api.yaml        # OpenAPI tool
│   │   └── payment_api.yaml        # OpenAPI tool
│   └── python_tools/
│       ├── calculator.py           # Python tool
│       └── data_processor.py       # Python tool
│
├── knowledge/                       # Knowledge bases
│   ├── company_policies/
│   │   ├── hr_policy.pdf
│   │   ├── security_policy.pdf
│   │   └── config.yaml
│   └── product_docs/
│       ├── manual.pdf
│       └── config.yaml
│
├── flows/                           # Agentic workflows
│   ├── order_processing.py         # Flow definition
│   ├── customer_onboarding.py      # Flow definition
│   └── escalation_flow.py          # Flow definition
│
├── connections/                     # Connection definitions
│   ├── api_connections.yaml        # API credentials
│   └── oauth_connections.yaml      # OAuth configs
│
├── .env                            # Environment variables
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

---

## How Agents Use Resources

### 1. Agent → Tool Interaction

```
┌──────┐                                                      ┌─────────┐
│ USER │                                                      │   API   │
└──┬───┘                                                      └────▲────┘
   │                                                               │
   │ "What's the weather in NYC?"                                 │
   ▼                                                               │
┌────────┐    ┌───────┐    ┌──────┐    ┌────────────┐           │
│ AGENT  │───▶│  LLM  │    │ TOOL │    │ CONNECTION │           │
└────┬───┘    └───┬───┘    └──┬───┘    └─────┬──────┘           │
     │            │           │              │                   │
     │ 1. Analyze │           │              │                   │
     │───────────▶│           │              │                   │
     │            │           │              │                   │
     │ 2. Need    │           │              │                   │
     │   weather_ │           │              │                   │
     │   tool     │           │              │                   │
     │◀───────────│           │              │                   │
     │                        │              │                   │
     │ 3. Call weather_tool   │              │                   │
     │   (city="NYC")         │              │                   │
     │───────────────────────▶│              │                   │
     │                        │              │                   │
     │                        │ 4. Get creds │                   │
     │                        │─────────────▶│                   │
     │                        │              │                   │
     │                        │ 5. API key   │                   │
     │                        │◀─────────────│                   │
     │                        │                                  │
     │                        │ 6. GET /weather?city=NYC         │
     │                        │──────────────────────────────────▶
     │                        │                                  │
     │                        │ 7. Weather data                  │
     │                        │◀──────────────────────────────────
     │                        │              │                   │
     │ 8. Return data         │              │                   │
     │◀───────────────────────│              │                   │
     │            │           │              │                   │
     │ 9. Format  │           │              │                   │
     │───────────▶│           │              │                   │
     │            │           │              │                   │
     │ 10. Response           │              │                   │
     │◀───────────│           │              │                   │
     │                        │              │                   │
     ▼                                                            │
   USER: "It's 72°F and sunny in NYC"                            │
```

**YAML Configuration:**
```yaml
# agents/weather_agent.yaml
spec_version: v1
kind: native
name: weather_agent
llm: watsonx/ibm/granite-3-8b-instruct
tools:
  - weather_api_tool
```

```yaml
# tools/weather_api_tool.yaml
spec_version: v1
kind: openapi
name: weather_api_tool
openapi_spec: ./weather_openapi.yaml
connection: weather_api_connection
```

---

### 2. Agent → Knowledge Base Interaction

```
┌──────┐
│ USER │
└──┬───┘
   │ "What's the return policy?"
   ▼
┌────────┐    ┌───────┐    ┌───────────┐    ┌───────────┐
│ AGENT  │───▶│  LLM  │    │ KNOWLEDGE │    │ VECTOR DB │
└────┬───┘    └───┬───┘    └─────┬─────┘    └─────┬─────┘
     │            │              │                │
     │ 1. Analyze │              │                │
     │───────────▶│              │                │
     │            │              │                │
     │ 2. Need    │              │                │
     │   policy   │              │                │
     │◀───────────│              │                │
     │                           │                │
     │ 3. Search "return policy" │                │
     │──────────────────────────▶│                │
     │                           │                │
     │                           │ 4. Vector      │
     │                           │    similarity  │
     │                           │    search      │
     │                           │───────────────▶│
     │                           │                │
     │                           │ 5. Relevant    │
     │                           │    chunks      │
     │                           │◀───────────────│
     │                           │                │
     │ 6. Return context         │                │
     │◀──────────────────────────│                │
     │            │              │                │
     │ 7. Generate│              │                │
     │   with     │              │                │
     │   context  │              │                │
     │───────────▶│              │                │
     │            │              │                │
     │ 8. Response│              │                │
     │◀───────────│              │                │
     │                           │                │
     ▼
   USER: "Our return policy allows returns within 30 days..."
```

**YAML Configuration:**
```yaml
# agents/support_agent.yaml
spec_version: v1
kind: native
name: support_agent
llm: watsonx/ibm/granite-3-8b-instruct
knowledge:
  - company_policies
  - product_documentation
```

---

### 3. Agent → Flow Interaction

```
┌──────┐
│ USER │
└──┬───┘
   │ "Process my order"
   ▼
┌────────┐    ┌──────────┐    ┌───────┐    ┌───────┐    ┌──────────┐
│ AGENT  │───▶│   FLOW   │───▶│ TOOL1 │    │ TOOL2 │    │  HUMAN   │
└────┬───┘    └────┬─────┘    └───┬───┘    └───┬───┘    └────┬─────┘
     │             │              │            │             │
     │ 1. Execute  │              │            │             │
     │    flow     │              │            │             │
     │────────────▶│              │            │             │
     │             │              │            │             │
     │             │ 2. Validate  │            │             │
     │             │─────────────▶│            │             │
     │             │              │            │             │
     │             │ 3. Valid     │            │             │
     │             │◀─────────────│            │             │
     │             │                           │             │
     │             │ 4. Check inventory        │             │
     │             │──────────────────────────▶│             │
     │             │                           │             │
     │             │ 5. In stock               │             │
     │             │◀──────────────────────────│             │
     │             │                                         │
     │             │ 6. Request approval                     │
     │             │────────────────────────────────────────▶│
     │             │                                         │
     │             │ 7. Approved                             │
     │             │◀────────────────────────────────────────│
     │             │              │            │             │
     │             │ 8. Process   │            │             │
     │             │    payment   │            │             │
     │             │─────────────▶│            │             │
     │             │              │            │             │
     │             │ 9. Success   │            │             │
     │             │◀─────────────│            │             │
     │             │              │            │             │
     │ 10. Complete│              │            │             │
     │◀────────────│              │            │             │
     │                            │            │             │
     ▼
   USER: "Order processed successfully!"
```

**YAML Configuration:**
```yaml
# agents/order_agent.yaml
spec_version: v1
kind: native
name: order_agent
llm: watsonx/ibm/granite-3-8b-instruct
flows:
  - order_processing_flow
  - refund_flow
```

---

### 4. Agent → Collaborator Interaction

```
┌──────┐
│ USER │
└──┬───┘
   │ "I need technical support"
   ▼
┌──────────────┐    ┌───────┐    ┌────────────────────┐
│  MAIN AGENT  │───▶│  LLM  │    │ SPECIALIST AGENT   │
│ (Orchestrator)│    └───┬───┘    │ (Tech Support)     │
└──────┬───────┘        │         └─────────┬──────────┘
       │                │                   │
       │ 1. Analyze     │                   │
       │───────────────▶│                   │
       │                │                   │
       │ 2. Delegate to │                   │
       │    tech_support│                   │
       │◀───────────────│                   │
       │                                    │
       │ 3. Forward request                 │
       │───────────────────────────────────▶│
       │                                    │
       │                                    │ 4. Process
       │                                    │    technical
       │                                    │    query
       │                                    │
       │ 5. Return solution                 │
       │◀───────────────────────────────────│
       │                                    │
       ▼
     USER: "Here's the technical solution..."
```

**YAML Configuration:**
```yaml
# agents/main_agent.yaml
spec_version: v1
kind: native
name: main_agent
llm: watsonx/ibm/granite-3-8b-instruct
collaborators:
  - tech_support_agent
  - billing_agent
  - sales_agent
```

---

## Building an Agent: Step-by-Step

### Step 1: Define Your Agent's Purpose

**Questions to Answer:**
- What problem does this agent solve?
- Who are the users?
- What capabilities does it need?
- What resources will it use?

**Example:**
```
Purpose: Customer support agent for e-commerce
Users: Customers with orders, returns, product questions
Capabilities: Order tracking, returns processing, product info
Resources: Order API tool, product knowledge base, refund flow
```

---

### Step 2: Create the Agent YAML

```yaml
# agents/customer_support_agent.yaml
spec_version: v1
kind: native
name: customer_support_agent
display_name: "Customer Support Assistant"
llm: watsonx/ibm/granite-3-8b-instruct
description: "Helpful assistant for customer inquiries about orders, returns, and products"

instructions: |
  You are a friendly customer support agent for an e-commerce store.
  
  Your responsibilities:
  - Help customers track their orders
  - Process return requests
  - Answer product questions
  - Escalate complex issues
  
  Always be polite, patient, and helpful.

welcome_content:
  welcome_message: "Hi! How can I help you today?"
  description: "I can help with orders, returns, and product questions."

starter_prompts:
  - "Where is my order?"
  - "I want to return an item"
  - "Tell me about this product"

tags:
  - customer-service
  - e-commerce
```

---

### Step 3: Create Required Tools

```yaml
# tools/order_lookup_tool.yaml
spec_version: v1
kind: openapi
name: order_lookup_tool
display_name: "Order Lookup"
description: "Look up order status by order number"
openapi_spec: ./order_api_spec.yaml
connection: order_api_connection
```

```python
# tools/refund_calculator.py
from wxo.adk.tools import tool

@tool(
    name="refund_calculator",
    description="Calculate refund amount based on order details"
)
def calculate_refund(order_total: float, days_since_purchase: int) -> dict:
    """Calculate refund with depreciation."""
    if days_since_purchase <= 30:
        refund_percentage = 100
    elif days_since_purchase <= 60:
        refund_percentage = 80
    else:
        refund_percentage = 50
    
    refund_amount = order_total * (refund_percentage / 100)
    
    return {
        "refund_amount": refund_amount,
        "refund_percentage": refund_percentage
    }
```

---

### Step 4: Create Knowledge Bases

```
knowledge/
└── product_catalog/
    ├── products.pdf
    ├── specifications.pdf
    └── config.yaml
```

```yaml
# knowledge/product_catalog/config.yaml
spec_version: v1
name: product_catalog
display_name: "Product Catalog"
description: "Complete product information and specifications"
```

---

### Step 5: Create Agentic Workflows (Optional)

```python
# flows/return_processing_flow.py
from wxo.adk.flows import flow, agent_node, tool_node, conditional_node

@flow(
    name="return_processing_flow",
    description="Process customer return requests"
)
def return_processing_flow(order_number: str, reason: str):
    # Step 1: Validate order
    order_info = tool_node(
        tool="order_lookup_tool",
        inputs={"order_number": order_number}
    )
    
    # Step 2: Check eligibility
    is_eligible = conditional_node(
        condition=order_info.days_since_purchase <= 60,
        if_true="eligible",
        if_false="not_eligible"
    )
    
    if is_eligible == "eligible":
        # Step 3: Calculate refund
        refund = tool_node(
            tool="refund_calculator",
            inputs={
                "order_total": order_info.total,
                "days_since_purchase": order_info.days_since_purchase
            }
        )
        
        # Step 4: Process refund
        result = tool_node(
            tool="process_refund_tool",
            inputs={
                "order_number": order_number,
                "amount": refund.refund_amount
            }
        )
        
        return {"status": "approved", "refund": refund.refund_amount}
    else:
        return {"status": "denied", "reason": "Outside return window"}
```

---

### Step 6: Configure Connections

```yaml
# connections/api_connections.yaml
spec_version: v1
connections:
  - name: order_api_connection
    type: api_key
    credentials:
      api_key: ${ORDER_API_KEY}
      header_name: X-API-Key
    
  - name: payment_api_connection
    type: oauth2
    credentials:
      client_id: ${PAYMENT_CLIENT_ID}
      client_secret: ${PAYMENT_CLIENT_SECRET}
      token_url: https://api.payment.com/oauth/token
```

---

### Step 7: Link Resources to Agent

```yaml
# agents/customer_support_agent.yaml (updated)
spec_version: v1
kind: native
name: customer_support_agent
display_name: "Customer Support Assistant"
llm: watsonx/ibm/granite-3-8b-instruct

# ... (previous configuration)

tools:
  - order_lookup_tool
  - refund_calculator
  - process_refund_tool

knowledge:
  - product_catalog
  - return_policies

flows:
  - return_processing_flow
  - order_tracking_flow
```

---

### Step 8: Test and Deploy

```bash
# Import the agent
orchestrate agents import agents/customer_support_agent.yaml

# Test the agent
orchestrate agents chat customer_support_agent

# Deploy to environment
orchestrate agents deploy customer_support_agent --env production
```

---

## Advanced Patterns

### Pattern 1: Multi-Agent Collaboration

```
                           ┌──────────┐
                           │   USER   │
                           └─────┬────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │   🤖 MAIN AGENT        │
                    │   (Orchestrator)       │
                    └──┬──────────┬─────────┬┘
                       │          │         │
         ┌─────────────┘          │         └─────────────┐
         │                        │                       │
         ▼                        ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ 🤖 TECHNICAL    │    │ 🤖 BILLING      │    │ 🤖 SALES        │
│    SUPPORT      │    │    AGENT        │    │    AGENT        │
│    SPECIALIST   │    │    SPECIALIST   │    │    SPECIALIST   │
└────────┬────────┘    └────────┬────────┘    └────────┬────────┘
         │                      │                       │
         ▼                      ▼                       ▼
    ┌─────────┐           ┌─────────┐            ┌─────────┐
    │🔧 Tech  │           │🔧 Billing│            │🔧 Sales │
    │  Tools  │           │  Tools   │            │  Tools  │
    └────┬────┘           └────┬─────┘            └────┬────┘
         │                     │                       │
         ▼                     ▼                       ▼
    ┌─────────┐           ┌─────────┐            ┌─────────┐
    │📚 Tech  │           │📚 Billing│            │📚 Product│
    │   Docs  │           │ Policies │            │ Catalog │
    └─────────┘           └──────────┘            └─────────┘

Routing Logic:
• Technical issues    → Technical Support Specialist
• Billing questions   → Billing Agent Specialist
• Product inquiries   → Sales Agent Specialist
• General questions   → Main Agent handles directly
```

**Configuration:**
```yaml
# agents/main_orchestrator.yaml
spec_version: v1
kind: native
name: main_orchestrator
llm: watsonx/meta-llama/llama-3-3-70b-instruct
description: "Main agent that routes requests to specialists"

instructions: |
  You are an orchestrator agent that routes customer requests to specialists.
  
  Routing rules:
  - Technical issues → tech_support_agent
  - Billing questions → billing_agent
  - Product inquiries → sales_agent
  - General questions → handle yourself

collaborators:
  - tech_support_agent
  - billing_agent
  - sales_agent
```

---

### Pattern 2: Tool Chain with Dependencies

```
┌──────────┐
│ 🤖 AGENT │
└─────┬────┘
      │
      ▼
┌──────────────────┐
│ 🔧 Tool 1:       │
│ Validate Input   │
└─────┬────────────┘
      │
      ▼
┌──────────────────┐      ┌─────────────────┐
│ 🔧 Tool 2:       │─────▶│ 🔌 Connection 1 │
│ Fetch Data       │      │ (API Auth)      │
└─────┬────────────┘      └─────────────────┘
      │
      ▼
┌──────────────────┐
│ 🔧 Tool 3:       │
│ Transform Data   │
└─────┬────────────┘
      │
      ▼
┌──────────────────┐      ┌─────────────────┐
│ 🔧 Tool 4:       │─────▶│ 🔌 Connection 2 │
│ Store Result     │      │ (DB Auth)       │
└──────────────────┘      └─────────────────┘
```

**Best Practice:** Use flows for complex tool chains with dependencies.

---

### Pattern 3: Knowledge-Enhanced Agent

```
┌──────────────┐
│  USER QUERY  │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────────────────┐
│                   🤖 AGENT                           │
└──┬────────────┬────────────┬────────────┬───────────┘
   │            │            │            │
   │            │            │            │
   ▼            ▼            ▼            ▼
┌────────┐  ┌────────┐  ┌────────┐  ┌─────────┐
│📚 KB:  │  │📚 KB:  │  │📚 KB:  │  │ 🧠 LLM  │
│Policies│  │Products│  │  FAQs  │  └────┬────┘
└───┬────┘  └───┬────┘  └───┬────┘       │
    │           │           │            │
    │           │           │            │
    ▼           ▼           ▼            │
┌─────────┐ ┌─────────┐ ┌─────────┐     │
│🔍 RAG   │ │🔍 RAG   │ │🔍 RAG   │     │
│ Search  │ │ Search  │ │ Search  │     │
└────┬────┘ └────┬────┘ └────┬────┘     │
     │           │           │          │
     └───────────┴───────────┴──────────┘
                 │
                 ▼
         ┌───────────────┐
         │  📄 CONTEXT   │
         │  (Combined)   │
         └───────┬───────┘
                 │
                 ▼
         ┌───────────────┐
         │   🧠 LLM      │
         │  (Generate)   │
         └───────┬───────┘
                 │
                 ▼
         ┌───────────────┐
         │ 💬 RESPONSE   │
         └───────┬───────┘
                 │
                 ▼
            ┌────────┐
            │  USER  │
            └────────┘
```

---

### Pattern 4: Human-in-the-Loop Flow

```
┌──────┐
│ USER │
└──┬───┘
   │ Request action
   ▼
┌────────┐
│ AGENT  │
└───┬────┘
    │ Execute workflow
    ▼
┌──────────────────────────────────────────────────────┐
│                    FLOW                              │
│                                                      │
│  Step 1: Automated                                   │
│  ┌──────────────┐                                    │
│  │ 🔧 Tool      │                                    │
│  │ (Validate)   │                                    │
│  └──────┬───────┘                                    │
│         │ Result                                     │
│         ▼                                            │
│  Step 2: Automated                                   │
│  ┌──────────────┐                                    │
│  │ 🔧 Tool      │                                    │
│  │ (Process)    │                                    │
│  └──────┬───────┘                                    │
│         │ Result                                     │
│         ▼                                            │
│  Step 3: Human Checkpoint                            │
│  ┌──────────────┐                                    │
│  │ 👤 HUMAN     │                                    │
│  │ (Approval)   │                                    │
│  └──────┬───────┘                                    │
│         │                                            │
│    ┌────┴────┐                                       │
│    │         │                                       │
│    ▼         ▼                                       │
│ APPROVED  REJECTED                                   │
│    │         │                                       │
│    │         └──────────────┐                        │
│    ▼                        │                        │
│  Step 4: Final              │                        │
│  ┌──────────────┐           │                        │
│  │ 🔧 Tool      │           │                        │
│  │ (Execute)    │           │                        │
│  └──────┬───────┘           │                        │
│         │ Success           │ Cancel                 │
│         ▼                   ▼                        │
└─────────┼───────────────────┼────────────────────────┘
          │                   │
          ▼                   ▼
      ┌────────┐          ┌────────┐
      │ AGENT  │          │ AGENT  │
      └───┬────┘          └───┬────┘
          │                   │
          ▼                   ▼
        USER:               USER:
      "Done!"          "Action cancelled"
```

---

## Best Practices

### 1. Agent Design
✅ **DO:**
- Give agents clear, specific roles
- Write detailed instructions
- Use appropriate LLM for the task
- Test with real user scenarios
- Monitor performance and costs

❌ **DON'T:**
- Create overly broad agents
- Use vague instructions
- Over-provision resources
- Skip testing
- Ignore user feedback

---

### 2. Tool Design
✅ **DO:**
- Make tools single-purpose
- Provide clear descriptions
- Handle errors gracefully
- Use connections for credentials
- Document inputs/outputs

❌ **DON'T:**
- Create monolithic tools
- Hardcode credentials
- Ignore error cases
- Skip input validation
- Leave tools undocumented

---

### 3. Knowledge Base Design
✅ **DO:**
- Organize by topic/domain
- Keep documents up-to-date
- Use clear, searchable content
- Test retrieval quality
- Monitor usage patterns

❌ **DON'T:**
- Mix unrelated content
- Use outdated information
- Include poor-quality documents
- Ignore retrieval accuracy
- Forget to update regularly

---

### 4. Flow Design
✅ **DO:**
- Break complex processes into steps
- Use conditional logic appropriately
- Include error handling
- Add human checkpoints for critical actions
- Test all branches

❌ **DON'T:**
- Create overly complex flows
- Skip error handling
- Automate everything without oversight
- Forget edge cases
- Leave flows untested

---

### 5. Connection Management
✅ **DO:**
- Use environment variables
- Rotate credentials regularly
- Limit connection scope
- Monitor connection usage
- Document connection requirements

❌ **DON'T:**
- Hardcode credentials
- Share connections unnecessarily
- Use overly permissive credentials
- Ignore security best practices
- Leave unused connections

---

### 6. Collaborator Design
✅ **DO:**
- Create specialized agents
- Define clear boundaries
- Document collaboration patterns
- Test inter-agent communication
- Monitor delegation patterns

❌ **DON'T:**
- Create duplicate functionality
- Use unclear delegation rules
- Skip testing collaborations
- Create circular dependencies
- Over-complicate architecture

---

## Resource Dependency Graph

```
┌─────────────────────────────────────────────────────────────────┐
│                        AGENT LAYER                              │
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │ 🤖 Main      │───▶│ 🤖 Collab 1  │    │ 🤖 Collab 2  │     │
│  │    Agent     │    │              │    │              │     │
│  └──┬───┬───┬───┘    └──┬───────┬───┘    └──────────────┘     │
│     │   │   │           │       │                              │
└─────┼───┼───┼───────────┼───────┼──────────────────────────────┘
      │   │   │           │       │
      │   │   │           │       │
┌─────┼───┼───┼───────────┼───────┼──────────────────────────────┐
│     │   │   │           │       │   CAPABILITY LAYER           │
│     │   │   │           │       │                              │
│     ▼   ▼   ▼           ▼       ▼                              │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐  ┌──────────┐            │
│  │🔧  │ │🔧  │ │📚  │ │🔧  │ │📚  │  │ 🔄 Flow 1│            │
│  │T1  │ │T2  │ │K1  │ │T3  │ │K2  │  │          │            │
│  └─┬──┘ └─┬──┘ └─┬──┘ └─┬──┘ └─┬──┘  └─┬──┬──┬──┘            │
│    │      │      │      │      │       │  │  │                │
└────┼──────┼──────┼──────┼──────┼───────┼──┼──┼────────────────┘
     │      │      │      │      │       │  │  │
     │      │      │      │      │       │  │  └──────┐
┌────┼──────┼──────┼──────┼──────┼───────┼──┼─────────┼─────────┐
│    │      │      │      │      │       │  │         │  INFRA  │
│    │      │      │      │      │       │  │         │  LAYER  │
│    ▼      ▼      ▼      ▼      ▼       │  │         │         │
│  ┌────────┐   ┌────────┐   ┌────────┐ │  │         │         │
│  │🔌 Conn1│   │🔌 Conn2│   │📄 Docs │ │  │         │         │
│  └───┬────┘   └───┬────┘   └────────┘ │  │         │         │
│      │            │                    │  │         │         │
│      ▼            ▼                    │  │         │         │
│  ┌────────┐   ┌────────┐              │  │         │         │
│  │🌐 API1 │   │🌐 API2 │              │  │         │         │
│  └────────┘   └────────┘              │  │         │         │
│                                        │  │         │         │
│  Flow 1 uses: ─────────────────────────┘  │         │         │
│    • Tool 1 (via Connection 1)            │         │         │
│    • Tool 2 (via Connection 1)            │         │         │
│    • Collaborator 1 ──────────────────────┘         │         │
│                                                      │         │
└──────────────────────────────────────────────────────┴─────────┘

Legend:
  🤖 = Agent    🔧 = Tool    📚 = Knowledge    🔄 = Flow
  🔌 = Connection    📄 = Documents    🌐 = External API
```

---

## Quick Reference: Component Checklist

### When Creating an Agent:
- [ ] Define purpose and scope
- [ ] Choose appropriate LLM
- [ ] Write clear instructions
- [ ] Configure welcome content
- [ ] Add starter prompts
- [ ] Link required tools
- [ ] Link knowledge bases
- [ ] Link flows
- [ ] Add collaborators (if needed)
- [ ] Test thoroughly
- [ ] Document usage

### When Creating a Tool:
- [ ] Define single, clear purpose
- [ ] Write descriptive name and description
- [ ] Specify inputs and outputs
- [ ] Create/link connection (if needed)
- [ ] Implement error handling
- [ ] Test with various inputs
- [ ] Document usage examples

### When Creating a Knowledge Base:
- [ ] Organize documents by topic
- [ ] Ensure content quality
- [ ] Configure search settings
- [ ] Test retrieval accuracy
- [ ] Monitor performance
- [ ] Plan update schedule

### When Creating a Flow:
- [ ] Map out process steps
- [ ] Identify decision points
- [ ] Add error handling
- [ ] Include human checkpoints
- [ ] Test all branches
- [ ] Document flow logic

---

## Summary

### Key Takeaways

1. **Agents are Orchestrators**: They coordinate tools, knowledge, flows, and collaborators
2. **Tools Extend Capabilities**: They connect agents to external systems and APIs
3. **Knowledge Provides Context**: RAG-based search enhances agent responses
4. **Flows Enable Complexity**: Multi-step processes with logic and control flow
5. **Connections Secure Access**: Centralized credential management
6. **Collaborators Enable Specialization**: Multi-agent architectures for complex domains

### Architecture Principles

1. **Separation of Concerns**: Each component has a specific role
2. **Modularity**: Components can be reused across agents
3. **Security**: Credentials managed separately from code
4. **Scalability**: Add capabilities without modifying core agent
5. **Testability**: Each component can be tested independently

---

## Additional Resources

- [Agent YAML Reference](./AGENT_YAML_REFERENCE.md)
- [watsonx Orchestrate Documentation](https://developer.watson-orchestrate.ibm.com/)
- [Building Agents Guide](https://developer.watson-orchestrate.ibm.com/agents/build_agent)
- [Creating Tools Guide](https://developer.watson-orchestrate.ibm.com/tools/create_tool)
- [Knowledge Bases Guide](https://developer.watson-orchestrate.ibm.com/knowledge_base/build_kb)
- [Agentic Workflows Guide](https://developer.watson-orchestrate.ibm.com/tools/flows/building_flow)

---

**Version:** 1.0  
**Last Updated:** 2026-03-25  
**Author:** watsonx Orchestrate Team

---

**Happy Building! 🚀**