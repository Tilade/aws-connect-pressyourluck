import boto3
import os
import random


def lambda_handler(event, context):
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
    finalScore = item.get('CurrentScore')
    
    '''final score based statement'''
    if finalScore >= 20000:
        finalStatement = scoreStatement(random.randint(10,14))

    elif finalScore >= 10000:
    	finalStatement = scoreStatement(random.randint(5,9))

    else:
    	finalStatement = scoreStatement(random.randint(0,4))
    	

    '''final whammy statement'''
    finalWhammy = whammyStatement(random.randint(0,6))

    
    gameover = {}
    gameover['go_statement'] = finalWhammy + finalStatement
    return gameover



def scoreStatement(num): 	
	'''score <1000'''
	scoreStatement = (
		"It's unfortunate your score isn't better.  Better luck next time. ",
		"See what that Whammy did? In case you didn't, here's your final score. ",
		"Whammy's kill scores, And they killed yours.  Here's the result.",
		"Usually I'd give you a snarky comment based on your low take home amount, but I'm in a good mood today.  Better luck next time. Let's see your result. ",
		"Ok, not great, but also not good.  Let's see how you did. ",
	#'''score > 10000'''
		"Not bad!  You'll be paying for the deluxe car wash from now on. Let's take a look. ",
		"Well, I know how's buying dinner next time, let's check out how you did. ",
		"Ok, you showed up to play and didn't do too bad.  Let's take a look. ",
		"Nicely done, could be better, but could also be much worse. Here's your result. ",
		"Hey hey hey, luck was certaintly on your side today--you finished with a whammy and still had a decent score. Let's see how you did.",
	#score > 20000
		"Even with that final Whammy, boy you sure know how to bring home the bacon, let's check out the final score. ",
		"Holy smokes look at that number, imagine how large it could have been without that final whammy.  Let's check out how you did. ",
		"You're about to make some new friends with a score like that.  It's too bad you had to end on a whammy.  Here's the final result. ",
		"Even with a Whammy, Cha ching baby!  Let's take a final look at how you did. ",
		"Whammy's don't stop you from making it rain, here's your final result. ",
	)
	return scoreStatement[num]


def whammyStatement(num): 	
    statement = (
        "You flew too close to the sun and got burned. ",
        "And that's the way the cookie crumnbles",
        "Look at this way, at least it was a short game and didn't waste too much of your time. ",
        "And that's the end of that chapter. ",
        "You Lose, good day to you! ",
        "Your game is now over. ",
        "G A M E O V E R Game Over Game Over. ",
    )
    return statement[num]