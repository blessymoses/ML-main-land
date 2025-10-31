"""
Models to be enabled:
Amazon Nova Reel

asynchronous processing capabilities of Bedrock using the start_async_invoke API.
"""
import boto3
import json
import random
bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")
bedrock = boto3.client(service_name="bedrock", region_name="us-east-1")  
s3 = boto3.client("s3")
model_id = "amazon.nova-reel-v1:0"

prompt = "A person dancing on a mountain."

seed = random.randint(0, 2147483646)

model_input = {
    "taskType": "TEXT_VIDEO",
    "textToVideoParams": {"text": prompt},
    "videoGenerationConfig": {
        "fps": 24,
        "durationSeconds": 6,
        "dimension": "1280x720",
        "seed": seed,
    },
}

output_config = {
    "s3OutputDataConfig": {
        "s3Uri": "s3://<FILL IN BUCKET NAME HERE>/video/"
    }
}

response = bedrock_runtime.start_async_invoke(
    modelId=model_id,
    modelInput=model_input,
    outputDataConfig=output_config,
)

invocation_arn = response["invocationArn"]
print("✅ Job submitted!")
print("Invocation ARN:", invocation_arn)

# check status
job_status = bedrock_runtime.get_async_invoke(invocationArn=invocation_arn)
print("Current Status:", job_status["status"])