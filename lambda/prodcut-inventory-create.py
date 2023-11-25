import boto3
from custom_encoder import CustomJSONEncoder

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


request_body = {
    "productID": "12414",
    "name": "product 2",
    "color": "white",
    "price": 1004
}
data = table.put_item(
    Item=request_body
)

body = {
    'Operation': 'SAVE',
    'Message': 'SUCCESS',
    'Item': request_body
}

print(build_response(status_code=201, status='OK', body=body))
