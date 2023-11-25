import boto3
from custom_encoder import CustomJSONEncoder
import json

dynamodb_table_name = 'product-inventory'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodb_table_name)


def build_response(status_code, status, body=None):
    response = {
        'statusCode': status_code,
        'status': status
    }
    if body:
        response['body']= json.dumps(body, cls=CustomJSONEncoder)
    return response

response = table.scan()
result = response['Items']
while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStarKey=response['LastEvaluatedKey'])
    result.extend(response['Items'])
# print(result)
body = {
    'products': result
}
print(build_response(status_code=200, status='OK', body=body))