# aws-connect-pressyourluck

**Press Your Luck**

*Most resources for this demo will be prefixed with “PYL”*



<u>Web Hosting</u>

Purpose: Place for dashboard to view games in progress and search for scores from past sessions

Service(s): S3

Bucket: connect-pressyourluck-staticwebsite/index2.html

URL: https://connect-pressyourluck-staticwebsite.s3.amazonaws.com/index2.html

 

<u>Stats and Scores</u>

Purpose: Place to write historical stores and query status for games in progress 

Service(s): DynamoDB

Tables: PYL_LiveGame, PYL_Stats

-**IMPORTANT** PYL_LiveGame lists games in progress and is automatically deleted and rebuilt after 5 minutes. This table also includes a DynamoDB stream attached that writes values to the historical table during gameplay.

​        -PYL_Stats lists historical stats of play and supports lookups from web browser and phone call

 

<u>Garbage Collection</u>

Purpose: A (brute force) method of deleting and rebuilding the live-game table to prevent sessions that never complete the game from appearing still in progress. 

Service(s): Cloudwatch Events

Rule: PYL_GarbageCollection_Event

 

<u>Phone call IVR Interface</u>

Purpose: Provides a phone number interface for game players

Service(s): Connect

Instance Alias: pressyourluck

Phone Number: 480-386-0883

Contact Flow: PYL_CurrentRank, PYL_DTMF-Gameover, PYL_Game_BigBoard, PYL_Game_rules, 

PYL_GameOver, PYL_Intro, PYL_MoneyNStats, PYL_PlayerInitialization, PYL_Sandbox, PYL_TopFive, PYL_WhammyGameOver

 

<u>Game Logic</u>

Purpose: The mechanics of gameplay

Service(s): Lambdas

Function Names: PYL_SpinCounter, PYL_InitializePlayer, PYL_LiveGames_GarbageCollection, PYL_DTMF_Gameover, PYL_GameoverHighScoreCheck, PYL_TextConfirmation, PYL_PrizeWon, PYL_LiveGames, PYL_MoneyandStats, PYL_highscore, PYL_WinMoney, PYL_whammy_gameover, PYL_GameOver, PYL_BigBucks, PYL_WhammyIncrement

 

 

 

 