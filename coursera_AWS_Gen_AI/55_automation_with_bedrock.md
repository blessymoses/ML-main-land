# Automation with Amazon Bedrock
In this reading, we delve into how Amazon Bedrock Data Automation (BDA) streamlines the extraction of structured insights from a wide range of unstructured content types including documents, images, videos, and audio. 

The reading introduces two key output modes: 
- standard extraction powered by Bedrock’s defaults and 
- customizable outputs defined through user-created blueprints. 

Core components like projects and blueprints enable tailored data processing pipelines, supporting both explicit and contextual inference. 

With use cases spanning content moderation, and media analysis, BDA empowers developers to build scalable automation workflows using advanced features like intelligent document splitting and semantic boundary detection.

## Core Purpose
Primary function: Extracts meaningful insights from unstructured content 
Supported input types: Documents, images, videos, and audio 
Output categories: Standard output and Custom output

## Output Types
### Standard Output:
Predefined extraction managed by Bedrock
Available for all content types
Configurable settings per content type
### Custom Output:
User-defined extraction rules
Available for documents and images only
Uses blueprints for extraction logic

## Key Components
### Projects
Definition: Collection of configuration settings
Features:
- Configurable standard output options
- Multiple blueprint support
- Document splitting capabilities
- Resource optimization settings

### Blueprints
Purpose: Instructions for custom data extraction
Types:
- Sample blueprints (pre-built)
- Custom blueprints (user-created)
Inference Types:
- Explicit: Direct extraction from document- 
- Implicit: Contextual value inference

### Use Cases
- RAG (Retrieval Augmented Generation) indexing 
- Document processing 
- Media analysis 
- Content classification 
- Content moderation

### Technical Implementation
API: invoke_data_automation_async
Required Parameters:
Input S3 location
Output S3 location
Project configuration
Blueprint(s)

### Advanced Features
Document Processing:
- Intelligent document splitting
- Semantic boundary detection
- Blueprint matching based on layout
Content Analysis:
- Image text recognition
- Logo detection
- Scene summarization
- Content moderation

### Practical Example
Use Case: AWS Certification Certificate Processing
Steps:
1. Create custom blueprint
2. Upload sample document
3. Define extraction rules
4. Configure output parameters
5. Process documents using the blueprint

