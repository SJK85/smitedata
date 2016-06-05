from base import *

f=open('output','w')
raw=open('rawoutput','w')

comp=getgods()
count=0

def showdata(dat):
	for dic in dat:
		if type(dic)==type({}):
			global count
			x=count
			f.write('-----List {}-----\n'.format(x))
			itdic(dic)
			f.write('-----List {} ENDED-----\n'.format(x))
			count+=1
		else:
			f.write('list: {}\n')


def itdic(dic):
	if type(dic)==type([]):
		showdata(dic)
	if type(dic)==type({}):
		for d2 in dic:
			if type(dic[d2])==type({}):
				f.write('\n--key: {}--\n\n'.format(d2))
				itdic(dic[d2])
				f.write('\n--Key: {} ENDED--\n\n'.format(d2))
			if type(dic[d2])==type([]):
				f.write('\n--key: {}--\n\n'.format(d2))
				showdata(dic[d2])
				f.write('\n--key: {} ENDED--\n\n'.format(d2))
			elif type(dic[d2])!=type({}):
				f.write('key: {0:<20s} \t\t\tvalue: {1}\n'.format(d2,dic[d2]))

def topline(dat):
	count=0
	for dic in dat:
		f.write('\n\n\n----------ENTRY NUMBER {}----------\n\n\n'.format(count))
		itdic(dic)
		count+=1

topline(comp)
raw.write(str(comp))
