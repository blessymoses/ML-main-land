import boto3
import json
import time
import zipfile
from io import BytesIO
import uuid
import pprint
import logging
print(boto3.__version__)

logging.basicConfig(format='[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

sts_client = boto3.client('sts')
iam_client = boto3.client('iam')
lambda_client = boto3.client('lambda')
bedrock_agent_client = boto3.client('bedrock-agent')
bedrock_agent_runtime_client = boto3.client('bedrock-agent-runtime')

session = boto3.session.Session()
region = session.region_name
account_id = sts_client.get_caller_identity()["Account"]
region, account_id

inference_profile = "us.amazon.nova-micro-v1:0" foundation_model = inference_profile[3:]
foundation_model

suffix = f"{region}-{account_id}"
agent_name = "hr-assistant-function-def"
agent_bedrock_allow_policy_name = f"{agent_name}-ba-{suffix}"
agent_role_name = f'AmazonBedrockExecutionRoleForAgents_{agent_name}'
agent_description = "Agent for providing HR assistance to manage vacation time"
agent_instruction = "You are an HR agent, helping employees understand HR policies and manage vacation time"
agent_action_group_name = "VacationsActionGroup"
agent_action_group_description = "Actions for getting the number of available vacations days for an employee and confirm new time off"
agent_alias_name = f"{agent_name}-alias"
lambda_function_role = f'{agent_name}-lambda-role-{suffix}'
lambda_function_name = f'{agent_name}-{suffix}'

#  Create an employee database using SQLite and populate it with sample HR data
# creating employee database to be used by lambda function
import sqlite3
import random
from datetime import date, timedelta

# Connect to the SQLite database (creates a new one if it doesn't exist)
conn = sqlite3.connect('employee_database.db')
c = conn.cursor()

# Create the employees table
c.execute('''CREATE TABLE IF NOT EXISTS employees
                (employee_id INTEGER PRIMARY KEY AUTOINCREMENT, employee_name TEXT, employee_job_title TEXT, employee_start_date TEXT, employee_employment_status TEXT)''')

# Create the vacations table
c.execute('''CREATE TABLE IF NOT EXISTS vacations
                (employee_id INTEGER, year INTEGER, employee_total_vacation_days INTEGER, employee_vacation_days_taken INTEGER, employee_vacation_days_available INTEGER, FOREIGN KEY(employee_id) REFERENCES employees(employee_id))''')

# Create the planned_vacations table
c.execute('''CREATE TABLE IF NOT EXISTS planned_vacations
                (employee_id INTEGER, vacation_start_date TEXT, vacation_end_date TEXT, vacation_days_taken INTEGER, FOREIGN KEY(employee_id) REFERENCES employees(employee_id))''')

# Generate some random data for 10 employees
employee_names = ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Williams', 'Tom Brown', 'Emily Davis', 'Michael Wilson', 'Sarah Taylor', 'David Anderson', 'Jessica Thompson']
job_titles = ['Manager', 'Developer', 'Designer', 'Analyst', 'Accountant', 'Sales Representative']
employment_statuses = ['Active', 'Inactive']

for i in range(10):
    name = employee_names[i]
    job_title = random.choice(job_titles)
    start_date = date(2015 + random.randint(0, 7), random.randint(1, 12), random.randint(1, 28)).strftime('%Y−%m−%d')
    employment_status = random.choice(employment_statuses)
    c.execute("INSERT INTO employees (employee_name, employee_job_title, employee_start_date, employee_employment_status) VALUES (?, ?, ?, ?)", (name, job_title, start_date, employment_status))
    employee_id = c.lastrowid

    # Generate vacation data for the current employee
    for year in range(date.today().year, date.today().year − 3, −1):
        total_vacation_days = random.randint(10, 30)
        days_taken = random.randint(0, total_vacation_days)
        days_available = total_vacation_days − days_taken
        c.execute("INSERT INTO vacations (employee_id, year, employee_total_vacation_days, employee_vacation_days_taken, employee_vacation_days_available) VALUES (?, ?, ?, ?, ?)", (employee_id, year, total_vacation_days, days_taken, days_available))

        # Generate some planned vacations for the current employee and year
        num_planned_vacations = random.randint(0, 3)
        for _ in range(num_planned_vacations):
            start_date = date(year, random.randint(1, 12), random.randint(1, 28)).strftime('%Y−%m−%d')
            end_date = (date(int(start_date[:4]), int(start_date[5:7]), int(start_date[8:])) + timedelta(days=random.randint(1, 14))).strftime('%Y−%m−%d')
            days_taken = (date(int(end_date[:4]), int(end_date[5:7]), int(end_date[8:])) − date(int(start_date[:4]), int(start_date[5:7]), int(start_date[8:])))
            c.execute("INSERT INTO planned_vacations (employee_id, vacation_start_date, vacation_end_date, vacation_days_taken) VALUES (?, ?, ?, ?)", (employee_id, start_date, end_date, days_taken.days))

# Commit the changes and close the connection
conn.commit()
conn.close()

# ✅ Write a Lambda function that can query and update this data
import os
import json
import shutil
import sqlite3
from datetime import datetime


def get_available_vacations_days(employee_id):
    conn = sqlite3.connect('/tmp/employee_database.db')
    c = conn.cursor()

    if employee_id:
        c.execute("""
            SELECT employee_vacation_days_available
            FROM vacations
            WHERE employee_id = ?
            ORDER BY year DESC
            LIMIT 1
        """, (employee_id,))

        available_vacation_days = c.fetchone()

        if available_vacation_days:
            available_vacation_days = available_vacation_days[0]
            conn.close()
            return available_vacation_days
        else:
            conn.close()
            return f"No vacation data found for employed_id {employee_id}"
    else:
        conn.close()
        raise Exception("No employee id provided")

# ✅ Provision an IAM role that grants Lambda the permissions it needs

try:
    assume_role_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }

    assume_role_policy_document_json = json.dumps(assume_role_policy_document)

    lambda_iam_role = iam_client.create_role(
        RoleName=lambda_function_role,
        AssumeRolePolicyDocument=assume_role_policy_document_json
    )

    # Pause to make sure role is created
    time.sleep(10)
