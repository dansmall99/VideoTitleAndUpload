#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import wx
import subprocess
import sys
from lxml import html
import requests
from bs4 import BeautifulSoup
import time
from datetime import date
import os
import datetime as dt
from pathlib import Path
import datetime
from shutil import copyfile



now = dt.datetime.now()
ago = now-dt.timedelta(minutes=180)

chaliceImage = ''

def get_video_files(videoDir):
        videoFilelist = []
        for root, dirs,files in os.walk(videoDir):  
            for fname in files:
                path = os.path.join(root, fname)
                st = os.stat(path)    
                mtime = dt.datetime.fromtimestamp(st.st_mtime)
                if mtime > ago:
                    if Path(fname.lower()).suffix == '.ts' or Path(fname.lower()).suffix == '.mp4':
                       print('%s modified %s'%(path, mtime))
                       videoFilelist.append(path)
        return videoFilelist
 


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)



def get_output_filenames():
        fns = []
        today = date.today()
        dt = today.strftime('%Y%m%d')

        next_sunday = next_weekday(today, 6) # 0 = Monday, 1=Tuesday, 2=Wednesday...
        dt = next_sunday.strftime('%Y%m%d')
        date_string = next_sunday.strftime("%A %B %d, %Y")


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
        title_w_spaces = ' '.join(l1[1:])


        if l2[1] in 'Reverend':
                fullname = ' '.join(l2[0:4])        
                preaching = l2[3]
        else:
                fullname = ' '.join(l2[0:2])        
                preaching = l2[1]

        fn = dt + '-' + title + '-' + preaching + '.mp4';
        print(fn);
        print(l1)
        print(l2)

        if sys.platform == 'linux':
                sysString = "convert -background  none  " 
                sysString += " chaliceSrc.png -fill white  -pointsize 72  -gravity north -font Times-Bold  -draw \"text 0,20 \'First Unitarian Church of Albuquerque\'\" "  
                sysString += " -gravity south  -draw \"text 0,50 \'" + fullname + "\'\""  
                sysString += " -draw \"text 0,120  \'" + date_string + "\'\"  -pointsize 72  "
                sysString += "-draw \"text 0,200  \'" + title_w_spaces + " \'\" " + dt + "_chalice.png"
                print(sysString)
                os.system(sysString)
        else:
                sysString = "magick.exe -background  none  " 
                sysString += " chaliceSrc.png -fill white  -pointsize 72  -gravity north -font Times-Bold  -draw \"text 0,20 \'First Unitarian Church of Albuquerque\'\" "  
                sysString += " -gravity south  -draw \"text 0,50 \'" + fullname + "\'\""  
                sysString += " -draw \"text 0,120  \'" + date_string + "\'\"  -pointsize 72  "
                sysString += "-draw \"text 0,200  \'" + title_w_spaces + " \'\" " + dt + "_chalice.png"
                print(sysString)
                os.system(sysString)
                sysString = "del c:\\Users\\Owner\\Pictures\\*_chalice.png" 
                os.system(sysString)
                sysString = "copy " + dt + "_chalice.png" + " c:\\Users\\Owner\\Pictures"
                os.system(sysString)
                sysString =  "\"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe\" c:\\Users\\Owner\\Pictures\\" + dt + "_chalice.png" 
                os.system(sysString)
        chaliceImage = dt + "_chalice.png"

        fns.append(fn)
        fns.append(chaliceImage)
        return fns


class VideoJoinAndUpload(wx.Frame):
    cbList = []
    fl = []
    outfile = ''
    chaliceImg = ''
    destDir = '/home/small'
    chaliceCB = ''
    def __init__(self, *args, **kw):
        super(VideoJoinAndUpload, self).__init__(*args, **kw)

        self.InitUI()

    def InitUI(self):
        pnl = wx.Panel(self)
        fns = get_output_filenames();
        self.outFile = fns[0]
        self.chaliceImg = fns[1]
        print('output = ' + self.outFile)
        print('chaliceImg = ' + self.chaliceImg)
        self.fl = get_video_files('./videos')
        x = self.fl
        print(*x)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.chaliceCB = wx.CheckBox(pnl, label="Use Chalice Intro Image?")
        self.chaliceCB.SetValue(True)
        vbox.Add(self.chaliceCB, flag=wx.TOP|wx.LEFT, border=10)
        pnl.SetSizer(vbox)
        l1 = wx.StaticText(pnl, -1, "Video Files to include:")
        vbox.Add(l1, flag=wx.TOP|wx.LEFT, border=10)

        for file in self.fl:
            cb = wx.CheckBox(pnl, label=os.path.basename(file))
            cb.SetValue(True)
            vbox.Add(cb, flag=wx.TOP|wx.LEFT, border=10)
            pnl.SetSizer(vbox)
            self.cbList.append(cb)

        basicLabel = wx.StaticText(pnl, -1, "OutputFile")
        self.basicText = wx.TextCtrl(pnl, -1, self.outFile, size=(275, -1))
        self.basicText.SetInsertionPoint(0)
        vbox.Add(basicLabel, flag=wx.TOP|wx.LEFT, border=10)
        vbox.Add(self.basicText, flag=wx.TOP|wx.LEFT, border=10)

        closeButton = wx.Button(pnl, label='Create File and Upload')
        vbox.Add(closeButton, flag=wx.TOP|wx.LEFT, border=10)
        closeButton.Bind(wx.EVT_BUTTON, self.createFile)

        self.SetTitle('uploader')
        self.Centre()

    def createFile(self, e):
        i = 0
        finalFileList = []
        
        sysString = "melt "
        if self.chaliceCB.GetValue():
           sysString += self.chaliceImg + " in=0 out=90 " 
        for cb in self.cbList:
            if cb.GetValue():
                finalFileList.append(self.fl[i])
                sysString += self.fl[i] + " "
            i = i + 1
        sysString += " -consumer avformat:" + self.basicText.GetValue() + " -profile atsc_1080p_30 acodec=libmp3lame vcodec=libx264"
        print(sysString)
        os.system(sysString)

        copyfile(self.basicText.GetValue(), os.path.join(self.destDir, self.basicText.GetValue()))
        wx.MessageBox(message='copied file: ' + self.basicText.GetValue() + ' to ' + os.path.join(self.destDir, self.basicText.GetValue()), caption='Conversion Complete', style=wx.OK | wx.ICON_INFORMATION)

                             
         
	    

def main():

    app = wx.App()
    ex = VideoJoinAndUpload(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()


