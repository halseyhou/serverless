import json
import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    payloads = event['Records'][0]["Sns"]
    msg = json.loads(payloads['Message'])
    SENDER = "notification@demo.xihou.me"
    RECIPIENT = msg['to']

    DESTINATION = {'ToAddresses': [
            msg['to'],
        ]
    }

    SUBJECT = payloads['Subject']
    BODY = msg['content']
    CHARSET = "UTF-8"

    client = boto3.client('ses')

    try:
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
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:")
        print(resp['MessageId'])
        print(RECIPIENT)

        return {
            'statusCode': 200,
            'body': json.dumps(resp)
        }
