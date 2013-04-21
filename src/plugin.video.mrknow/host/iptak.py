# -*- coding: utf-8 -*-
import urllib, urllib2, re, os, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
from urlparse import urlparse, parse_qs
import urlparser
import urlparse


scriptID = 'plugin.video.mrknow'
scriptname = "Filmy online www.mrknow.pl - iptak"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, settings, Parser, pCommon

log = pLog.pLog()

mainUrl = 'http://iptak.pl/'
sort_asc = '?o=rosnaco&f=tytul'
sort_desc = '?o=malejaco&f=tytul'
playerUrl = 'http://www.youtube.pl/'

HOST = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:19.0) Gecko/20121213 Firefox/19.0'

MENU_TAB = {1: "Nowości",
            2: "Kategorie", 
            3: "Szukaj" }


class IPTAK:
    def __init__(self):
        log.info('Starting IPTAK')
        #self.settings = settings.TVSettings()
        #self.parser = Parser.Parser()
        self.up = urlparser.urlparser()
        self.cm = pCommon.common()
        self.parser = Parser.Parser()
        self.up = urlparser.urlparser()
        self.page = ""



    def listsMainMenu(self, table):
        for num, val in table.items():
            self.add('iptak', 'main-menu', val, 'None', 'None', 'None', 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def listsCategoriesMenu(self):
        req = urllib2.Request(mainUrl)
        req.add_header('User-Agent', HOST)
        openURL = urllib2.urlopen(req)
        readURL = openURL.read()
        openURL.close()
        match = re.compile('<div id="category">(.*?)</ul>', re.DOTALL).findall(readURL)
        match1 = re.compile('<h5>(.*?)</h5>', re.DOTALL).findall(match[0])
        match2 = re.compile('<a(.*?)href="(.*?)">', re.DOTALL).findall(match[0])
        
        if len(match1) > 0:
            log.info('Listuje kategorie: ')
            for i in range(len(match1)):
                self.add('iptak', 'categories-menu', match1[i].strip(), 'None', 'None', match2[i][1], 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getSearchURL(self, key):
        url = mainUrl + '/kategoria/szukaj?s=' + urllib.quote_plus(key) 
        return url
        #req = urllib2.Request(url)
        #req.add_header('User-Agent', HOST)
        #openURL = urllib2.urlopen(req)
        #readURL = openURL.read()
        

    def listsItems(self, url,page):
        print('page:',page,url)
        query_data = { 'url': url+page, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        readURL = self.cm.getURLRequestData(query_data)
        match1 = re.compile('<div id="item"(.*?)><a title="(.*?)" href="(.*?)"><img src="(.*?)" height="(.*?)" width="(.*?)" alt="(.*?)"/><h6>(.*?)</h6></a>',re.DOTALL).findall(readURL)
        print ("NBN",readURL)
        if len(match1) > 0:
            for i in range(len(match1)):
                #add(self, service, name,               category, title,     iconimage, url, desc, rating, folder = True, isPlayable = True):
                self.add('iptak', 'playSelectedMovie', 'None', match1[i][1], match1[i][3], match1[i][2], 'aaaa', 'None', True, False)
        match2 = re.compile('<div style="width:640px; font-size: 18px;" id="stronicowanie">(.*?)</div>' ,re.DOTALL).findall(readURL)
        print ("ZZZ",match2)
        if len(match2)>0:
            match3 = re.compile('<a href="(.*?)">(.*?)</a>',re.UNICODE).findall(match2[0])
            print ("ZZZ",match3)
            newpage = match3[-1][0].replace('./','')
            print ("ZZZ11",newpage,page)
            if len(match3)>0 and newpage != page:
                log.info('Nastepna strona: '+ match3[-1][0])
                self.add('iptak', 'categories-menu', 'Następna Strona', 'None', 'None', url, 'None', 'None', True, False, newpage)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def listsItemsN(self, url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        readURL = self.cm.getURLRequestData(query_data)
        match = re.compile('ci</h3>(.*?)<div id="footer">',re.DOTALL).findall(readURL)
        print match
        if len(match) > 0:
            match1 = re.compile('<a href="(.*?)" title="(.*?)"><img height="(.*?)" width="(.*?)" alt="(.*?)" src="(.*?)"/><h6>(.*?)</h6></a>',re.DOTALL).findall(match[0])
            print match1
            if len(match1) > 0:
                for i in range(len(match1)):
                    okladka = match1[i][5].replace('mala','srednia').replace('../../..','')
                #add(self, service, name,               category, title,     iconimage, url, desc, rating, folder = True, isPlayable = True):
                    self.add('iptak', 'playSelectedMovie', 'None', match1[i][1], mainUrl+okladka, match1[i][0], 'aaaa', 'None', True, False)

        xbmcplugin.endOfDirectory(int(sys.argv[1])) 



    def getMovieLinkFromXML(self, url):
        print ("URL XML", url)
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match = re.compile('{playMovie\("(.*?)","(.*?)"\)', re.DOTALL).findall(link)
        print ("A1",match)
        if len(match) > 0:
            if match[0][1] == 'cda':
                linkVideo = self.up.getVideoLink('http://www.cda.pl/video/'+match[0][0])
            elif match[0][1] == 'yt':
                linkVideo = self.up.getVideoLink('http://www.youtube.com/watch?v='+match[0][0])
            else:
                linkVideo = False
            return linkVideo
        else:
            return False
        return linkVideo
        
  

    def searchInputText(self):
        text = None
        k = xbmc.Keyboard()
        k.doModal()
        if (k.isConfirmed()):
            text = k.getText()
        return text
    

    def add(self, service, name, category, title, iconimage, url, desc, rating, folder = True, isPlayable = True,page = ''):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category + "&title=" + title + "&url=" + urllib.quote_plus(url) + "&icon=" + urllib.quote_plus(iconimage)+ "&page=" + urllib.quote_plus(page)
        #log.info(str(u))
        if name == 'main-menu' or name == 'categories-menu':
            title = category 
        if iconimage == '':
            iconimage = "DefaultVideo.png"
        liz=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        if isPlayable:
            liz.setProperty("IsPlayable", "true")
        liz.setInfo( type="Video", infoLabels={ "Title": title } )
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
            

    def LOAD_AND_PLAY_VIDEO(self, videoUrl, title, icon):
        ok=True
        if videoUrl == '':
                d = xbmcgui.Dialog()
                d.ok('Nie znaleziono streamingu.', 'Może to chwilowa awaria.', 'Spróbuj ponownie za jakiś czas')
                return False
        liz=xbmcgui.ListItem(title, iconImage=icon, thumbnailImage=icon)
        liz.setInfo( type="Video", infoLabels={ "Title": title, } )
        try:
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(videoUrl, liz)
            
            if not xbmc.Player().isPlaying():
                xbmc.sleep( 10000 )
                #xbmcPlayer.play(url, liz)
            
        except:
            d = xbmcgui.Dialog()
            d.ok('Błąd przy przetwarzaniu.', 'Problem')        
        return ok


    def handleService(self):
    	params = self.parser.getParams()
        name = self.parser.getParam(params, "name")
        category = self.parser.getParam(params, "category")
        url = self.parser.getParam(params, "url")
        title = self.parser.getParam(params, "title")
        icon = self.parser.getParam(params, "icon")
        page = self.parser.getParam(params, "page") 
        if page ==None:
            page=''
        
        if name == None:
            self.listsMainMenu(MENU_TAB)
        elif name == 'main-menu' and category == 'Kategorie':
            log.info('Jest Kategoria: ' + str(url))
            self.listsCategoriesMenu()
        elif name == 'main-menu' and category == 'Nowości':
            log.info('Jest Nowości: ')
            self.listsItemsN(mainUrl)
            
        elif name == 'main-menu' and category == "Szukaj":
            key = self.searchInputText()
            self.listsItems(self.getSearchURL(key),page)
        elif name == 'categories-menu' and category != 'None':
            log.info('url: ' + str(url))
            self.listsItems(url,page)
        if name == 'playSelectedMovie':
            log.info('playSelectedMovie: ' + str(url))
            self.LOAD_AND_PLAY_VIDEO(self.getMovieLinkFromXML(url), title, icon)

        
  