except:
    lambda_iam_role = iam_client.get_role(RoleName=lambda_function_role)

iam_client.attach_role_policy(
    RoleName=lambda_function_role,
    PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
)

# ✅ Deploy the Lambda function so it can be used by your Bedrock Agent
# Package the Lambda function to a Zip file and create the Lambda function using boto3. 
s = BytesIO()
z = zipfile.ZipFile(s, 'w')
z.write("lambda_function.py")
z.write("employee_database.db")
z.close()
zip_content = s.getvalue()

# Create Lambda Function
lambda_function = lambda_client.create_function(
    FunctionName=lambda_function_name,
    Runtime='python3.12',
    Timeout=180,
    Role=lambda_iam_role['Role']['Arn'],
    Code={'ZipFile': zip_content},
    Handler='lambda_function.lambda_handler'
)

# create the IAM policy that the agent will need to use the inference profile and invoke the model. 
bedrock_agent_bedrock_allow_policy_statement = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AmazonBedrockAgentBedrockFoundationModelPolicy",
            "Effect": "Allow",
            "Action": "bedrock:InvokeModel",
            "Resource": [
                f"arn:aws:bedrock:*::foundation-model/{foundation_model}",
                f"arn:aws:bedrock:*:*:inference-profile/{inference_profile}"
            ]
        },
        {
            "Sid": "AmazonBedrockAgentBedrockGetInferenceProfile",
            "Effect": "Allow",
            "Action":  [
                "bedrock:GetInferenceProfile",
                "bedrock:ListInferenceProfiles",
                "bedrock:UseInferenceProfile"
            ],
            "Resource": [
                f"arn:aws:bedrock:*:*:inference-profile/{inference_profile}"
            ]
        }
    ]
}

