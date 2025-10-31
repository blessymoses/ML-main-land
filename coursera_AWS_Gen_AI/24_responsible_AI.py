"""
Key Components of Guardrails
Input Protection:
Filters harmful user inputs before reaching the model
Prevents prompt injection attempts
Blocks denied topics and custom phrases
Output Safety:
Screens model responses for harmful content
Masks or blocks sensitive information
Ensures responses meet quality thresholds
"""
import boto3

client = boto3.client('bedrock')

create_response = client.create_guardrail(    

   name='fiduciary-advice',    

   description='Prevents the our model from providing fiduciary advice.',    

   topicPolicyConfig={        

      'topicsConfig': [            

         {                

          'name': 'Fiduciary Advice',                

          'definition': 'Providing personalized advice or recommendations on managing financial assets, investments, or                                 trusts in a fiduciary capacity or assuming related                                 obligations and liabilities.',                

           'examples': [                    

              'What stocks should I invest in for my retirement?',                    

              'Is it a good idea to put my money in a mutual fund?',                    

              'How should I allocate my 401(k) investments?',                    

              'What type of trust fund should I set up for my children?',                    

              'Should I hire a financial advisor to manage my investments?'                

           ],                

           'type': 'DENY'            

        }        

     ]    

   },    

   contentPolicyConfig={        

      'filtersConfig': [            

          {                

          'type': 'SEXUAL',                

          'inputStrength': 'HIGH',                

          'outputStrength': 'HIGH'            

     },            

     {                

          'type': 'VIOLENCE',                

          'inputStrength': 'HIGH',                

          'outputStrength': 'HIGH'            

     },            

     {                

          'type': 'HATE',                

          'inputStrength': 'HIGH',                

          'outputStrength': 'HIGH'            

     },            

     {                

          'type': 'INSULTS',                

          'inputStrength': 'HIGH',                         

          'outputStrength': 'HIGH'            

     },            

     {                

          'type': 'MISCONDUCT',                

          'inputStrength': 'HIGH',                

          'outputStrength': 'HIGH'            

     },            

     {                

          'type': 'PROMPT_ATTACK',                

          'inputStrength': 'HIGH',                

          'outputStrength': 'NONE'            

      }        

   ]    

},    

wordPolicyConfig={        

    'wordsConfig': [            

          {'text': 'fiduciary advice'},            

          {'text': 'investment recommendations'},            

          {'text': 'stock picks'},            

          {'text': 'financial planning guidance'},            

          {'text': 'portfolio allocation advice'},            

          {'text': 'retirement fund suggestions'},            

          {'text': 'wealth management tips'},            

          {'text': 'trust fund setup'},            

          {'text': 'investment strategy'},            

          {'text': 'financial advisor recommendations'}            

     ],        

     'managedWordListsConfig': [            

          {'type': 'PROFANITY'}        

     ]    

},    

 sensitiveInformationPolicyConfig={        

     'piiEntitiesConfig': [            

          {'type': 'EMAIL', 'action': 'ANONYMIZE'},            

          {'type': 'PHONE', 'action': 'ANONYMIZE'},            

          {'type': 'NAME', 'action': 'ANONYMIZE'},            

          {'type': 'US_SOCIAL_SECURITY_NUMBER', 'action': 'BLOCK'},            

          {'type': 'US_BANK_ACCOUNT_NUMBER', 'action': 'BLOCK'},            

          {'type': 'CREDIT_DEBIT_CARD_NUMBER', 'action': 'BLOCK'}        

     ],        

     'regexesConfig': [            

        {                

          'name': 'Account Number',                

          'description': 'Matches account numbers in the format XXXXXX1234',                

          'pattern': r'\b\d{6}\d{4}\b',                

          'action': 'ANONYMIZE'            

        }        

    ]    

  },    

  contextualGroundingPolicyConfig={        

     'filtersConfig': [            

         {                

          'type': 'GROUNDING',                

          'threshold': 0.75            

     },            

     {                

          'type': 'RELEVANCE',                

          'threshold': 0.75            

          }        

     ]    

  },    

   blockedInputMessaging="""I can provide general info about Acme Financial's products and services, but can't fully address your request here. For personalized help or detailed questions, please contact our customer service team directly. For security reasons, avoid sharing sensitive information through this channel. If you have a general product question, feel free to ask without including personal details. """,    

   blockedOutputsMessaging="""I can provide general info about Acme Financial's products and services, but can't fully address your request here. For personalized help or detailed questions, please contact our customer service team directly. For security reasons, avoid sharing sensitive information through this channel. If you have a general product question, feel free to ask without including personal details. """,    

    tags=[        

      {'key': 'purpose', 'value': 'fiduciary-advice-prevention'},        

      {'key': 'environment', 'value': 'production'}    

   ]

)

print(create_response)