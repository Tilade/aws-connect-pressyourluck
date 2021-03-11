import boto3
import os
import random




def lambda_handler(event, context):
    '''workflow:
    
    1.  Check for gameover reason--whammy or decided to quit
    2.  playback final score and stats
    3.  Check for placement in database of users
    4.  If in top 10%, playback super positive mesasge
    	else if in 11-50%, playback good job message
    	else if in bottom 50% playback less than stellar message and invite 
    	to play again
    5.  repeat specific percentage of the player or position (?)
    6.  Text final result to player (possibly use Twilio if no verification required)
    7.  Play finishing music and ask if they would like to play again?
    '''
    sessionID = event.get('Details').get('ContactData').get('ContactId')
    
    #finalWhammy = '0'
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
    finalScore = item.get('CurrentScore')
    whammyCount = item.get('CurrentWhammy')

    if finalScore >= 20000:
    	finalStatement = scoreStatement(random.randint(10,14))

    elif finalScore >= 10000:
    	finalStatement = scoreStatement(random.randint(5,9))

    else:
    	finalStatement = scoreStatement(random.randint(0,4))

    if whammyCount == 3:
	    finalWhammy = whammyStatement(random.randint(0,3))

    elif whammyCount <= 2:
    	finalWhammy = whammyStatement(random.randint(4,7))
    
    gameover = {}
    gameover['go_statement'] = finalWhammy + finalStatement
    return gameover
	
def whammyStatement(num):
	'''quitting with 3 whammys'''
	whammyStatement = (
		"Good call, dodge the sword.  With 3 whammys, who knows if the next spin would be the last. ",
		"Probably a good decision to quit while you're ahead. ",
		"In the world of going big or going home, you seem to have chosen the latter. ",
		"ooooooh, dodging the bullet.  Ok, I respect that. ",
	#2 or fewer whammys
		"Wow, you're playing it safe and quitting early. ",
		"Kinda early maybe?  Eh, your call. ",
		"Quitting while you're ahead?  Ok, I respect that. ",
		"Are you sure you're not quitting too early?  Hopefully your score accounts for this. "
	)
	return whammyStatement[num]



def scoreStatement(num): 	
	'''score <1000'''
	scoreStatement = (
		"It's unfortunate, though, that your score isn't better.  Better luck next time. ",
		"But do you really want to quit with only that amount?  Alright, but I spend more on lunch. Here's your amount. ",
		"However, let's give it a better effort next time and get more money. ",
		"Usually I'd give you a snarky comment based on your low take home amount, but I'm in a good mood today.  Better luck next time. Let's see your result. ",
		"Ok, not great, but also not good.  Let's see how you did. ",
	#'''score > 10000'''
		"Not bad!  You'll be paying for the deluxe car wash from now on. Let's take a look. ",
		"Well, I know how's buying dinner next time, let's check out how you did. ",
		"Ok, you showed up to play and didn't do too bad.  Let's take a look. ",
		"Nicely done, could be better, but could also be much worse. Here's your result. ",
		"Alright, it truly was your lucky day. Let's see your final result.",
	#score > 20000
		"Boy you sure know how to bring home the bacon, let's check out the final score. ",
		"Holy smokes look at that number, let's check out how you did. ",
		"You're about to make some new friends with a score like that, here's the final result. ",
		"Cha ching baby!  Let's take a final look at how you did. ",
		"Good Golly talk about making it rain, here's your final result. ",
	)
	return scoreStatement[num]







