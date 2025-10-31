import boto3
import json

bedrock = boto3.client(service_name='bedrock-runtime')
lambda_client = boto3.client("lambda")

MODEL_ID_CLAUDE_SONNET = "anthropic.claude-3-sonnet-20240229-v1:0"

# Define toolSpec for lambda function
# Lambda function named getWeather already created
weather_tool = {
    "toolSpec": {
        "name": "getWeather",
        "description": "Gets the current weather using latitude and longitude.",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "lat": {"type": "number"},
                    "lon": {"type": "number"}
                },
                "required": ["lat", "lon"]
            }
        }
    }
}

# Invoke Lambda Function (tool)
def invoke_weather_lambda(input_data):
    response = lambda_client.invoke(
        FunctionName="weather-tool",
          InvocationType="RequestResponse",
        Payload=json.dumps(input_data)
    )
    payload = response["Payload"].read()
    result = json.loads(payload)
    body = result.get("body", "{}")
    return json.loads(body) if isinstance(body, str) else body

initial_user_msg = {
    "role": "user",
    "content": [{"text": "What's the weather like in portland?"}]
}

system_prompt = [
    {"text": """
    You are a helpful assistant that can check the weather using tools when needed.
     If the user inputs a city name that exists in multiple geogrpahic areas, ask the user for clarification.
    """}]

# Ask model initial question
initial_response = bedrock.converse(
    modelId=MODEL_ID_CLAUDE_SONNET,
    system=system_prompt,
    messages=[initial_user_msg],
    toolConfig={
        "tools": [weather_tool],
        "toolChoice": {"auto": {}}
    },
    inferenceConfig={"temperature": 0.7}
)

# Parse response from Claude to determine if tool is needed
assistant_msg = initial_response["output"]["message"]
content_blocks = assistant_msg["content"]
tool_use_block = next((block for block in content_blocks if "toolUse" in block), None)

if not tool_use_block:
    print("=== Claude Response ===")
    print(content_blocks[0]["text"])
else:
    tool_use = tool_use_block["toolUse"]
    tool_input = tool_use["input"]
    tool_use_id = tool_use["toolUseId"]
    print(tool_use_block)
    print(f"→ Claude requested tool: getWeather with input: {tool_input}")

    # Invoke tool
    tool_output = invoke_weather_lambda(tool_input)
    print(f"← Lambda returned: {tool_output}")

    # Print out tool output
    try:
        summary = f"The weather in {tool_output['location']} is currently {tool_output['temperature']} with {tool_output['condition']}."
    except Exception as e:
        summary = f"Sorry, I couldn't retrieve the weather. ({str(e)})"

    # Construct tool result message
    tool_result_msg = {
        "role": "user",
        "content": [
            {
                "toolResult": {
                    "toolUseId": tool_use_id,
                    "content": [{"text": summary}]
                }
            }
        ]
    }

    # Pass tool result message to model
    final_response = bedrock.converse(
        modelId=MODEL_ID_CLAUDE_SONNET,
        messages=[initial_user_msg, assistant_msg, tool_result_msg],
        toolConfig={
              "tools": [weather_tool],
            "toolChoice": {"auto": {}}
        },
        inferenceConfig={"temperature": 0.7}
    )

    # Print final response
    final_msg = final_response["output"]["message"]["content"][0]["text"]
    print("\n=== Final Agent Response ===")
    print(final_msg)