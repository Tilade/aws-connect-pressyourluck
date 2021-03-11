import os
import boto3
import random


def lambda_handler(event, context):

    '''assign awareded money'''
    cashMoney = awardMoney()
    
    #....refactored......
    # '''assign randomized statement with money'''
    # finalStatement = winingStatement(cashMoney)

    '''add money to database'''
    #incrementMoney(event, int(cashMoney))
    incrementMoney(event, cashMoney)
    

    whatIsSaid = {}
    '''refactored command--assgin audio  statement string to returned dict'''
    whatIsSaid["moneyStatement"] = winingStatement(cashMoney)
    return whatIsSaid
    
    
def awardMoney():
    money = (100, 200, 300, 400, 500, 600, 700, 800, 900, 1000)
    awardedMoney = money[random.randint(0,9)]
    return awardedMoney

def winingStatement(mon):
    
    statements = (
        "Check please,",
        "Making it rain,",
        "Look at you, moving on up with",
        "Coming your way,",
        "Amazing, you just got",
        "Boom shakalaka,",
        "Keep this up and I'm gonna start calling you Mr. Scrooge McDuck,",
        "Rich uncle pennybags pales in comparison to you,",
        "Go Get that Money,"
        )
    '''str required to force string return vs object'''
    combinedStatement = str(statements[random.randint(0,8)] +" "+ str(mon) + " dollars")
    return combinedStatement




def incrementMoney(event, mon):
    '''get UUID'''
    sessionID = event.get('Details').get('ContactData').get('ContactId')
    
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
    currentScore += mon
    pylstats.update_item(
        Key = {
            'CallSessionUID' : sessionID,
        },
        UpdateExpression='SET CurrentScore = :val1',
        ExpressionAttributeValues={
            ':val1': currentScore
        }
    )
    
    
    

        
        

    