# Nedrock Agents

## Key components and capabilities
### Foundation Model integration
At the heart of every Bedrock Agent is a foundation model that powers its understanding and decision-making capabilities. When creating an agent, you'll:
- Select from AWS's collection of foundation models available through Amazon Bedrock
- Configure the model to align with your use case through system prompt configuration
- Let the agent use this model to process user inputs, determine when tools are needed, and orchestrate responses
### Agent instructions
Think of agent instructions as your agent's mission statement and operating manual combined. These instructions define the boundaries and personality of your agent, guiding its interactions and decision-making processes.
### Code interpretation
Code interpretation allows agents to generate and execute code in a secure sandbox environment, enabling:
Real-time data analysis
Complex calculations
Format conversions
Data visualization
Custom data processing workflows
### Interactive user inputs
The interactive nature of Bedrock Agents is demonstrated through its sophisticated conversation management. During interactions, agents can:
Request specific information when needed
Validate user inputs
Maintain context throughout the interaction
Guide users through multi-step processes
### Action groups
Action groups serve as your agent's toolkit for executing tasks. These action groups can include Lambda functions, API integrations, and custom tools. Agents can also connect to knowledge bases to access sources like:
Company policies
Product documentation
Technical guides
FAQs
Historical data
### Memory
Bedrock Agents can maintain conversation context through its memory capabilities. Memory enables agents to:
Retain context across multiple user sessions
Recall and reference past interactions
Store summarized conversations using the foundation model
Configure retention periods by:
Number of days
Number of sessions
Access relevant historical information when needed
### Knowledge Base Integration
Bedrock Agents can be associated with one or more knowledge bases to enhance their responses. This integration:
Enables Retrieval Augmented Generation (RAG)
Allows agents to access domain-specific information such as:
Corporate policies
Technical documentation
Product information
Training materials
Augments LLM responses with verified information
Provides real-time access to updated company knowledge
Helps ensure accurate and consistent responses
### Orchestration
Bedrock Agents use orchestration prompts to manage complex tasks and interactions. The orchestration process:
Combines multiple components to build comprehensive responses:
Agent instructions
Action group definitions
Knowledge base content
Uses system instructions alongside user chat interactions
Comes with default prompt templates for common scenarios
Allows customization through advanced prompts for specific needs
Manages the flow of:
User requests
Model interactions
Function calls
Data retrieval
### Mult-agent collaboration
Bedrock Agents can work together as collaborators to handle complex workflows. This collaboration enables:
Association of multiple specialized agents
Reuse of existing agent capabilities, such as:
Flight booking agents
Calendar management agents
Data processing agents
Orchestration of responses across multiple agents
Division of complex tasks into specialized functions
Seamless handoff between different agent capabilities
Maintenance of context across agent interactions
