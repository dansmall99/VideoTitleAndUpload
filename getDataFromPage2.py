from lxml import html
import requests

from bs4 import BeautifulSoup

import time
from datetime import date
import os
import datetime as dt

now = dt.datetime.now()
ago = now-dt.timedelta(minutes=180)

for root, dirs,files in os.walk('.'):  
    for fname in files:
        path = os.path.join(root, fname)
        st = os.stat(path)    
        mtime = dt.datetime.fromtimestamp(st.st_mtime)
        if mtime > ago:
            print('%s modified %s'%(path, mtime))


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


today = date.today()
dt = today.strftime('%Y%m%d')

url='http://uuabq.com/calendar/action~oneday/exact_date~' + str(today.month) + '-' + str(today.day) + '-' + str(today.year)
url='http://uuabq.com/calendar/action~oneday/exact_date~9-10-2017' 
print ('getting:' + url)
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
titles=soup.find_all(class_="ai1ec-event-title")
preachers=soup.find_all(class_="ai1ec-popup-excerpt")

for t,p in zip(titles,preachers):
	if str(t).find('Worship:') != -1:
		foo1 = str(t.contents)
		foo2 = str(p.contents)
		print(str(t.contents).strip())
		print(str(p.contents).strip())
		break

import re
regex1 = re.compile(r'\\n')
regex2 = re.compile(r'\\t')
regex3 = re.compile('[^a-zA-Z ]')
#First parameter is the replacement, second parameter is your input string
foo1_1 = regex1.sub('', foo1[2:-2])
foo1_2 = regex2.sub('', foo1_1)
foo1_3 = regex3.sub('', foo1_2)


foo2_1 = regex1.sub('', foo2[2:-2])
foo2_2 = regex2.sub('', foo2_1)
foo2_3 = regex3.sub('', foo2_2)

l1 = foo1_3.split(" ")
l2 = foo2_3.split(" ")

title = ''.join(l1[1:])
if l2[1] in 'Reverend':
	preaching = l2[3]
else:
	preaching = l2[1]

fn = dt + '-' + title + '-' + preaching + '.mp4';
print(fn);
print(l1)
print(l2)


