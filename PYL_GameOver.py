import boto3
import os


def lambda_handler(event, context):
    
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
    
    finalScore = item.get('CurrentScore')
    finalSpin = item.get('CurrentSpinCount')
    whammyCount = item.get('CurrentWhammy')
    callerID = item.get("CallerID")
    
    if whammyCount == 4:
        whammyMsg = "It's a crying shame you finished on a whammy.  Better luck next time."
    else:
        whammyMsg = "And good for you, not ending the game on a whammy like many others have."
    
    '''delete entry from LiveGame table'''
    deleteLiveGame(callerID)
    
        
    returnedPrompt = {}
    returnedPrompt["finalspeech"] = "You're taking home " + str(finalScore) + " dollars with having spun the big board " + str(finalSpin) + " times. " + whammyMsg + " Hope you had fun and come back soon."
    returnedPrompt["textMsg"] = "If you would like a text copy for confirmation of your score, press 1 and a message will be sent to your phone with your results.  Otherwise, feel free to hang-up and thanks for playing!"
    
    
    return returnedPrompt
    
def deleteLiveGame(a):
    '''database connection'''
    dynamodb = boto3.resource('dynamodb')
    pylLive = dynamodb.Table('PYL_LiveGame')
    
    pylLive.delete_item(
    Key={
        'CallerID': a
    }
)
    
    
    
    
    