import boto3
import os
import random


def lambda_handler(event, context):



    bigBucksAmount = [2000, 3000, 4000, 5000, 10000, 20000]

    dollarAmount = {}
    money = bigBucksAmount[random.randint(0,5)]
    print (money)
    

    statement = (
        "Cash Money Time, you just nailed " + str(money) + " dollars.  Nicely Done.",
        "Jumping Jimminy Cricket!  Benjamins all over the place.  You're adding " + str(money) +" dollars to your total ",
        "Now you're riding in jet planes, wearing gold chains, and making it rain. " + str(money) + " dollars, good job.",
        "Oh Snap, you just banked " + str(money) + " dollars! That's quite the pay day!",
        ",,Wait,,Can you hear someting beeping? ,,That's the sound of you backing up the truck with " + str(money) + " dollars.  Well done!"
    )
    
    
    dollarAmount['bigBucksStatement'] = str(statement[random.randint(0,4)])
    
    '''get UUID'''
    sessionID = event.get('Details').get('ContactData').get('ContactId')
    #sessionID = '1234'
    ''''database connection '''
    dynamodb = boto3.resource('dynamodb')
    pylstats = dynamodb.Table('PYL_Stats')
    response = pylstats.get_item(
    TableName = 'PYL_Stats',
    Key = {
        'CallSessionUID' : sessionID
        }
    )
    item = response['Item'] 
    
    '''increment based on CashMoney generated and update DB'''
    currentScore = item.get('CurrentScore')
    currentScore += money
    pylstats.update_item(
        Key = {
            'CallSessionUID' : sessionID,
        },
        UpdateExpression='SET CurrentScore = :val1',
        ExpressionAttributeValues={
            ':val1': currentScore
        }
    )
    return dollarAmount