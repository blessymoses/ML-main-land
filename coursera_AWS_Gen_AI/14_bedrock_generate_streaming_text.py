"""
Using Amazon Bedrock for streaming text generation
Amazon Bedrock can generate and transform text using the InvokeModelWithResponseStream API call.

What each API does

InvokeModel
	•	Endpoint: POST /model/{modelId}/invoke
	•	Returns the full generated response once the model has finished processing.
	•	The body of the response contains the model output (text, image, embeddings) under body.
	•	Simpler to implement for typical use-cases.
    Purpose: Synchronous model invocation for immediate responses
Key Features:
Single request-response pattern
Direct model interaction
Suitable for real-time applications
Best for:
Chatbots
Interactive applications
Real-time content generation

InvokeModelWithResponseStream
	•	Endpoint: POST /model/{modelId}/invoke-with-response-stream
	•	Returns a streaming response, i.e., the model output is sent in chunks/tokens as they are generated.
	•	You must check if the chosen model supports streaming — via GetFoundationModel.responseStreamingSupported field.
	•	Requires permission: bedrock:InvokeModelWithResponseStream.
    urpose: Streaming responses for better user experience
Benefits:
Real-time text generation
Improved interactivity
Ideal for chatbots and interactice applications
Best for:
Interactive chat applications
Real-time content generation
User-facing applications 
Live text generation displays

When to use each

Use InvokeModel when:
	•	You dont need to display the output token-by-token (streaming) — just get the result in one go.
	•	Your use-case is “batch” style: send a prompt, get full answer, process it.
	•	Latency and interactive experience are less critical.
	•	Simpler code and no streaming subscription required.

Use InvokeModelWithResponseStream when:
	•	You want interactive user experiences: e.g., chat UI showing replies as they are generated (type-writer effect).
	•	You want lower time to first token (i.e., user sees something quicker) especially for long responses.
	•	You need to process tokens as they come (for example, to abort mid-stream, start parallel work, or implement incremental display).
	•	The selected model declares streaming support.
	•	Youre comfortable handling a streamed event-based response (rather than a simple single JSON).

Scenario
Ideal API
Short prompt → short answer, just process result
InvokeModel
Long-form generation, chat UI, want to display answer as it is generated
InvokeModelWithResponseStream
Model or use-case doesn’t support streaming
InvokeModel
Need simple code path and don’t need partial results
InvokeModel

"""
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
model_id = 'amazon.nova-micro-v1:0'

payload = {
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "text": "Tell me what type of dances people do."
                }
            ]
        }
    ]
}

payload_json = json.dumps(payload)

response = bedrock.invoke_model_with_response_stream(
    modelId=model_id,
    body=payload_json,
    contentType='application/json',
    accept='application/json'
)

stream = response['body']
full_text = ""

print("Receiving response stream:")
for event in stream:
    chunk = event['chunk']
    chunk_str = chunk.get('bytes', b'').decode('utf-8')

    try:
        json_chunk = json.loads(chunk_str)

        if "contentBlockDelta" in json_chunk:
            delta = json_chunk["contentBlockDelta"]["delta"]
            text = delta.get("text", "")
            full_text += text
            print(text, end='') 

    except json.JSONDecodeError:
        continue