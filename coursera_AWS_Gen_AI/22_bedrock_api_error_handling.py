"""
"""
def safe_model_invoke(prompt, model_id):    

try:        

    response = bedrock_runtime.invoke_model(            

          modelId=model_id,            

          body=json.dumps({                

               "inputText": prompt,                

               "textGenerationConfig": {                    

                    "maxTokenCount": 512,                    

                    "temperature": 0.7                

                }            

          })        

     )        

     return json.loads(response['body'].read())    

except bedrock_runtime.exceptions.ValidationException:        

     print("Invalid request parameters")    

except bedrock_runtime.exceptions.ModelTimeoutException:        

     print("Model inference timed out")    

except Exception as e:        

     print(f"Unexpected error: {str(e)}")