# -*- coding: utf-8 -*-
import urllib, urllib2, re, os, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
from urlparse import urlparse, parse_qs
import pageparser
import string


scriptID = 'plugin.video.mrknow'
scriptname = "Wtyczka XBMC www.mrknow.pl - meczyki"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, settings, Parser,pCommon

log = pLog.pLog()

mainUrl = 'http://www.meczyki.pl'

HOST = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3'

MENU_TAB = {1: "Dzisiaj",
            2: "Jutro",
            3: "Pojutrze",
            12: "Filmiki" }


class MECZYKI:
    def __init__(self):
        log.info('Starting meczyki.pl')
        self.settings = settings.TVSettings()
        self.parser = Parser.Parser()
        self.up = pageparser.pageparser()
        self.cm = pCommon.common()
        

    def listsMainMenu(self, table):
        for num, val in table.items():
            self.add('meczyki', 'main-menu', val, 'None', 'None', 'None', 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def listsCategoriesMenu(self,url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        readURL = self.cm.getURLRequestData(query_data)
        match = re.compile('<div class="transmission" id="(.*?)">(.*?)</table>', re.DOTALL).findall(readURL)
        for i in range(len(match)):
            #print ("Ile",i)
            match1 = re.compile('<div class="name">(.*?)<a href="(.*?)">(.*?)</a>', re.DOTALL).findall(match[i][1])
            match2 = re.compile('<div class="time" style="float: left;">(.*?)</div>', re.DOTALL).findall(match[i][1])
            #match1 = re.compile('<div class="transmission" id="(.*?)">(.*?)</table>', re.DOTALL).findall(readURL)
            #print match1
            if len(match1) > 0:
                p = re.compile(r'<.*?>')
                tytul = match2[0] + ' ' + ' '.join(str(match1[0][2]).translate(None, string.whitespace[:5]).split())
                tytul =  p.sub('', tytul)
                tytul = tytul.replace("&nbsp;", "")
                self.add('meczyki', 'categories-menu', tytul, 'None', 'None', mainUrl+ match1[0][1], 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getSearchURL(self, key):
        url = mainUrl + 'search.php?phrase=' + urllib.quote_plus(key) 
        return url
        #req = urllib2.Request(url)
        #req.add_header('User-Agent', HOST)
        #openURL = urllib2.urlopen(req)
        #readURL = openURL.read()
        

    def listsItems(self, url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', HOST)
        openURL = urllib2.urlopen(req)
        readURL = openURL.read()
        openURL.close()
        match = re.compile('<td class="flag">(.*?)</tr>', re.DOTALL).findall(readURL)
#        print ("Match", match)
        valTab = [] 
        strTab = [] 
        for i in range(len(match)):
            #print ("Ile",i)
            match1 = re.compile('href="(.*?)"', re.DOTALL).findall(match[i])
            match2 = re.compile('<img src="(.*?)" /></td>\n                <td class="channel">\n                    <span class="channel_name">(.*?)</span>', re.DOTALL).findall(match[i])
            match3 = re.compile('<td class="desc">(.*?)</td>', re.DOTALL).findall(match[i])
#            print ("A",match[i])
#            print ("2",match2)
#            print ("1",match1)
#            print ("3",match3)
            tytul =  match3[0] + ' - ' + match2[0][1]
            tytul = tytul.replace('&nbsp;','').replace('WWW','').replace('\n','').replace(' ','')
            link = match1[0].replace(' ','').replace('\n','')
            #print("AAAA|",link)
            if len(match1) > 0 and len(match3[0].replace('&nbsp;','').replace('WWW','').replace('\n','').replace(' ',''))>0:
                jadymy = True
                print tytul
                if tytul.find('Meczyki') >-1:
                    jadymy = False
                if tytul.find('PREMIUM') >-1:
                    jadymy = False
                if tytul.find('Derbymecz') >-1:
                    jadymy = False
                if tytul.find('Sopcast') >-1:
                    jadymy = False
            
                if jadymy==True:
                    strTab.append(tytul)
                    strTab.append(mainUrl+match2[0][0])
                    strTab.append(link)
                    valTab.append(strTab)
                    strTab = []
                    valTab.sort(key = lambda x: x[0], reverse=True)
        for i in valTab:
            self.add('meczyki', 'playSelectedMovie', 'None', i[0], i[1], i[2], 'None', 'None', True, False)
           #self.add('meczyki', 'playSelectedMovie', 'None',tytul , mainUrl+match2[0][0], match1[0], 'aaaa', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def listsItemsPage(self, url):
        if not url.startswith("http://"):
            url = mainUrl + url
        if self.getSizeAllItems(url) > 0  and self.getSizeItemsPerPage(url) > 0:
            a = math.ceil(float(self.getSizeAllItems(url)) / float(self.getSizeItemsPerPage(url)))
            for i in range(int(a)):
                num = i + 1
                title = 'Lista ' + str(num)
                destUrl = url + sort_asc + '&page=' + str(num)
                self.add('meczyki', 'items-menu', 'None', title, 'None', destUrl, 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))        


    def listsItemsSerialPage(self, url, sizeOfSerialParts):
        if not url.startswith("http://"):
            url = mainUrl + url
        if sizeOfSerialParts > 0  and self.getSizeItemsPerPage(url) > 0:
            a = math.ceil(float(sizeOfSerialParts) / float(self.getSizeItemsPerPage(url)))
            for i in range(int(a)):
                num = i + 1
                title = 'Lista ' + str(num)
                destUrl = url + sort_asc + '&page=' + str(num)
                self.add('meczyki', 'items-menu', 'None', title, 'None', destUrl, 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1])) 


    def getMovieLinkFromXML(self, url):
        linkVideo = self.up.getVideoLink(url)
        return linkVideo


    def getSizeAllItems(self, url):
        numItems = 0
        req = urllib2.Request(url)
        req.add_header('User-Agent', HOST)
        openURL = urllib2.urlopen(req)
        readURL = openURL.read()
        openURL.close()
        match = re.compile('<li data-theme="c" action="watch">(.*?)<a href="(.*?)" data-transition="slide">(.*?)<img src="(.*?)" height="90px" width="90px" title="(.*?)" />(.*?)</a>(.*?)</li>', re.DOTALL).findall(readURL)
        if len(match) == 1:
            numItems = match[0]
        return numItems
    
    
    def getSizeItemsPerPage(self, url):
        numItemsPerPage = 0
        openURL = urllib.urlopen(url)
        readURL = openURL.read()
        openURL.close()
        match = re.compile('<div class="movie-(.+?)>').findall(readURL)
        if len(match) > 0:
            numItemsPerPage = len(match)
        return numItemsPerPage        

    def getMovieID(self, url):
        id = 0
        tabID = url.split(',')
        if len(tabID) > 0:
            id = tabID[1]
        return id


    def getItemTitles(self, table):
        out = []
        for i in range(len(table)):
            value = table[i]
            out.append(value[1])
        return out

    def getItemURL(self, table, key):
        link = ''
        for i in range(len(table)):
            value = table[i]
            if key in value[0]:
                link = value[2]
                break
        return link


    def searchInputText(self):
        text = None
        k = xbmc.Keyboard()
        k.doModal()
        if (k.isConfirmed()):
            text = k.getText()
        return text
    

    def add(self, service, name, category, title, iconimage, url, desc, rating, folder = True, isPlayable = True):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category + "&title=" + title + "&url=" + urllib.quote_plus(url) + "&icon=" + urllib.quote_plus(iconimage)
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
        if name == None:
            self.listsMainMenu(MENU_TAB)
        elif name == 'main-menu' and category == 'Dzisiaj':
            log.info('Jest Dzisiaj: ')
            self.listsCategoriesMenu('http://www.meczyki.pl/')
        elif name == 'main-menu' and category == 'Jutro':
            log.info('Jest Dzisiaj: ')
            self.listsCategoriesMenu('http://www.meczyki.pl/jutro,1,dzien.html')
        elif name == 'main-menu' and category == 'Pojutrze':
            log.info('Jest Dzisiaj: ')
            self.listsCategoriesMenu('http://www.meczyki.pl/pojutrze,2,dzien.html')
            
        elif name == 'main-menu' and category == "Szukaj":
            key = self.searchInputText()
            self.listsItems(self.getSearchURL(key))
        elif name == 'categories-menu' and category != 'None':
            log.info('url: ' + str(url))
            self.listsItems(url)
        if name == 'playSelectedMovie':
            self.LOAD_AND_PLAY_VIDEO(self.getMovieLinkFromXML(url), title, icon)

        
  
