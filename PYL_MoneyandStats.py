'''Function returns back total cash, spin, and whammy count
stored in database'''

import boto3
import os


def lambda_handler(event, context):

    '''initialize table object'''
    dynamodb = boto3.resource('dynamodb')
    pylstats = dynamodb.Table('PYL_Stats')

    '''capture UUID'''
    sessionID = event.get('Details').get('ContactData').get('ContactId')


    '''Get Item from Database'''
    response = pylstats.get_item(
        TableName = 'PYL_Stats',
        Key = {
            'CallSessionUID' : sessionID
        }
    )
    item = response['Item']
    
    
    '''return money and spin values as a string'''
    moneyAndStats = {}
    moneyAndStats['Money'] = str(item.get('CurrentScore'))
    moneyAndStats['Spins'] = str(item.get('CurrentSpinCount'))
    moneyAndStats['Whammy'] = str(item.get('CurrentWhammy'))
    
    return moneyAndStats
    
