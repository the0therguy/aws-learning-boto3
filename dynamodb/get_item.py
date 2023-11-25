import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

response = table.get_item(
    Key={
        'username': 'bobsmith',
        'last_name': 'Smith'
    }
)
print(response)