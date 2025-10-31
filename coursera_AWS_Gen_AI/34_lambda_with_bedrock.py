# Setup Bedrock and Lambda
import boto3
import json

bedrock = boto3.client(service_name='bedrock-runtime')
lambda_client = boto3.client("lambda")
MODEL_ID = "amazon.nova-micro-v1:0"

# Define the calculation tool
math_tool = {
    "toolSpec": {
        "name": "calculateNumbers",
        "description": "Performs basic arithmetic operations",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "operation": {"type": "string"},
                    "num1": {"type": "number"},
                    "num2": {"type": "number"}
                },
                "required": ["operation", "num1", "num2"]
            }
        }
    }
}

# Function to trigger the Lambda calculation service
def execute_calculation(input_data):
    response = lambda_client.invoke(
        FunctionName="math-function",  
        InvocationType="RequestResponse",
        Payload=json.dumps(input_data)
    )
    response_payload = response["Payload"].read()
    calculation_result = json.loads(response_payload)
    response_body = calculation_result.get("body", "{}")
    return json.loads(response_body) if isinstance(response_body, str) else response_body

# User's initial message
user_input = {
    "role": "user",
    "content": [{"text": "Please subtract 60 from 100"}]
}

# Define system instructions
system_instructions = [
    {"text": """
    You are a virtual assistant capable of performing basic arithmetic operations: add, subtract, multiply, and divide.
    If the user doesn't specify an operation, ask them for more details.
    """}
]

# First interaction with the model
first_interaction = bedrock.converse(
    modelId=MODEL_ID,
    system=system_instructions,
    messages=[user_input],
    toolConfig={
        "tools": [math_tool],
        "toolChoice": {"auto": {}}
    },
    inferenceConfig={"temperature": 0.7}
)

# Process the assistant's response to check if tool is required
assistant_reply = first_interaction["output"]["message"]
message_parts = assistant_reply["content"]
tool_request_block = next((part for part in message_parts if "toolUse" in part), None)

if not tool_request_block:
    print("=== Assistant's Direct Response ===")
    print(message_parts[0]["text"])
else:
    tool_request = tool_request_block["toolUse"]
    tool_input_data = tool_request["input"]
    tool_id = tool_request["toolUseId"]
    print(tool_request_block)
    print(f"→ Assistant triggered tool: calculateNumbers with input: {tool_input_data}")

    # Execute the requested tool
    tool_result = execute_calculation(tool_input_data)
    print(f"← Lambda Function output: {tool_result}")

    # Create a response based on the tool's output
    try:
        result_summary = f"The outcome of the calculation is {tool_result['result']}."
    except Exception as e:
        result_summary = f"Oops! There was an error with the calculation. ({str(e)})"

    # Generate tool result message
    tool_response_msg = {
        "role": "user",
        "content": [
            {
                "toolResult": {
                    "toolUseId": tool_id,
                    "content": [{"text": result_summary}]
                }
            }
        ]
    }

    # Send tool result back to the model
    final_output = bedrock.converse(
        modelId=MODEL_ID,
        messages=[user_input, assistant_reply, tool_response_msg],
        toolConfig={  
            "tools": [math_tool],
            "toolChoice": {"auto": {}}
        },
        inferenceConfig={"temperature": 0.7}
    )

    # Display the final response from the assistant
    final_message = final_output["output"]["message"]["content"][0]["text"]
    print("\n=== Final Assistant Response ===")
    print(final_message)