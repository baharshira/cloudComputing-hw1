import boto3
import json
import datetime

# Initialize AWS services
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('parking')


def lambda_handler(event, context):
    if event['httpMethod'] == 'POST' and event['resource'] == '/entry':
        # Process entry request
        query_params = event['queryStringParameters']
        license_plate = query_params['plate']
        parking_lot_id = query_params['parkingLot']
        entry_time = datetime.datetime.now().isoformat()

        # Insert entry data into DynamoDB
        item = {
            'license_plate': license_plate,
            'entry_time': entry_time,
            'parking_lot_id': parking_lot_id
        }
        table.put_item(Item=item)

        # Return ticket ID
        ticket_id = str(item['entry_time']) + '-' + license_plate
        response = {
            'statusCode': 200,
            'body': json.dumps({'ticketId': ticket_id})
        }
        return response

    elif event['httpMethod'] == 'POST' and event['resource'] == '/exit':
        # Process exit request
        query_params = event['queryStringParameters']
        ticket_id = query_params['ticketId']
        exit_time = datetime.datetime.now().isoformat()

        # Retrieve entry data from DynamoDB
        response = table.get_item(Key={'ticket_id': ticket_id})
        entry_data = response.get('Item', None)

        if entry_data:
            license_plate = entry_data['license_plate']
            entry_time = entry_data['entry_time']
            parking_lot_id = entry_data['parking_lot_id']
            entry_time = datetime.datetime.fromisoformat(entry_time)
            exit_time = datetime.datetime.fromisoformat(exit_time)

            # Calculate parking charge
            charge = calculate_charge(entry_time, exit_time)

            # Update exit time and charge in DynamoDB
            table.update_item(
                Key={'ticket_id': ticket_id},
                UpdateExpression='SET exit_time = :exit_time, charge = :charge',
                ExpressionAttributeValues={
                    ':exit_time': exit_time.isoformat(),
                    ':charge': charge
                }
            )

            # Return parking details
            response = {
                'statusCode': 200,
                'body': json.dumps({
                    'licensePlate': license_plate,
                    'totalParkedTime': str(exit_time - entry_time),
                    'parkingLotId': parking_lot_id,
                    'charge': charge
                })
            }
            return response
        else:
            # Ticket ID not found in DynamoDB
            response = {
                'statusCode': 404,
                'body': json.dumps({'error': 'Ticket ID not found'})
            }
            return response

    else:
        # Invalid resource or HTTP method
        response = {
            'statusCode': 404,
            'body': json.dumps({'error': 'Invalid resource or HTTP method'})
        }
        return response


def calculate_charge(entry_time, exit_time):
    """
    Calculate the parking charge based on the entry and exit time.
    Charge is $10 per hour, rounded up to the nearest 15 minutes.
    """
    time_difference = exit_time - entry_time
    hours = time_difference.total_seconds() / 3600
    charge = round((hours * 10), 2)
    return charge
