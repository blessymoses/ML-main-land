import boto3
import json

bedrock = boto3.client(service_name='bedrock-runtime')
bedrock_agent = boto3.client(service_name='bedrock-agent')

MODEL_ID = "amazon.nova-micro-v1:0"

temperature = .7

inference_config = {"temperature": temperature}

system_prompts = [{"text": "You are a virtual travel assistant that suggests destinations based on user preferences."
                + "Only return destination names and a brief description."}]

messages = []

message_1 = {
    "role": "user",
    "content": [{"text": "Create a list of 3 travel destinations."}]
}

messages.append(message_1)

response = bedrock.converse(
    modelId=MODEL_ID,
    messages=messages,
    system=system_prompts,
    inferenceConfig=inference_config
)

def print_response(response):
    model_response = response.get('output', {}).get('message', {}).get('content', [{}])[0].get('text', '')

    print("✈️ Your suggested travel destinations:")
    print(model_response)

print_response(response)

message_2 = {
        "role": "user",
        "content": [{"text": "Only suggest travel locations that are no more than one short flight away."}]
}

messages.append(message_2)

response = bedrock.converse(
    modelId=MODEL_ID,
    messages=messages,
    system=system_prompts,
    inferenceConfig=inference_config
)

print_response(response)

message_3 = {
        "role": "user",
        "content": [{"text": "INSERT YOUR PROMPT HERE"}]
}

messages.append(message_3)

response = bedrock.converse(
    modelId=MODEL_ID,
    messages=messages,
    system=system_prompts,
    inferenceConfig=inference_config
)

print_response(response)

# create a custom Bedrock prompt designed to evaluate trip planning requests like a travel agent would.

try:
    response = bedrock_agent.create_prompt(
        name="Travel-Agent-Prompt",
        description="Checks if all trip information has been provided.",
        variants=[
            { 
                "name": "Variant1",
                "modelId": MODEL_ID,
                "templateType": "CHAT",
                "inferenceConfiguration": {
                    "text": {
                        "temperature": 0.4
                    }
                },
                "templateConfiguration": { 
                    "chat": {
                        'system': [ 
                            {
                                "text": """You are a travel agent evaluating trip requests for custom itineraries. 
                                Review the message carefully and answer YES or NO to the following screening questions. 
                                Be strict—if any detail is missing or unclear, answer NO.

                                A) Is the destination clearly stated?
                                B) Are the travel dates within a reasonable range (not last−minute or over a year away)?
                                C) Does the request avoid high−risk or restricted activities (e.g., extreme sports, off−grid travel)?
                                D) Is there any mention of a valid passport or travel documentation?
                                E) Is there enough information to follow up with a proposed itinerary?"""
                            }
                        ],
                        'messages': [{
                            'role': 'user',
                            'content': [ 
                                {
                                    'text': "Trip request: {{event_request}}"
                                }
                            ]
                        }],
                        'inputVariables' : [
                            { 'name' : 'event_request'}
                        ]
                    }
                }
        }]
    )
    print("Created!")
    prompt_arn = response.get("arn")
except bedrock.exceptions.ConflictException as e:
    print("Already exists!")
    response = bedrock.list_prompts()
    prompt = next((prompt for prompt in response['promptSummaries'] if prompt['name'] == "TripBooker_xyz"), None)
    prompt_arn = prompt['arn']

prompt_arn

