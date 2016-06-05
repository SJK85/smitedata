import requests
import hashlib
import time
import json

#Anything marked with ####  (4 # marks) represents a bug or issue that needs to be properly completed

###Base Objects###


devid='1552'
dev=open('dev.txt','r')
Authkey=dev.read()
apibase='http://api.smitegame.com/smiteapi.svc/'


###Base Functions###


#Creates a hash from a string

def computeMD5hash(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()

#Brings up the text response from a webpage
#Used to get the json response from the api

def call(url):
	result=requests.get(url)
	page=result.text
	return page

#Creates a timestamp in Hirez format
#Have to adjust hours to get to work
#Use EST as the standard then work from there
####Will need to update so the time shifts correctly for changing months and years. Right now only adjusted for a change in day.

def stamp():
	new=time.strftime("%Y%m%d%H%M%S")
	other=time.strftime("%H%M%S")
	if int(other)>190000:
		new=int(new)-240000
	new=int(new)+1050000
	new=str(new)
	return new

#Creates a signature in Hirez format
#Method refers to which call you are using, each requires a different signature

def signature(method):
	sig=devid+method+Authkey+stamp()
	m=hashlib.md5()
	m.update(sig.encode('utf-8'))
	hsh=m.hexdigest()
	return str(hsh)


###Creating Session to use###


newsession=apibase+'createsessionJson/'+devid+'/'+signature('createsession')+'/'+stamp()
sessionid=json.loads(call(newsession))


###Call Functions###

#All of these functions will bring back a list
#The list will consist of dictionaries inside, which may have more dictionaries inside


#Function used to create building blocks of calls
#Can be used with most other calls to simplify

def getdefault(action,detail):
	html=apibase+action+'json/'+devid+'/'+signature(action)+'/'+sessionid['session_id']+'/'+stamp()+'/'+str(detail)
	response=call(html)
	return json.loads(response)

#Checks the data used up against the API limits

def getdataused():
	html=apibase+'getdataused'+'json/'+devid+'/'+signature('getdataused')+'/'+sessionid['session_id']+'/'+stamp()
	response=call(html)
	return json.loads(response)

#Returns info back regaurding a current match
#Uses the matchid as the arg

def getdemodetails(match):
	return getdefault('getdemodetails',match)

#Returns information about the proleague, including teams and matchups

def getesports():
	html=apibase+'getesportsproleaguedetails'+'json/'+devid+'/'+signature('getesportsproleaguedetails')+'/'+sessionid['session_id']+'/'+stamp()
	response=call(html)
	print (response)
	return json.loads(response)

#Will return the friends of the player specified
#Uses the players name as arg

def getfriends(player):
	return getdefault('getfriends',player)

#Returns god stats for the player
#Returns every god
#Uses the players name as arg

def getgodranks(player):
	return getdefault('getgodranks',player)

#Returns every god with their abilities and scaling
#The arg #1 is to specify english language, can use other languages

def getgods():
	return getdefault('getgods','1')

#Returns the recommended items for a god
#Uses the godid for arg, can find in other calls

def recommendeditems(godid):
	return getdefault('getgodrecommendeditems',str(godid)+'/1')

#Returns every item, gives stats, tiers, and so much more

def getitems():
	return getdefault('getitems','1')

#Returns information about a particular match
#Uses matchid for the arg

def getmatchdetails(match):
	return getdefault('getmatchdetails',match)

#Returns information about a LIVE match
#Uses matchid for the arg

def getmatchplayerdetails(match):
	return getdefault('getmatchplayerdetails',match)

#Returns match ids for the que, date, and hour you specify
#Que is 3 digit number for each mode
#Date is 8 digit number YYYYMMDD
#Hour is 0-23 (military)
#Hour can use -1, which returns the entire day

def getmatchidsbyqueue(que,date,hour):
	html=apibase+'getmatchidsbyqueuejson/'+devid+'/'+signature('getmatchidsbyqueue')+'/'+sessionid['session_id']+'/'+stamp()+'/'+str(que)+'/'+str(date)+'/'+str(hour)
	response=call(html)
	return json.loads(response)

#Returns list of the top people in each tier for ranked
#I have only gotten back empty lists thus far, not sure what I should be using for season or if it's the API
#Que is a 3 digit number for each mode
#Tier is a 2 digit number starting at 1 (Bronze V), and ending at 26 (Masters)
#Season starts at 1 and goes up once every month (according to Hi-Rez)

def getleagueleaderboard(que,tier,season):
	detail=str(que)+'/'+str(tier)+'/'+str(season)
	return getdefault('getleagueleaderboard',str(detail))

#Returns all the different seasons going on for the que
#Que is a 3 digit number for each mode
#I assume the id you get back from this should work with leaderboards, but doesn't seem to work

def getleagueseasons(que):
	return getdefault('getleagueseasons',que)

#Returns a list of recent matches with data
#Uses player name as arg

def getmatchhistory(player):
	return getdefault('getmatchhistory',player)

#Returns overall information about the player
#Uses player name as arg

def getplayer(player):
	return getdefault('getplayer',player)

#Returns current player status
#0-Offline, 1-In Lobby, 2-God Selection, 3-In Game, 4-Online
#Uses player name as arg

def getplayerstatus(player):
	return getdefault('getplayerstatus',player)

#Returns summary statistics by god for the que specified
#Que is a 3 digit number for each mode
#Uses player name for player

def getqueuestats(player,que):
	detail=str(player)+'/'+str(que)
	return getdefault('getqueuestats',detail)

#Returns players in clan and basic clan information
#Uses clanid which can be found in player data or searchteams if not known

def getteamdetails(clanid):
	return getdefault('getteamdetails',clanid)

#Returns recent matches from the clan
#Uses clanid, not name
#I only got back empty lists, though it might be because the search I tried never grouped. So could be based on matches with multiple clan members in it

def getteammatchhistory(clanid):
	return getdefault('getteammatchhistory',clanid)

#Returns all the players in the clan with some info
#Uses clanid, not name

def getteamplayers(clanid):
	return getdefault('getteamplayers',clanid)

#Returns the top 50 most watched / recorded matches

def gettopmatches():
	html=apibase+'gettopmatchesjson/'+devid+'/'+signature('gettopmatches')+'/'+sessionid['session_id']+'/'+stamp()
	return json.loads(call(html))

#Returns Clan that fit into the search
#Does a string search based on clanname

def searchteams(clanname):
	return getdefault('searchteams',clanname)
