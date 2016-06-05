import requests
from bs4 import BeautifulSoup as soup
import urllib.request
import re
import sys

#returns list with all the img links
def getpics(url):
	request=requests.get(url)
	page=request.text
	doc=soup(page,'html.parser')
	imglink=[element.get('src') for element in doc.find_all('img')]
	return imglink

#only grabs the first arg after the filename
website=sys.argv
url=website[1]
print ('getting pictures from {}'.format(url))
pics=[]
new=getpics(url)

#cuts off the // in front of the webadress
for img in new:
	pics.append(img[2:])

count=0

#will download image file from the url and put into the directory specified
for imgur in pics:
	sea=re.match('.*i.imgur',imgur)
	if sea:
		bot='http://'+imgur
		count+=1
		urllib.request.urlretrieve(bot,'/home/stephen/Pictures/Auto/'+imgur[12:])

print ('Copied {} images'.format(count))