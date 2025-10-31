import json

def add(num1, num2):
    return num1 + num2

def subtract(num1, num2):
    return num1 - num2

def multiply(num1, num2):
    return num1 * num2

def divide(num1, num2):
    if num2 == 0:
        raise ValueError("division by zero")
    return num1 / num2

def power(num1, num2):
    return num1 ** num2

def lambda_handler(event, context):
    operation = event.get('operation')
    try:
        num1 = float(event['num1'])
        num2 = float(event['num2'])
    except (KeyError, ValueError):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid input, num1 and num2 must be numeric'})
        }

    # Map operations to functions
    operations = {
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide,
        'power': power
    }

    # Find the operation function and execute
    operation_func = operations.get(operation)
    
    if operation_func:
        try:
            result = operation_func(num1, num2)
            return {
                'statusCode': 200,
                'body': json.dumps({'result': result})
            }
        except ValueError as e:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': str(e)})
            }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'invalid operation'})
        }