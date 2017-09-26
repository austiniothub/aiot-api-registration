from chalice import Chalice
import boto3

app = Chalice(app_name='aiot-api-registration')

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Instantiate a table resource object without actually
# creating a DynamoDB table. Note that the attributes of this table
# are lazy-loaded: a request is not made nor are the attribute
# values populated until the attributes
# on the table resource are accessed or its load() method is called.

table = dynamodb.Table('UsersRegistration')

app = Chalice(app_name='aiot-api-registration')


@app.route('/users')
def index():
    response = table.scan()
    items = response['Items']
    return items


@app.route('/users/{email}')
def get_by_id(email):
    key = {'Email': email}
    response = table.get_item(Key=key)
    item = response['Item']
    return item


@app.route('/users/create', methods=['POST'])
def put():
    user = app.current_request.json_body
    try:
        table.put_item(Item=user)
        return True
    except:
        return False


@app.route('/users/delete/{email}', methods=['DELETE'])
def delete(email):
    key = {'Email': email}
    try:
        table.delete_item(Key=key)
        return True
    except:
        return False
