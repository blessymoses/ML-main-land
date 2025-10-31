"""
Amazon Bedrock Knowledge Bases

How Knowledge Bases Works: The RAG Approach
Knowledge Bases uses a technique called Retrieval-Augmented Generation (RAG). Here's how it works:
1. Document Processing 
Upload your documents to Amazon S3
The system creates embeddings (numerical representations of text) using models like Amazon Titan Text Embeddings
Documents are chunked into manageable pieces
2. Vector Storage
Those embeddings get stored in a vector database (like Amazon OpenSearch Serverless)
This enables semantic searching - finding content based on meaning, not just keywords
3. Query Processing
When someone asks a question:
Their question gets converted to an embedding
The system finds similar vectors in the database based on semantic search
A foundation model generates a response using the retrieved content
Responses include citations back to source documents

Prompt Management allows you to:
Create and save prompts as reusable templates
Version control your prompts
Include variables (placeholders) in prompts
Manage prompts across different environments (development, staging, production)

Two main template types:
Chat Template: For conversational formats, includes system prompts and tool configurations
Text Template: For single text message prompts
You set the template type for the prompt by configuring the templateType parameter when you create the prompt. Valid values are TEXT or CHAT. CHAT is only compatible with models that support the Converse API. If you want to use prompt caching, you must use the CHAT template type.


"""
# to query KB
response = bedrock.retrieve_and_generate(        
     input={"text": "How do I restart the staging environment?"},        retrieveAndGenerateConfiguration={            
          "type": "KNOWLEDGE_BASE",            
          "knowledgeBaseConfiguration": {                
               "knowledgeBaseId": "<KNOWLEDGE_BASE_ID>",                 
                "modelArn": "<MODEL_ID>"            
             }
        }
    )

# prompt management
prompt_name = "hr_assistant_prompt_template"
template_text = '''
You are an HR assistant.

Write a professional, inclusive job description using the following inputs:

Job title: {{job_title}}
Responsibilities: {{responsibilities}}
Requirements: {{requirements}}
Location: {{location}}
Work type: {{work_type}}

- Start with a clear summary
- Use concise, inclusive language
- Keep it under 250 words
'''

response = bedrock_agent.create_prompt(
    name=prompt_name,
    description="Generates inclusive job descriptions from structured inputs",
    defaultVariant="v1",
    variants=[
        {
            "name": "v1",
            "modelId": <MODEL_ID>,
            "templateType": "TEXT",
            "templateConfiguration": {
                "text": {
                    "inputVariables": [
                        {"name": "job_title"},
                        {"name": "responsibilities"},
                        {"name": "requirements"},
                        {"name": "location"},
                        {"name": "work_type"}
                    ],
                    "text": template_text
                }
            },
            "inferenceConfiguration": {
                "text": {
                    "maxTokens": 500,
                    "temperature": 0.7,
                    "topP": 0.9,
                    "stopSequences": []
                }
            }
        }
    ]
)

variant_examples = [
    # First variant
    {
        "name": "detailed",
        "modelId": "<MODEL_ID>",
        "inferenceConfiguration": {
            "text" : {
              "temperature": 0.2,  # Lower temperature for more focused responses
              "topP": 0.9
            }
        }
    },
    # Second variant
    {
        "name": "summary",
        "modelId": "<MODEL_ID>",
        "inferenceConfiguration": {
            "text" : {
             "temperature": 0.7,  # Higher temperature for more focused responses
             "topP": 0.9
            }
        }
    }
]

# With Converse API
response = bedrock.converse(    
     modelId="<prompt_arn>",    
     promptVariables={        
          'request': {            
               'text': "<request_content_here>"
        }
    },
)

