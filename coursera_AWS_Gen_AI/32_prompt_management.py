import boto3
import json
import datetime
from IPython.display import display, JSON

bedrock_agent = boto3.client("bedrock-agent")
bedrock_runtime = boto3.client("bedrock-runtime")
bedrock_agent_runtime = boto3.client("bedrock-agent-runtime")

model_id = "amazon.nova-micro-v1:0"

# create_prompt API
prompt_name = f"job-description-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

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
            "modelId": model_id,
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
print("\n==================== Response Object ====================\n")
display(JSON(response))

print("\n==================== Prompt ARN ====================\n")
print(response['arn'])

# create_prompt_version API
response = bedrock_agent.create_prompt_version(
    description='Initial prompt for creating job description documents.',
    promptIdentifier="<FILL_ME_IN>"
)

print("\n==================== PROMPT VERSION ARN ====================\n")
print(response["arn"])

# Invoke a Model Using the Versioned Prompt Template
prompt_arn_with_version = "<FILL_ME_IN>"

response = bedrock_runtime.converse(
    modelId=prompt_arn_with_version,
    promptVariables={
        "job_title": {"text": "UX Designer"},
        "responsibilities": {"text": "Design user interfaces, run usability testing, collaborate with product teams"},
        "requirements": {"text": "3+ years experience, Figma, HTML/CSS knowledge, communication skills"},
        "location": {"text": "New York or remote"},
        "work_type": {"text": "Full-time"}
    }
)

print("\n==================== Response Text ====================\n")
print(response['output']['message']['content'][0]['text'])

# optimize_prompt API
def handle_response_stream(response):
    try:
        event_stream = response['optimizedPrompt']
        for event in event_stream:
            if 'optimizedPromptEvent' in event:
                print("\n==================== OPTIMIZED PROMPT ====================\n")
                print(event['optimizedPromptEvent']['optimizedPrompt']['textPrompt']['text'])
    except Exception as e:
        raise e


prompt_input = {
    "textPrompt": {
        "text": template_text
    }
}

response = bedrock_agent_runtime.optimize_prompt(
            input=prompt_input,
            targetModelId=model_id
        )

print("\n==================== ORIGINAL PROMPT ====================\n")
print(template_text)
handle_response_stream(response)

# update the prompt based on the output from the optimization step and create a new version
prompt_identifier = "<FILL_ME_IN_1>"

existing_prompt = bedrock_agent.get_prompt(promptIdentifier=prompt_identifier)
print("\n==================== ORIGINAL PROMPT ====================\n")
print(existing_prompt["variants"][0]["templateConfiguration"]["text"]["text"])


updated_variants = existing_prompt["variants"]
for variant in updated_variants:
    if variant["templateType"] == "TEXT":
        variant["templateConfiguration"]["text"]["text"] = "<FILL_ME_IN_2>"


response = bedrock_agent.update_prompt(
    promptIdentifier=prompt_identifier,
    name=existing_prompt["name"],
    description=existing_prompt["description"],
    defaultVariant=existing_prompt["defaultVariant"],
    variants=updated_variants
)

print("\n==================== UPDATED PROMPT ====================\n")

updated_prompt = bedrock_agent.get_prompt(promptIdentifier=prompt_identifier)
print(updated_prompt["variants"][0]["templateConfiguration"]["text"]["text"])

response = bedrock_agent.create_prompt_version(
    description='Optimized prompt for creating job description documents.',
    promptIdentifier=prompt_identifier
)

print("\n==================== PROMPT VERSION ARN ====================\n")
print(response["arn"])

# Compare Versions
prompt_arn = "<FILL_ME_IN>"

response = bedrock_runtime.converse(
    modelId=prompt_arn,
    promptVariables={
        "job_title": {"text": "UX Designer"},
        "responsibilities": {"text": "Design user interfaces, run usability testing, collaborate with product teams"},
        "requirements": {"text": "3+ years experience, Figma, HTML/CSS knowledge, communication skills"},
        "location": {"text": "New York or remote"},
        "work_type": {"text": "Full-time"}
    }
)

print("\\n==================== Response Text ====================\\n")
print(response['output']['message']['content'][0]['text'])

prompt_arn = "<FILL_ME_IN>"

response = bedrock_runtime.converse(
    modelId=prompt_arn,
    promptVariables={
        "job_title": {"text": "UX Designer"},
        "responsibilities": {"text": "Design user interfaces, run usability testing, collaborate with product teams"},
        "requirements": {"text": "3+ years experience, Figma, HTML/CSS knowledge, communication skills"},
        "location": {"text": "New York or remote"},
        "work_type": {"text": "Full-time"}
    }
)

print("\\n==================== Response Text ====================\\n")
print(response['output']['message']['content'][0]['text'])

# cleanup
response = bedrock_agent.list_prompts()

for prompt in response['promptSummaries']:
    prompt_id = prompt['id']  # The correct key is 'id', not 'promptId'
    print(f"Deleting prompt: {prompt['name']} (ID: {prompt_id})")
    bedrock_agent.delete_prompt(promptIdentifier=prompt_id)

print("All prompts deleted successfully")