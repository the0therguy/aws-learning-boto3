import json
import boto3
import logging
from custom_encoder import CustomJSONEncoder

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb_table_name = 'product-inventory'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodb_table_name)

get_method = 'GET'
post_method = 'POST'
patch_method = 'PATCH'
delete_method = 'DELETE'
health_path = '/health'
product_path = '/product'
products_path = '/products'


def build_response(status_code, status, body=None):
    response = {
        'statusCode': status_code,
        'status': status
    }
    if body:
        response['body']= json.dumps(body, cls=CustomJSONEncoder)
    return response


def get_product(product_id):
    try:
        response = table.get_item(
            key={
                'productID': product_id
            }
        )
        if 'Item' in response:
            return build_response(status_code=200, status='OK', body=response['Item'])
        else:
            return build_response(status_code=404, status='Failed',
                                  body={'message': f"No product found with this {product_id}"})
    except error as e:
        print(e)
        return build_response(status_code=500, status='Failed', body={'message': 'Something Went Wrong'})


def get_products():
    try:
        response = table.scan()
        result = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStarKey=response['LastEvaluatedKey'])
            result.extend(response['Items'])

        body = {
            'products': response
        }
        return build_response(status_code=200, status='OK', body=body)
    except error as e:
        print(e)
        return build_response(status_code=500, status='Failed', body={'message': 'Something Went Wrong'})


def save_product(request_body):
    try:
        table.put_item(Item=request_body)
        body = {
            'Operation': 'SAVE',
            'Message': 'SUCCESS',
            'Item': request_body
        }

        return build_response(status_code=201, status='OK', body=body)
    except error as e:
        print(e)
        return build_response(status_code=500, status='Failed', body={'message': 'Something Went Wrong'})


def modify_product(product_id, update_key, update_value):
    try:
        response = table.update_item(
            key={
                'productID': product_id
            },
            UpdatedExpression='set %s = :value' % update_key,
            ExpressionAttributeValues={
                ':value': update_value
            }
        )

        body = {
            'Operation': 'UPDATE',
            'Message': 'Success',
            'UpdateAttributes': response
        }

        return build_response(status_code=200, status='OK', body=body)
    except error as e:
        print(e)
        return build_response(status_code=500, status='Failed', body={'message': 'Something Went Wrong'})


def delete_product(product_id):
    try:
        response = table.delete_item(
            key={
                'productID': product_id
            },
            ReturnValues='ALL_OLD'
        )

        body = {
            'Operation': 'DELETE',
            'Message': 'SUCCESS',
            'deletedItem': response
        }

        return build_response(status_code=204, status='OK', body=body)

    except error as e:
        print(e)
        return build_response(status_code=500, status='Failed', body={'message': 'Something Went Wrong'})


def lambda_handler(event, context):
    logger.info(event)
    http_method = event['httpMethod']
    path = event['path']
    if http_method == get_method and path == health_path:
        response =  build_response(200, 'OK')
    elif http_method == get_method and path == product_path:
        response = get_product(event['queryStringParameters']['productID'])
    elif http_method == post_method and path == product_path:
        response = save_product(json.loads(event['body']))
    elif http_method == patch_method and path == product_path:
        requestBody = json.loads(event['body'])
        response= modify_product(requestBody['productID'], requestBody['updateKey'], requestBody['updateValue'])
    elif http_method == delete_method and path==product_path:
        requestBody = json.loads(event['body'])
        response = delete_product(requestBody['productID'])
    elif http_method == get_method and path == products_path:
        response = get_products()

    else:
        response = build_response(status_code=404, status='Not found')

    return response