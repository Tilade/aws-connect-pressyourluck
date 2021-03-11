import boto3


def lambda_handler(event, context):    
    dynamodb = boto3.resource('dynamodb')
    pylstats = dynamodb.Table('PYL_Stats')
    
    response = pylstats.scan(
        TableName='PYL_Stats',
        Select='ALL_ATTRIBUTES'
    )
    
    item = response['Items']

    scores = []
    contactID = []
    callerID = []
    #dateID = []

    ''' dump scores and ID's in unordered list'''
    x = 0
    while (x < len(item)):
        scores.append(item[x]["CurrentScore"])
        contactID.append(item[x]["CallSessionUID"])
        callerID.append(item[x]["CallerID"])
        #dateID.append(item[x]["DateTime"])
        x = x + 1
        
    '''sort lists'''
    insertionSort(scores, contactID, callerID)
    
    '''get top 5 results'''
    topFive = []
    x = -1
    while (x >= -5):
        topFive.append(str(scores[x]))
        #print ("SessionID: " + str(contactID[x]) + " User: " + str(callerID[x]) + " with $" + str(scores[x]))
        x = x - 1
    
    scorereturn = {}
    scorereturn["highScoreStatement"] = "For Number 5, the total is " + topFive[4] +  " dollars. Number 4 ," + topFive [3] + " dollars. Three, brought home " + topFive[2] + " dollars. Two, had an impressive return of " + topFive[1] + " dollars. ,,And the largest total so far is a respectable " + topFive[0] + " dollars."
    
    
    ########################################################
    
    #ANI = "+12065555555"
    ANI = event.get('Details').get('ContactData').get('CustomerEndpoint').get('Address')
    highList = []
    highCallList = []
    highContactList = []
    '''reverse order of scores from highest to lowest'''
    for o in reversed(scores):
        highList.append(o)
    
    for o in reversed(callerID):
        highCallList.append(o)
    
    for o in reversed(contactID):
        highContactList.append(o)
    
    
    
    '''introduce index counter, check for existing ANI in ordered callist, break and record index location when found'''
    index = 0
    for value in highCallList:
        if (value == ANI):
            print ('found at index: ', value, index)
            break
        index += 1
    else:
        print('High Score not found')
        index = -1
    
    '''uses above index to reference dollar value'''
    
    print ("highlist: ", highList[index])
    
    scorereturn["yourScore"]= highList[index]
    if (index == -1) and (highList[index] == 0):
        ranking = "Unranked"
    else:
        ranking = index + 1
    scorereturn["yourRank"] = str(ranking)
    
    
    ###################################################    
    
    
    #check top 5 scores
    #get UUID of current call
    #if UUID of call is in top5 scores, New hall of fame entry
    #read back ranking
    
    '''get UUID'''
    sessionID = event.get('Details').get('ContactData').get('ContactId')  #production code
    #sessionID= '1234'  # first place
    #sessionID = "1c54761c-2e32-47b0-88a4-bba50a900a9e"  #not in top 5
    #sessionID = "4819a098-61e7-4231-a63e-193f0cce73aa" #3rd place
    

    y = 0
    newRanking = 0
    
    '''check to see if UUID is in top 5 scores
    if so, replay back the rank and announcement
    if not, message gets skipped
    '''
    print (highContactList)
    while (y < 5):
        if (highContactList[y] == sessionID):
            newRanking = int(y + 1)
            scorereturn["newTopScore"] = "True"
        y += 1
    
    textNewRanking = ""
    if (newRanking == 1):
        textNewRanking = "1st"
    elif (newRanking == 2):
        textNewRanking = "2nd"
    elif (newRanking == 3):
        textNewRanking = "3rd"
    elif (newRanking == 4):
        textNewRanking = "4th"
    else:
        textNewRanking = "5th"
        
    print ("Text ranking ", textNewRanking)
      
    if newRanking == 1:
        scorereturn["topPhrase"] = "Wow, you're " + textNewRanking + " place, king of the mountain, top dog, numero uno.  Amazing and well done!  Don't forget that being at the top means that anyone can knock you down. Make sure to check back every so often to see if you're stll king."
    elif (1 < newRanking < 6):
        scorereturn["topPhrase"] = "Amazing, you finished " + textNewRanking + " and are now in the top 5 with that performance.  Congrats!  However, you know what they say about being in second place, though,,  you're the first loser. Give it another try and see if you can get to the top!"
    

    '''require return'''    
    return scorereturn
    
    ##################################################################
    
def insertionSort(alist, blist, clist):
    
    for index in range(1,len(alist)):
    
        acurrentvalue = alist[index]
        bcurrentvalue = blist[index]
        ccurrentvalue = clist[index]
        #dcurrentvalue = dlist[index]
        position = index
        
        while position>0 and alist[position-1]>acurrentvalue:
            alist[position]=alist[position-1]
            blist[position]=blist[position-1]
            clist[position]=clist[position-1]
            #dlist[position]=dlist[position-1]
            position = position-1
        
        alist[position]=acurrentvalue
        blist[position]=bcurrentvalue
        clist[position]=ccurrentvalue
        #dlist[position]=dcurrentvalue


