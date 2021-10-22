# Amazon Lex V2
Amazon Lex enables you to add self-service, natural language chatbots to your applications or devices.

Lab: https://aws.amazon.com/getting-started/hands-on/create-banking-bot-on-amazon-lex-v2-console/?trk=gs_card
## Concepts
- `Intent`:
  - An intent represents an action that the user wants to perform.
  - Example: In *BankingBot*, *CheckBalance*, allowing your users to check the balance in their accounts, or *TransferFunds* for paying bills.
- `Utterance`:
  - An utterance is a phrase that is used to trigger your intent.
- `Slots`:
  - Slots are input data that a bot needs to complete an action or fulfill an intent.
  - This data is captured as slots, which is used to fulfill the intents.
  - 2 types of slot:
    - `Built-in slots`: These slots provide a definition of how the data is recognized and handled. 
      - For example, Amazon Lex has the built-in slot type for AMAZON.DATE, which recognizes words or phrases that represent a date and converts them into a standard date format (for example, "tomorrow," "the fifth of November," or "22 December").
    - `Custom slots`: These slots allow you to define and manage a custom catalog of items. You can define a custom slot by providing a list of values. Amazon Lex uses these values to train the natural language understanding model used for recognizing values for the slot. 
      - For example, you can define a slot type as accountType with values such as *Checking, Savings, and Credit*.
- `Prompts`:
  - Prompts and responses are bot messages that can be used to get information, acknowledge what the user said earlier, or confirm an action with the user before completing a transaction.
- `Fulfillment`: 
  - As part of fulfilling the user’s request, you can configure the bot to respond with a closing response. Optionally, you can enable code hooks such as AWS Lambda functions to run business logic.

# Amazon Textract
Amazon Textract is a fully managed machine learning service that automatically extracts text and data from scanned documents to identify, understand, and extract data from forms and tables.
## Extract text and structured data with Amazon Textract
Lab: https://aws.amazon.com/getting-started/hands-on/extract-text-with-amazon-textract/?trk=gs_card

# Amazon Rekognition
Amazon Rekognition is a deep learning-based image and video analysis service.