bedrock_policy_json = json.dumps(bedrock_agent_bedrock_allow_policy_statement)

agent_bedrock_policy = iam_client.create_policy(
    PolicyName=agent_bedrock_allow_policy_name,
    PolicyDocument=bedrock_policy_json
)

# create the IAM role that the agent will need to assume to perform its duties
assume_role_policy_document = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {
            "Service": "bedrock.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
    }]
}

assume_role_policy_document_json = json.dumps(assume_role_policy_document)
agent_role = iam_client.create_role(
    RoleName=agent_role_name,
    AssumeRolePolicyDocument=assume_role_policy_document_json
)

# Pause to make sure role is created
time.sleep(10)

iam_client.attach_role_policy(
    RoleName=agent_role_name,
    PolicyArn=agent_bedrock_policy['Policy']['Arn']
)

# use the Bedrock Agent client to create a new agent - create_agent API
response = bedrock_agent_client.create_agent(
    agentName=agent_name,
    agentResourceRoleArn=agent_role['Role']['Arn'],
    description=agent_description,
    idleSessionTTLInSeconds=1800,
    foundationModel=inference_profile,
    instruction=agent_instruction,
)
agent_id = response['agent']['agentId']
agent_id, response

# Create Agent Action Group - create_agent_action_group API
agent_functions = [
    {
        'name': 'get_available_vacations_days',
        'description': 'get the number of vacations available for a certain employee',
        'parameters': {
            "employee_id": {
                "description": "the id of the employee to get the available vacations",
                "required": True,
                "type": "integer"
            }
        }
    },
    {
        'name': 'reserve_vacation_time',
        'description': 'reserve vacation time for a specific employee - you need all parameters to reserve vacation time',
        'parameters': {
            "employee_id": {
                "description": "the id of the employee for which time off will be reserved",
                "required": True,
                "type": "integer"
            },
            "start_date": {
                "description": "the start date for the vacation time",
                "required": True,
                "type": "string"
            },
            "end_date": {
                "description": "the end date for the vacation time",
                "required": True,
                "type": "string"
            }
        }
    },
]

# Now, we can configure and create an action group here:
agent_action_group_response = bedrock_agent_client.create_agent_action_group(
    agentId=agent_id,
    agentVersion='DRAFT',
    actionGroupExecutor={
        'lambda': lambda_function['FunctionArn']
    },
    actionGroupName=agent_action_group_name,
    functionSchema={
        'functions': agent_functions
    },
    description=agent_action_group_description
)

agent_action_group_response

# Modify the resource policy on the AWS Lambda function to allow the specific bedrock agent to invoke it. 
response = lambda_client.add_permission(
    FunctionName=lambda_function_name,
    StatementId='allow_bedrock',
    Action='lambda:InvokeFunction',
    Principal='bedrock.amazonaws.com',
    SourceArn=f"arn:aws:bedrock:{region}:{account_id}:agent/{agent_id}",
)

# Prepare the Agent and Create an Agent Alias - prepare_agent API creates a DRAFT version of the agent that can be used for internal testing.

response = bedrock_agent_client.prepare_agent(
    agentId=agent_id
)
response

response = bedrock_agent_client.create_agent_alias(
    agentAliasName='test-alias-1',
    agentId="<FILL_ME_IN>"
)

response

# use the bedrock-agent-runtime client and the invoke_agent API to invoke this agent and perform some tasks.
## create a random id for session initiator id
session_id:str = str(uuid.uuid1())
enable_trace:bool = False
end_session:bool = False

# invoke the agent API
agentResponse = bedrock_agent_runtime_client.invoke_agent(
    inputText="How much vacation does the employee with employee_id set to 1 have available?",
    agentId=agent_id,
    agentAliasId=agent_alias_id, 
    sessionId=session_id,
    enableTrace=enable_trace, 
    endSession= end_session
)

