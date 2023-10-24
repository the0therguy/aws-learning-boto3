import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')
data = table.put_item(
   Item={
        'username': 'jonedoe',
        'last_name': 'Doe',
    }
)

print(data)