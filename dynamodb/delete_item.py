import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')


data = table.delete_item(
    Key={
        'username': 'janedoe',
        'last_name': 'Doe'
    }
)
print(data)