import boto3
import os


def lambda_handler(event, context):
    
    '''intilize SNS'''
    msg = boto3.client('sns')
    
    
    sessionID = event.get('Details').get('ContactData').get('ContactId') 
    #sessionID = '1234'
    '''database connection'''
    dynamodb = boto3.resource('dynamodb')
    pylstats = dynamodb.Table('PYL_Stats')
    response = pylstats.get_item(
    TableName = 'PYL_Stats',
    Key = {
        'CallSessionUID' : sessionID
        }
    )
    item = response['Item'] 
    
    '''get results from DB'''
    finalScore = item.get('CurrentScore')
    finalSpin = item.get('CurrentSpinCount')
    finalWhammy = item.get('CurrentWhammy')
    phoneNumber = item.get('CallerID')
    
    finalMsg = str("Congratulations and thanks for playing.  You're taking home $" + str(finalScore) + " with " + str(finalSpin)+ " spins. You had "+ str(finalWhammy) + " whammys!")
    print (finalMsg)
    print (phoneNumber)
    '''send msg'''
    response = msg.publish(
        PhoneNumber=phoneNumber,
        Message= finalMsg
    )
    
    lambdaRun = {'success' : 'True'}
    
    return lambdaRun