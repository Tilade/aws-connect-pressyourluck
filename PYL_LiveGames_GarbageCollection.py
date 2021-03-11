import boto3
import time



def lambda_handler(event, context):

    # '''initialize table object'''
    dynamodb = boto3.resource('dynamodb')
    pylLiveGC = dynamodb.Table('PYL_LiveGame')
    
    try:
        pylLiveGC.delete()    
        print("[INFO] PYL_LiveGame DELETED")
        
    except:
        print("[ERROR] PYL_LiveGame delete NOT SUCCESSFUL")
    
    '''table operations buffer'''
    time.sleep(5)  
    
    try:
        table = dynamodb.create_table(
            TableName='PYL_LiveGame',
            KeySchema=[
                {
                    'AttributeName': 'CallerID',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'CallerID',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 75,
                'WriteCapacityUnits': 75
            }
        )
        print("[INFO] PYL_LiveGame CREATED")
    except:
        print("[CRITICAL ERROR] Table PYL_LiveGame creation FAILED")
    
    gcrun = "[INFO]: Garbage Collection Complete"
    print(gcrun)
    
    return gcrun