logger.info(pprint.pprint(agentResponse))

event_stream = agentResponse['completion']
try:
    for event in event_stream:        
        if 'chunk' in event:
            data = event['chunk']['bytes']
            logger.info(f"Final answer ->\n{data.decode('utf8')}")
            agent_answer = data.decode('utf8')
            end_event_received = True
        elif 'trace' in event:
            logger.info(json.dumps(event['trace'], indent=2))
        else:
            raise Exception("unexpected event.", event)
except Exception as e:
    raise Exception("unexpected event.", e)

agentResponse = bedrock_agent_runtime_client.invoke_agent(
    inputText="Great. please reserve one day of time off for the employee with employee_id set to 1 for <FILL_ME_IN>",
    agentId=agent_id,
    agentAliasId=agent_alias_id, 
    sessionId=session_id,
    enableTrace=enable_trace, 
    endSession= end_session
)

logger.info(pprint.pprint(agentResponse))

event_stream = agentResponse['completion']
try:
    for event in event_stream:        
        if 'chunk' in event:
            data = event['chunk']['bytes']
            logger.info(f"Final answer ->\n{data.decode('utf8')}")
            agent_answer = data.decode('utf8')
            end_event_received = True
            # End event indicates that the request finished successfully
        elif 'trace' in event:
            logger.info(json.dumps(event['trace'], indent=2))
        else:
            raise Exception("unexpected event.", event)
except Exception as e:
    raise Exception("unexpected event.", e)

agentResponse = bedrock_agent_runtime_client.invoke_agent(
    inputText="How much vacation does the employee with employee_id set to 1 have available?",
    agentId=agent_id,
    agentAliasId=agent_alias_id, 
    sessionId=session_id,
    enableTrace=enable_trace, 
    endSession= end_session
)

logger.info(pprint.pprint(agentResponse))

event_stream = agentResponse['completion']
try:
    for event in event_stream:        
        if 'chunk' in event:
            data = event['chunk']['bytes']
            logger.info(f"Final answer ->\n{data.decode('utf8')}")
            agent_answer = data.decode('utf8')
            end_event_received = True
        elif 'trace' in event:
            logger.info(json.dumps(event['trace'], indent=2))
        else:
            raise Exception("unexpected event.", event)
except Exception as e:
    raise Exception("unexpected event.", e)

# cleanup
action_group_id = agent_action_group_response['agentActionGroup']['actionGroupId']
action_group_name = agent_action_group_response['agentActionGroup']['actionGroupName']

response = bedrock_agent_client.update_agent_action_group(
    agentId=agent_id,
    agentVersion='DRAFT',
    actionGroupId= action_group_id,
    actionGroupName=action_group_name,
    actionGroupExecutor={
        'lambda': lambda_function['FunctionArn']
    },
    functionSchema={
        'functions': agent_functions
    },
    actionGroupState='DISABLED',
)

action_group_deletion = bedrock_agent_client.delete_agent_action_group(
    agentId=agent_id,
    agentVersion='DRAFT',
    actionGroupId= action_group_id
)
response = bedrock_agent_client.delete_agent_alias(
    agentAliasId=agent_alias_id,
    agentId=agent_id
)
agent_deletion = bedrock_agent_client.delete_agent(
    agentId=agent_id
)
lambda_client.delete_function(
    FunctionName=lambda_function_name
)
for policy in [agent_bedrock_allow_policy_name]:
    iam_client.detach_role_policy(RoleName=agent_role_name, PolicyArn=f'arn:aws:iam::{account_id}:policy/{policy}')
    
iam_client.detach_role_policy(RoleName=lambda_function_role, PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole')

for role_name in [agent_role_name, lambda_function_role]:
    iam_client.delete_role(
        RoleName=role_name
    )

for policy in [agent_bedrock_policy]:
    iam_client.delete_policy(
        PolicyArn=policy['Policy']['Arn']
)
