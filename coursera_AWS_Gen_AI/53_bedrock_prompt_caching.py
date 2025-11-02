"""
Why does the cached response use less tokens even with a new request? Using cache_point = {"cachePoint": {"type": "default"}} with Bedrock on a new request can still use fewer tokens because the system leverages pre-cached computations and optimizations. Even for new requests, parts of the model's processing might be reused from the cache, reducing the need for fresh token computation. This caching strategy helps minimize redundant processing, leading to lower token usage and cost. Essentially, Bedrock efficiently reuses cached intermediate results, even on the first request.
"""
import boto3
 import json
 from datetime import datetime

 bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')  

 MODEL_ID = "amazon.nova-micro-v1:0"

system_prompt = """
 You are an assistant that summarizes music reviews for a record company.
 Here are examples:

 Review: The latest album by The New Wave Band is a masterpiece! Every track is a hit.
 Summary: Reviewer praises the latest album as a masterpiece with hit tracks.

 Review: I was disappointed with the new single; it lacked the energy of their previous work.
 Summary: Reviewer expresses disappointment, noting a lack of energy compared to previous work.
 """

 user_input_review = "This EP is a solid effort with a few standout songs, though some tracks feel repetitive."

# no caching
no_cache_payload = {
     "system": [
         {"text": system_prompt}
     ],
     "messages": [
         {
             "role": "user",
             "content": [
                 {"text": user_input_review + "\nSummary:"}
             ]
         }
     ]
 }

 no_cache_response = bedrock.converse(
     modelId=MODEL_ID,
     system=no_cache_payload["system"],
     messages=no_cache_payload["messages"]
 )

 no_cache_output = no_cache_response['output']['message']['content'][0]['text']
 no_cache_input_tokens = no_cache_response['usage']['inputTokens']
 no_cache_output_tokens = no_cache_response['usage']['outputTokens']
 no_cache_tokens = no_cache_input_tokens + no_cache_output_tokens

 print("[No Caching] Generated Summary:")
 print(no_cache_output)
 print(f"Total Tokens Used (No Cache): {no_cache_tokens}")

# with caching
cache_point = {"cachePoint": {"type": "default"}}

 payload_with_caching = {
     "system": [
         {"text": system_prompt},
         cache_point
     ],
     "messages": [
         {
             "role": "user",
             "content": [
                 {"text": user_input_review + "\nSummary:"}
             ]
         }
     ]
 }

 response = bedrock.converse(
     modelId=MODEL_ID,
     system=payload_with_caching["system"],
     messages=payload_with_caching["messages"]
 )

 cache_output = response['output']['message']['content'][0]['text']
 cache_input_tokens = response['usage']['inputTokens']
 cache_output_tokens = response['usage']['outputTokens']
 cache_tokens = cache_input_tokens + cache_output_tokens

 print("[With Caching] Generated Summary:")
 print(cache_output)
 print(f"Total Tokens Used: {cache_tokens}")

# modify your Bedrock instructions to observe how caching behaves when you change your original request
system_prompt = """
 You are a pet expert that will tell the user what type of pet they have based on a description. You'll keep your responses short and generalized.
 Here are examples:

 Description: My pet barks and has four legs.
 Summary: Your pet is a dog.

 Review: My pet meows and uses a litter box.
 Summary: Your pet is a cat.
 """

 user_input_review = "My pet sings and has wings."

