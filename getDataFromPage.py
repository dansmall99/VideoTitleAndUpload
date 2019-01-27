from lxml import html
import requests

from bs4 import BeautifulSoup

import time
from datetime import date


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


today = date.today()
dt = today.strftime('%Y%m%d')
date_string = today.strftime("%A %B %d, %Y")

url='http://uuabq.com/calendar/action~oneday/exact_date~' + str(today.month) + '-' + str(today.day) + '-' + str(today.year)
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
title_w_spaces = ' '.join(l1[1:])
if l2[1] in 'Reverend':
	last_name = l2[3]
	first_name  = l2[2]
else:
	last_name = l2[1]
	first_name = l2[1]

fullname = first_name + ' ' + last_name

fn = dt + '-' + title + '-' + last_name + '.mp4';
print(fn);
print(l1)
print(l2)

imglabel = date_string + '\n' + first_name + ' ' + last_name + '\n' + title_w_spaces 

#convert -background  none    -fill white  -pointsize 36  -gravity south -font Times-Bold  -draw "text 0,0 'First Unitarian Church of Albuquerque'" -gravity south  -draw "text 0,50 "  -draw "text 0,100  '$d'"  -pointsize 72  -draw "text 0,200  '$title'"  c.png  foo.png

#convert uuabq.jpg   label:imglabel  +swap  -gravity Center -append    anno_label2.jpg


print(imglabel)
