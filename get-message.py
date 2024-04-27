import boto3
from botocore.exceptions import ClientError
import requests
import json
import pprint

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/qnd8mu"
sqs = boto3.client('sqs')

def delete_message(handle):
    try:
        # Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=handle
        )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])

def get_message():
    messages = {}
    for i in range(10):
        try:
            # Receive message from SQS queue. Each message has two MessageAttributes: order and word
            # You want to extract these two attributes to reassemble the message
            response = sqs.receive_message(
                QueueUrl=url,
                AttributeNames=[
                    'All'
                ],
                
                MessageAttributeNames=[
                    'All'
                ],
                
            )
            
            if "Messages" in response:
                
                # extract the two message attributes you want to use as variables
                # extract the handle for deletion later
                order = response['Messages'][0]['MessageAttributes']['order']['StringValue']
                word = response['Messages'][0]['MessageAttributes']['word']['StringValue']
                handle = response['Messages'][0]['ReceiptHandle']
                
                messages[order] = word
                

                # Print the message attributes - this is what you want to work with to reassemble the message
                print(f"Order: {order}")
                print(f"Word: {word}")

            # If there is no message in the queue, print a message and exit    
            else:
                print("No message in the queue")
                print("Unsorted Values!")
                pprint.pprint(messages)
                sorted_messages = {k: messages[k] for k in sorted(messages, key=lambda k: str(k))}
                return sorted_messages
                # break
                # exit(1)
                
        # Handle any errors that may occur connecting to SQS
        except ClientError as e:
            print(e.response['Error']['Message'])
    

# Trigger the function
if __name__ == "__main__":
    
    contents = get_message()  
    print("Final Values!")  #gets sorted dictionary
    pprint.pprint(contents)
    
    print("Complete Sentence:") #prints out the complete sentence
    for key in sorted(contents):
        print(contents[key], end = " ")
    