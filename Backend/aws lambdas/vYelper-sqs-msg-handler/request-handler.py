import json
import boto3

def lambda_handler(event, context):

    # Create SQS client
    sqs = boto3.client('sqs')

    #queue_url = HIDDEN DUE TO SECURITY REASONS

    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'All'
        ],
        MaxNumberOfMessages=10,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=30,
        WaitTimeSeconds=0
    )
    
    messages = response['Messages']
    
    hmap = {}
    rhandle = {}
    
    for i in range(len(messages)):
        id = messages[i]['MessageId']
        hmap[id] = messages[i]['MessageAttributes']
        rhandle[id] = messages[i]['ReceiptHandle']    # collecting all reciept handles, so as to delete later
    
    print("The stu"+str(hmap))
    for k,v in hmap.items():
        dinning = v['dinning']['StringValue']
        area = v['area']['StringValue']
        phone = v['phone']['StringValue']
        cuisine = v['cuisine']['StringValue']
        people = v['people']['StringValue']
        time = v['time']['StringValue']
        date = v['date']['StringValue']
        print(dinning)
        print(area)
    
    
    for k,v in rhandle.items():
        # Delete received messages from queue
        print(v)
        res_del = sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=v
        )
        print('Received and deleted message handle: %s' %v)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
