import requests
import hashlib
import time
import json

###Base Objects###

devid='1552'
Authkey='DAF3EBE667BA4C4C94EACF26A59A9C7D'
jjson='createsessionJson/'
apibase='http://api.smitegame.com/smiteapi.svc/'

###Base Functions###

def computeMD5hash(string):							#Creates a hash from a string
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()

def call(url):										#Brings up the text response from a webpage
	result=requests.get(url)
	page=result.text
	return page

def stamp():										#Creates a timestamp in Hirez format
	new=time.strftime("%Y%m%d%H%M%S")
	new=int(new)+50000
	new=str(new)
	return new

def signature(method):								#Creates a signature in Hirez format
	sig=devid+method+Authkey+stamp()
	m=hashlib.md5()
	m.update(sig.encode('utf-8'))
	hsh=m.hexdigest()
	return str(hsh)

###Creating Session to use###

newsession=apibase+jjson+devid+'/'+signature('createsession')+'/'+stamp()
sessionid=json.loads(call(newsession))
print (sessionid['ret_msg'])

###Call Functions###

def getdefault(action,detail):
	html=apibase+action+'json/'+devid+'/'+signature(action)+'/'+sessionid['session_id']+'/'+stamp()+'/'+detail
	response=call(html)
	return json.loads(response

def getplayer(name):
	return getdefault('getplayer',name)

def getmatchdetails(match):
	html=apibase+'getmatchdetailsjson/'+devid+'/'+signature('getmatchdetails')+'/'+sessionid['session_id']+'/'+stamp()+'/'+match
	response=call(html)
	result=json.loads(response)
	return result

def gettopmatches():
	html=apibase+'gettopmatchesjson/'+devid+'/'+signature('gettopmatches')+'/'+sessionid['session_id']+'/'+stamp()
	return json.loads(call(html))

def topmatchstat():
	match=gettopmatches()
	return (getmatchdetails(str(match[0]['Match'])))

para=getplayer('parabola')
match=topmatchstat()
print (para)
print (match)
for no in match:
	print (no['playerName']+'\t'+no['Reference_Name'])
