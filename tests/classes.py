import requests
import hashlib
import time
import json

devid='1552'
Authkey='DAF3EBE667BA4C4C94EACF26A59A9C7D'
apibase='http://api.smitegame.com/smiteapi.svc/'

def stamp():
	new=time.strftime("%Y%m%d%H%M%S")
	other=time.strftime("%H%M%S")
	if int(other)>190000:
		new=int(new)-240000+1000000
	new=int(new)+40000
	new=str(new)
	return new

def call(url):
	result=requests.get(url)
	page=result.text
	return page

def signature(method):
	sig=devid+method+Authkey+stamp()
	m=hashlib.md5()
	m.update(sig.encode('utf-8'))
	hsh=m.hexdigest()
	return str(hsh)

class session():
	def __init__(self,devid,auth):
		self.devid=devid
		newsession=apibase+'createsessionJson/'+devid+'/'+signature('createsession')+'/'+stamp()
		self.message=json.loads(call(newsession))
		self.id=self.message['session_id']

class player():
	def __init__(self,player,sessid):
		self.sessid=sessid
		self.player=player
	def getdefault(self,action,detail):
		html=apibase+action+'json/'+devid+'/'+signature(action)+'/'+self.sessid+'/'+stamp()+'/'+detail
		response=call(html)
		return json.loads(response)
	def stats(self):
		return self.getdefault('getplayer',self.player)
	def friends(self):
		return self.getdefault('getfriends',self.player)
	def gods(self):
		return self.getdefault('getgodranks',self.player)
	def history(self):
		return self.getdefault('getmatchhistory',self.player)
	def status(self):
		return self.getdefault('getplayerstatus',self.player)

class match():
	def __init__(self,match,sessid):
		self.match=match
		self.sessid=sessid
	def getdefault(self,action,detail):
		html=apibase+action+'json/'+devid+'/'+signature(action)+'/'+self.sessid+'/'+stamp()+'/'+detail
		response=call(html)
		return json.loads(response)
	def mode(self):
		return self.getdefault('getdemodetails',self.match)
	def details(self):
		return self.getdefault('getmatchdetails',self.match)
	def live(self):
		return self.getdefault('getmatchplayerdetails',self.match)



sesh=session(devid,Authkey)
print (sesh.id)
para=player('Parabola',sesh.id)
print (para.history())
m1=match('252537680',sesh.id)
print (m1.mode())