# -*- coding: utf-8 -*-
import cookielib, os, string, StringIO
import os, time, base64, logging, calendar
import urllib, urllib2, re, sys, math
import xbmcaddon, xbmc, xbmcgui, simplejson
import urlparse, httplib, random, string

scriptID = 'plugin.video.mrknow'
scriptname = "Wtyczka XBMC www.mrknow.pl"
ptv = xbmcaddon.Addon(scriptID)

import pLog, Parser, settings, pCommon, urlparser


log = pLog.pLog()
sets = settings.TVSettings()


class pageparser:
  def __init__(self):
    self.cm = pCommon.common()
    self.up = urlparser.urlparser()
    


  def hostSelect(self, v):
    hostUrl = False
    d = xbmcgui.Dialog()
    if len(v) > 0:
      valTab = []
      for i in range(len(v)):
	valTab.append(str(i+1) + '. ' + self.getHostName(v[i], True))
      item = d.select("Wybor hostingu", valTab)
      if item >= 0: hostUrl = v[item]
    else: d.ok ('Brak linkow','Przykro nam, ale nie znalezlismy zadnego linku do video.', 'Sproboj ponownie za jakis czas')
    return hostUrl


  def getHostName(self, url, nameOnly = False):
    hostName = ''       
    match = re.search('http://(.+?)/',url)
    if match:
      hostName = match.group(1)
      if (nameOnly):
	n = hostName.split('.')
	hostName = n[-2]
    return hostName


  def getVideoLink(self, url):
    nUrl=''
    host = self.getHostName(url)
    log.info("video hosted by: " + host)
    log.info(url)
    
    #if host == 'livemecz.com':
    #    nUrl = self.livemecz(url)
    #    print "Self",nUrl
    if host == 'www.drhtv.com.pl':
        nUrl = self.drhtv(url)
    elif host == 'www.realtv.com.pl':
        nUrl = self.realtv(url)
    elif host == 'www.transmisje.info':
        nUrl = self.transmisjeinfo(url)
    elif host == '79.96.137.217' or host == 'http://178.216.200.26':
        nUrl = self.azap(url)
    elif host == 'bbpolska.webd.pl':
        nUrl = self.bbpolska(url)
    elif host == 'fotosend.pl':
        nUrl = self.azap(url)
        
    elif nUrl  == '':
        print "Jedziemy na ELSE - "+  nUrl
        nUrl = self.pageanalyze(url,host)
    print ("Link:",nUrl)
    return nUrl

    
  def azap(self,url):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    print link
    match1=re.compile('<meta http-equiv="Refresh" content="(.*?); url=(.*?)" />').findall(link)
    if len(match1)>0:
        url = match1[0][1]
        print ("m",match1)
        query_data = { 'url': match1[0][1], 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match=re.compile('file: "(.*?)"').findall(link)
        match1=re.compile("file: '(.*?)'").findall(link)
        print ("m",link)
        print ("m",match)
        print ("Match",url,match,link)
        if len(match)>0:
            return match[0]
        elif len(match1)>0:
            return match1[0]
        
    else:
        return self.pageanalyze(match1[0])
    
  def bbpolska(self,url):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    match=re.compile('<div id="player">(.*?)</div>').findall(link)
    print match
    if len(match)>0:
        match1=re.compile('src="(.*?)"').findall(match[0])
        print match1
        return self.pageanalyze(match1[0],match1[0])
    else:
        return False
    
    match=re.compile('<iframe width="(.*?)" height="(.*?)" src="(.*?)" scrolling="no" frameborder="0" style="border: 0px none transparent;">').findall(link)
    print ("Match",match)
    return self.pageanalyze('http://www.transmisje.info'+match[0][2],'http://www.transmisje.info')
  

  def transmisjeinfo(self,url):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    match=re.compile('<iframe width="(.*?)" height="(.*?)" src="(.*?)" scrolling="no" frameborder="0" style="border: 0px none transparent;">').findall(link)
    print ("Match",match)
    return self.pageanalyze('http://www.transmisje.info'+match[0][2],'http://www.transmisje.info')

  def realtv(self,url):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    match=re.compile('<iframe frameborder="0" height="420" marginheight="0px" marginwidth="0px" name="RealTV.com.pl" scrolling="no" src="(.*?)" width="650">').findall(link)
    print ("Match",match)
    return self.pageanalyze(match[0],'http://www.realtv.com.pl')

 
  def livemecz(self,url):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    match=re.compile('<iframe frameborder="0" height="480" marginheight="0px" marginwidth="0px" name="livemecz.com" scrolling="no" src="(.+?)" width="640"></iframe>').findall(link)
    query_data = { 'url': match[0], 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    match=re.compile('<iframe marginheight="0" marginwidth="0" name="livemecz.com" src="(.*?)" frameborder="0" height="480" scrolling="no" width="640">').findall(link)
    print ("Match livemecz",match)
    videolink =  self.pageanalyze(match[0],'http://livemecz.com/')
    print ("videolink  livemecz",videolink)
    return videolink

  def drhtv(self,url):
    return self.pageanalyze(url,url)

  def pageanalyze(self,url,referer=''):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    match=re.compile('<script type="text/javascript"> channel="(.*?)"; width="(.*?)"; height="(.*?)";</script><script type="text/javascript" src="http://yukons.net/share.js"></script>').findall(link)
    match1=re.compile("<script type='text/javascript'>fid='(.*?)'; v_width=(.*?); v_height=(.*?);</script><script type='text/javascript' src='http://www.reyhq.com/player.js'></script>").findall(link)
    match2=re.compile("<script type='text/javascript' src='http://www.sawlive.tv/embed/(.*?)'>").findall(link)
    match3=re.compile("<script type='text/javascript' src='http://sawlive.tv/embed/(.*?)'>").findall(link)
    match4=re.compile('<script type="text/javascript" src="http://www.ilive.to/embed/(.*?)&width=640&height=400&autoplay=true">').findall(link)
    match5=re.compile("<script type='text/javascript'> channel='(.*?)'; user='(.*?)'; width='640'; height='400';</script><script type='text/javascript' src='http://jimey.tv/player/jimeytv_embed.js'>").findall(link)
    match6=re.compile("<script type='text/javascript'> width=(.*?), height=(.*?), channel='(.*?)', e='(.*?)';</script><script type='text/javascript' src='http://www.mips.tv/content/scripts/mipsEmbed.js'>").findall(link)
    match7=re.compile('<script type="text/javascript">fid="(.*?)"; v_width=(.*?); v_height=(.*?);</script><script type="text/javascript" src="http://www.ukcast.tv/embed.js"></script>').findall(link)
    match8=re.compile('<script type="text/javascript"> channel="(.*?)"; vwidth="(.*?)"; vheight="(.*?)";</script><script type="text/javascript" src="http://castamp.com/embed.js"></script>').findall(link)
    match9=re.compile("<script type='text/javascript'>id='(.*?)'; width='(.*?)'; height='(.*?)';</script><script type='text/javascript' src='http://liveview365.tv/js/player.js'></script>").findall(link)
    match10=re.compile('<script type="text/javascript"> channel="(.*?)"; width="(.*?)"; height="(.*?)";</script>\r\n<script type="text/javascript" src="http://yukons.net/share.js"></script>').findall(link)
    match11=re.compile('<iframe width="600px" height="400px" scrolling="no" frameborder="0" src="http://www.putlive.in/(.*?)"></iframe>').findall(link)
    match12=re.compile('<iframe frameborder=0 marginheight=0 marginwidth=0 scrolling=\'no\'src="(.*?)" width="(.*?)" height="(.*?)">').findall(link)
    match13=re.compile("<script type='text/javascript'> width=640, height=480, channel='(.*?)', g='(.*?)';</script><script type='text/javascript' src='http://www.ucaster.eu/static/scripts/ucaster.js'></script>").findall(link)
    match14=re.compile("<script type='text/javascript'>fid='(.*?)'; v_width=(.*?); v_height=(.*?);</script><script type='text/javascript' src='http://www.flashwiz.tv/player.js'></script>").findall(link)
    
    #print ("link",link)
    
    print ("Match",match8,match2,match1,match,match3,match4,match5)
    if len(match) > 0:
        return self.up.getVideoLink('http://yukons.net/'+match[0][0])
    elif len(match1) > 0:
        return self.up.getVideoLink('http://www.reyhq.com/'+match1[0][0])
    elif len(match2) > 0:
        print ("Match2",match2)
        return self.up.getVideoLink('http://www.sawlive.tv/embed/'+match2[0],url)
    elif len(match3) > 0:
        return self.up.getVideoLink('http://www.sawlive.tv/embed/'+match3[0],url)
    elif len(match4) > 0:
        print ("Match4",match4)
        return self.up.getVideoLink('http://www.ilive.to/embed/'+match4[0],referer)
    elif len(match6) > 0:
        print ("Match6",match6[0])
        return self.up.getVideoLink('http://mips.tv/embedplayer/'+match6[0][2]+'/'+match6[0][3]+'/'+match6[0][0]+'/'+match6[0][1])
    elif len(match7) > 0:
        print ("Match7",match7)
        return self.up.getVideoLink('http://www.ukcast.tv/embed.php?u='+match7[0][0]+'&amp;vw='+match7[0][1]+'&amp;vh='+match7[0][2])
    elif len(match8) > 0:
        print ("Match8",match8)
        return self.up.getVideoLink('http://castamp.com/embed.php?c='+match8[0][0]+'&ch=1',referer)
    elif len(match9) > 0:
        print ("Match9",match9)
        return self.up.getVideoLink('http://liveview365.tv/embedded?id='+match9[0][0],referer)
    elif len(match10) > 0:
        print ("Match10",match10)
        return self.up.getVideoLink('http://yukons.net/'+match10[0][0])
    elif len(match11) > 0:
        print ("Match11",'http://www.putlive.in/'+match11[0])
        return self.up.getVideoLink('http://www.putlive.in/'+match11[0],referer)
    elif len(match12) > 0:
        print ("Match12",match12)
        return self.up.getVideoLink(match12[0][0])
    elif len(match13) > 0:
        print ("Match13",match13)
        return self.up.getVideoLink('http://www.ucaster.eu/embedded/'+match13[0][0]+'/'+match13[0][1]+'/400/480',referer)
    elif len(match14) > 0:
        print ("Match14",match14)
        return self.up.getVideoLink('http://www.flashwiz.tv/embed.php?live='+match14[0][0]+'&vw='+match14[0][1]+'&vh='+match14[0][2],referer)


    else:
        return False





          
