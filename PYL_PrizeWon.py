import boto3
import os
import random

def lambda_handler(event, context):
    prizeAmount = (2499, 7599, 19995, 6595, 3500, 4500, 1800, 8500, 5000, 900, 1300)    
    prizeObject = (
        "A new watch", 
        "An all expenses paid trip to tahiti", 
        "A brand new car", 
        "A new dinette set", 
        "A new entertainment and gaming system", 
        "A trip to the florida keys", 
        "A brand new computer",
        "A camper",
        "A trip to Las Vegas with $2000 in spending money",
        "An exercise rowing machine",
        "A tredmill"
    )
    randomPrize = random.randint(0,10)
    statement = (
        "Boo yeah, sometimes prizes are better than cash.  You won " + str(prizeObject[randomPrize]) + " valued at a whopping " + str(prizeAmount[randomPrize]) + " dollars.",
        "Well look at this, you've won one of our fabulous prizes.  Let's see what you won. " +  str(prizeObject[randomPrize]) + " priced at a lovely " + str(prizeAmount[randomPrize]) + " dollars.  How lovely indeed.",
        "Go get that prize.  You're taking home " + str(prizeObject[randomPrize]) + ".  This beauty's retail price is " + str(prizeAmount[randomPrize]) + " dollars.  How about those apples?"
    )
 
    prizeStatement = str(statement[random.randint(0,2)])
    print (prizeStatement)
    
    dynamodb = boto3.resource('dynamodb')
    pylstats = dynamodb.Table('PYL_Stats')
    
    sessionID = event.get('Details').get('ContactData').get('ContactId')
    #sessionID = "1234"
    response = pylstats.get_item(
    TableName = 'PYL_Stats',
    Key = {
        'CallSessionUID' : sessionID
        }
    )
    item = response['Item'] 
    currentScore = item.get('CurrentScore')
    
    currentScore += prizeAmount[randomPrize]
    
    pylstats.update_item(
        Key = {
            'CallSessionUID' : sessionID,
        },
        UpdateExpression='SET CurrentScore = :val1',
        ExpressionAttributeValues={
            ':val1': currentScore
        }
    )
    score = {}
    score ['returnScore'] = prizeStatement
    print (currentScore)

    return score