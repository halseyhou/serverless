import boto3
import json
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    payloads = event['Records'][0]["Sns"]
    msg = json.loads(payloads['Message'])
    SENDER = "support@demo.xihou.me"
    RECIPIENT = msg['to']

    DESTINATION = {'ToAddresses': [
            msg['to'],
        ]
    }

    SUBJECT = payloads['Subject']
    BODY = msg['content']
    CHARSET = "UTF-8"

    client = boto3.client('ses')
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('emailTrackingTable')

    try:
        resp = table.get_item(Key={'email': BODY})
        item = resp.get('Item', {})
        if item:
            print('The email content has been sent!')
            return {'statusCode': 200, 'body': json.dumps(item)}
        resp = client.send_email(
            Destination=DESTINATION,
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
        table.put_item(Item={'email': BODY})

    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print(resp)
        print("Email sent! Message ID:")
        print(resp['MessageId'])
        print(RECIPIENT)

        return {
            'statusCode': 200,
            'body': json.dumps(resp)
        }
