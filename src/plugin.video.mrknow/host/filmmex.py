# -*- coding: utf-8 -*-
import urllib, urllib2, re, os, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
from urlparse import urlparse, parse_qs
import urlparser


scriptID = 'plugin.video.mrknow'
scriptname = "Filmy online www.mrknow.pl - filmmex"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, settings, Parser,pCommon

log = pLog.pLog()

mainUrl = 'http://filmmex.pl/'

HOST = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3'

MENU_TAB = {5: "Gorące",
            6: "Kategorie",
            10: "Data dodania",
            12: "Data premiery",
            13: "Oglądalność",
            14: "Oceny",
            15: "Alfabetycznie"
            }


class filmmex:
    def __init__(self):
        log.info('Starting filmmex.pl')
        self.settings = settings.TVSettings()
        self.parser = Parser.Parser()
        self.up = urlparser.urlparser()
        self.cm = pCommon.common()



    def listsMainMenu(self, table):
        for num, val in table.items():
            self.add('filmmex', 'main-menu', val, 'None', 'None', 'None', 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def listsCategoriesMenu(self):
        query_data = { 'url': 'http://filmmex.pl/kategorie.html', 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }        
        link = self.cm.getURLRequestData(query_data)
        match = re.compile('<div class="leftMenu">(.*?)<span>Wersja</span>', re.DOTALL).findall(link)
        match1 = re.compile('<a href="(.*?)">(.*?)</a> ', re.DOTALL).findall(match[0])
        print match
        print match1
        #<a href="filmy,Akcja.html">Akcja</a> 
        
        if len(match1) > 0:
            log.info('Listuje kategorie: ')
            for i in range(len(match1)):
                url = mainUrl + match1[i][0].replace('.html','')
                print url
                self.add('filmmex', 'categories-menu', match1[i][1].strip(), 'None', 'None', url, 'None', 'None', True, False,'0','sort_field=data-dodania&sort_method=asc')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getSearchURL(self, key):
        url = mainUrl + 'search.php?phrase=' + urllib.quote_plus(key) 
        return url
        #req = urllib2.Request(url)
        #req.add_header('User-Agent', HOST)
        #openURL = urllib2.urlopen(req)
        #readURL = openURL.read()
        
    def listsItemsOther(self, url):
        #http://filmmex.pl/kategorie,0,wszystkie,wszystkie,1900-2013,.html?sort_field=data-dodania&sort_method=asc
        #urllink = url + ',' + str(strona) + ',wszystkie,wszystkie,1900-2013,.html?' + filtrowanie
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }        
        link = self.cm.getURLRequestData(query_data)
        match = re.compile('<div class="mostPopular movies hotMovies">(.*?)<div class="newMovies movies_r">', re.DOTALL).findall(link)
        match1 = re.compile('<li>\n                        <div class="poster" style="background:url\(\'(.*?)\'\) no-repeat 11px 0px"></div>\n                        <div class="title">\n                            <h2><a href="(.*?)" title="(.*?)">(.*?)</a></h2>', re.DOTALL).findall(match[0])
        print match1
        if len(match1) > 0:
            for i in range(len(match1)):
                data = self.cm.getURLRequestData({ 'url': mainUrl+ match1[i][1], 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True })
                if (data.find('http://filmmex.pl/static/img/niedostepny.jpg')) == -1:
                    #add(self, service, name,               category, title,     iconimage, url, desc, rating, folder = True, isPlayable = True):
                    self.add('filmmex', 'playSelectedMovie', 'None', match1[i][3],  match1[i][0].replace('_small',''), mainUrl+ match1[i][1], 'aaaa', 'None', True, False)

        xbmcplugin.endOfDirectory(int(sys.argv[1]))

        
    def listsItems(self, url, strona='0', filtrowanie=''):
        print strona
        print filtrowanie
        #http://filmmex.pl/kategorie,0,wszystkie,wszystkie,1900-2013,.html?sort_field=data-dodania&sort_method=asc
        urllink = url + ',' + str(strona) + ',wszystkie,wszystkie,1900-2013,.html?' + filtrowanie
        print urllink
        query_data = { 'url': urllink, 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }        
        link = self.cm.getURLRequestData(query_data)
        match = re.compile('<div class="moviesWrap">(.*?)<footer>', re.DOTALL).findall(link)
        match1 = re.compile('<li data-movie_url="(.*?)">\r\n            <img class="poster" src="(.*?)" alt="(.*?)" />\r\n            <div class="title">\r\n                <h2><a title="(.*?)" href="(.*?)">(.*?)</a></h2>', re.DOTALL).findall(match[0])
        if len(match1) > 0:
            for i in range(len(match1)):
                data = self.cm.getURLRequestData({ 'url': mainUrl+ match1[i][0], 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True })
                if (data.find('http://filmmex.pl/static/img/niedostepny.jpg')) == -1:
                    #add(self, service, name,               category, title,     iconimage, url, desc, rating, folder = True, isPlayable = True):
                    self.add('filmmex', 'playSelectedMovie', 'None', match1[i][5],  match1[i][1].replace('_small',''), mainUrl+ match1[i][0], 'aaaa', 'None', True, False)
        #urllink = url + ',' + str((int(strona)+1)) + ',wszystkie,wszystkie,1900-2013,.html?' + filtrowanie
        log.info('Nastepna strona: '+  urllink)
        self.add('filmmex', 'categories-menu', 'Następna', 'None', 'None', url, 'None', 'None', True, False,str(int(strona) + 1), filtrowanie)
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
                self.add('filmmex', 'items-menu', 'None', title, 'None', destUrl, 'None', 'None', True, False)
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
                self.add('filmmex', 'items-menu', 'None', title, 'None', destUrl, 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1])) 


    def getMovieLinkFromXML(self, url):
        HOST = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3'
        query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match1 = re.compile('<ul class="players" style="float:right;width:200px;height:27px;overflow:hidden">(.*?)</ul>', re.DOTALL).findall(link)
        match2 = re.compile('<li class="(.*?)"><a href="(.*?)">(.*?)</a></li>', re.DOTALL).findall(match1[0])
        tab = []
        tab.append("Player premium")   
        for i in range(len(match2)):
            print ("Match2",match2)
            if (match2[i][2].find('div')) > -1:
                #<div class="s-quality_mid_active"></div><span>Średnia jakość</span>putlocker
                match3 = re.compile('<span>(.*?)</span>', re.DOTALL).findall(match2[i][2])
                tab.append(match3[0] + ' - ' + match2[i][2].split('</span>')[1]) 
            else:
                tab.append(match2[i][2])           
        d = xbmcgui.Dialog()        
        video_menu = d.select("Wybór playera ...", tab)
        print ("video_menu",video_menu)
        if video_menu != "" and video_menu==0:
            url = mainUrl + match2[0][1] + '&premium'
            print "premium", url
            query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
            link = self.cm.getURLRequestData(query_data)
            match1 = re.compile('clip: {\r\n                    url: \'(.*?)\',', re.DOTALL).findall(link)
            return match1[0]
            
        if video_menu != "" and video_menu>=1:
            video_menu = video_menu-1
            print match2
            print ("AAAAAA",match2[video_menu][1])
            url = mainUrl + match2[video_menu][1] + '&standard'
            query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
            link = self.cm.getURLRequestData(query_data)
            match1 = re.compile('<iframe src="(.*?)" width="(.*?)" height="(.*?)" frameborder="0" scrolling="no"></iframe>', re.DOTALL).findall(link)
            linkVideo = ''
            if len(match1)==0:
                match1 = re.compile('<iframe src="(.*?)" style="(.*?)" scrolling="no"></iframe>', re.DOTALL).findall(link)
                print ("1",match1)
            if len(match1)==0:
                match1 = re.compile('<iframe src="(.*?)" style="(.*?)" frameborder="0" scrolling="no"></iframe>', re.DOTALL).findall(link)
                print ("2",match1)                #
            #    
            print ("3",match1)
            if len(match1)>0:
                linkVideo = self.up.getVideoLink(match1[0][0])
                print linkVideo
                return linkVideo
            else:
                return False



    def getSizeAllItems(self, url):
        numItems = 0
        req = urllib2.Request(url)
        req.add_header('User-Agent', HOST)
        openURL = urllib2.urlopen(req)
        readURL = openURL.read()
        openURL.close()
        match = re.compile('<span class="nav_ext">...</span> <a href="http://filmmex.pl/filmy/page/(.*?)/">(.*?)</a></div>(.*?)</li>', re.DOTALL).findall(readURL)
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
    

    def add(self, service, name, category, title, iconimage, url, desc, rating, folder = True, isPlayable = True, strona = '', filtrowanie=''):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category + "&title=" + title + "&url=" + urllib.quote_plus(url) + "&icon=" + urllib.quote_plus(iconimage)+ "&strona=" + urllib.quote_plus(strona)+ "&filtrowanie=" + urllib.quote_plus(filtrowanie)
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
        strona = self.parser.getParam(params, "strona")
        filtrowanie = self.parser.getParam(params, "filtrowanie")
        print("url",url,strona, filtrowanie)
        
        if name == None:
            self.listsMainMenu(MENU_TAB)
        elif name == 'main-menu' and category == 'Data dodania':
            log.info('Jest Wszystkie: ')
            self.listsItems('http://filmmex.pl/kategorie',0,'sort_field=data-dodania&sort_method=desc')
        elif name == 'main-menu' and category == 'Data premiery':
            log.info('Jest Wszystkie: ')
            self.listsItems('http://filmmex.pl/kategorie',0,'sort_field=data-premiery&sort_method=desc')
        elif name == 'main-menu' and category == 'Oglądalność':
            log.info('Jest Wszystkie: ')
            self.listsItems('http://filmmex.pl/kategorie',0,'sort_field=odslony&sort_method=desc')
        elif name == 'main-menu' and category == 'Oceny':
            log.info('Jest Wszystkie: ')
            self.listsItems('http://filmmex.pl/kategorie',0,'sort_field=ocena&sort_method=desc')
        elif name == 'main-menu' and category == 'Alfabetycznie':
            log.info('Jest Wszystkie: ')
            self.listsItems('http://filmmex.pl/kategorie',0,'sort_field=alfabetycznie&sort_method=desc')
        elif name == 'main-menu' and category == 'Gorące':
            log.info('Jest Gorące: ')
            self.listsItemsOther('http://filmmex.pl/')
        elif name == 'main-menu' and category == 'Kategorie':
            log.info('Jest Gorące: ')
            self.listsCategoriesMenu()
 

            
        elif name == 'main-menu' and category == "Szukaj":
            key = self.searchInputText()
            self.listsItems(self.getSearchURL(key))
        elif name == 'categories-menu' and category != 'None':
            log.info('url: ' + str(url))
            self.listsItems(url,strona,filtrowanie)
        if name == 'playSelectedMovie':
            self.LOAD_AND_PLAY_VIDEO(self.getMovieLinkFromXML(url), title, icon)

        
  
