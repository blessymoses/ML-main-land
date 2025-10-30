"""
The InvokeModel API is a low-level API for Amazon Bedrock. There are higher level APIs as well, like the Converse API.
"""

import boto3

import json

# Initialize Bedrock client

bedrock_runtime = boto3.client("bedrock-runtime")

model_id_titan = "amazon.titan-text-premier-v1:0"

# Text generation example


def generate_text():

    payload = {
        "inputText": "Explain quantum computing in simple terms.",
        "textGenerationConfig": {"maxTokenCount": 500, "temperature": 0.5, "topP": 0.9},
    }
    response = bedrock_runtime.invoke_model(
        modelId=model_id_titan, body=json.dumps(payload)
    )
    return json.loads(response["body"].read())


generate_text()
