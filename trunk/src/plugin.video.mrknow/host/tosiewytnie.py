# -*- coding: utf-8 -*-
import urllib, urllib2, re, os, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
import cookielib
from urlparse import urlparse, parse_qs
import urlresolver
from cookielib import CookieJar


scriptID = 'plugin.video.mrknow'
scriptname = "Filmy online www.mrknow.pl - tosiewytnie"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, settings, Parser

log = pLog.pLog()

mainUrl = 'http://tosiewytnie.pl/'
polecane = 'mindex.html'
sort_desc = '?o=malejaco&f=tytul'
playerUrl = 'http://www.youtube.pl/'

HOST = 'Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B176 Safari/7534.48.3'
cj = cookielib.CookieJar()


MENU_TAB = {1: "Polecane",
            2: "Rankingi - Najpopularniejsze",
            3: "Rankingi - Najnowsze",
            4: "Rankingi - Najczęściej komentowane",
            5: "Rankingi - Najgorsze",
            6: "Kanały - Najnowsze",
            7: "Kanały - Alfabetycznie",
            8: "Kanały - Najpopularniejsze",
            9: "Kanały - Ilość produkcji"}
    #        10: "Szukaj"}

class MyHTTPErrorProcessor(urllib2.HTTPErrorProcessor):

    def http_response(self, request, response):
        code, msg, hdrs = response.code, response.msg, response.info()

        if not (200 <= code < 300):
            response = self.parent.error(
                'http', request, response, code, msg, hdrs)
        return response

    https_response = http_response


               
class ToSieWytnie:
    def __init__(self):
        log.info('Starting ToSieWytnie')
        self.settings = settings.TVSettings()
        self.parser = Parser.Parser()


    def listsMainMenu(self, table):
        for num, val in table.items():
            self.add('tosiewytnie', 'main-menu', val, val, 'None', 'None', 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def pageadditemscat(self, data,category):
        match = re.compile('<div class="clip"><a href="(.*?)" class="title"><img class="preview" src="(.*?)" alt="" />(.*?)</a><br/>(.*?): (.*?)<br/><img src="(.*?)" alt="(.*?)"/>').findall(data)
        if len(match) > 0:
            for i in range(len(match)):
                opis = match[i][2] + ' - ilość produkcji:'+ match[i][4]
                url =  mainUrl + match[i][0]
                self.add('tosiewytnie', 'categories-menu', category, opis , match[i][1], url, '', 'None', True, False)

    def listsCategoriesMenu(self,url,category=''):
        newurl = url
        nrstrony = 0 
        while (nrstrony < 3):
            urldata = self.pagedo(newurl)
            self.pageadditemscat(urldata,category)
            geturl = self.pageafindnext(urldata)
            if len(geturl) > 0:
                newurl = mainUrl + geturl[0]
                nrstrony = nrstrony +1
            else:
                nrstrony = 4
        if nrstrony == 3:
           #service=tosiewytnie&name=categories-menu&category=Kanały
           self.add('tosiewytnie', 'main-menu', category, 'Następna strona', 'None', newurl, 'None', 'None', True, False)
                
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        
    def pagedo(self,url):
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), MyHTTPErrorProcessor)
        opener.addheaders = [('User-agent', HOST)]
        urllib2.install_opener(opener)
        page = urllib2.urlopen('http://tosiewytnie.pl/accepted,1,mindex.html')
        page = urllib2.urlopen(url)
        response =  page.read()
        page.close()
        return response
    def pageadditems(self, data):
        match = re.compile('<div class="clip"><a href="(.*?)" class="title"><img class="preview" src="(.*?)" alt="" />(.*?)</a><br/>(.*?)<br/><div class="saw"><img src="(.*?)" alt="(.*?)"/></div><br/><br/><a href="(.*?)">').findall(data)
        if len(match) > 0:
            for i in range(len(match)):
                self.add('tosiewytnie', 'playSelectedMovie', 'None', match[i][2], match[i][1], match[i][0], '', 'None', True, False)
 
    def pageafindnext(self, data):
        match = re.compile('<a class="next" href="(.*?)">Następne</a>').findall(data)
        
        return match
           
        
    def listsItems(self, url,category=''):
        newurl = url
        nrstrony = 0 
        while (nrstrony < 3):
            urldata = self.pagedo(newurl)
            self.pageadditems(urldata)
            geturl = self.pageafindnext(urldata)
            if len(geturl) > 0:
                newurl = mainUrl + geturl[0]
                nrstrony = nrstrony +1
            else:
                nrstrony = 4
        if nrstrony == 3:
           self.add('tosiewytnie', 'categories-menu', category, 'Następna strona', 'None', newurl, 'None', 'None', True, False)
                
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def getMovieLink(self, url):
        urlLink = 'None'
        url = mainUrl + url
        urldata = self.pagedo(url)
        match = re.compile('<div class="clip"><a href="(.*?)">').findall(urldata)
        return match[0]

    def searchInputText(self):
        text = None
        k = xbmc.Keyboard()
        k.doModal()
        if (k.isConfirmed()):
            text = k.getText()
        return text
    

    def add(self, service, name, category, title, iconimage, url, desc, rating, folder = True, isPlayable = True):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category + "&title=" + title + "&url=" + urllib.quote_plus(url) + "&icon=" + urllib.quote_plus(iconimage)
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
        elif name == 'main-menu' and category == 'Polecane':
            log.info(category)
            self.listsItems('http://tosiewytnie.pl/mindex.html',category)
        elif name == 'main-menu' and category == 'Rankingi - Najpopularniejsze':
            log.info(category)
            self.listsItems('http://tosiewytnie.pl/mrankingi.html',category)
        elif name == 'main-menu' and category == 'Rankingi - Najnowsze':
            log.info(category)
            self.listsItems('http://tosiewytnie.pl/type,new,mrankingi.html',category)

        elif name == 'main-menu' and category == 'Rankingi - Najczęściej komentowane':
            log.info(category)
            self.listsItems('http://tosiewytnie.pl/type,comment,mrankingi.html',category)

        elif name == 'main-menu' and category == 'Rankingi - Najgorsze':
            log.info(category)
            self.listsItems('http://tosiewytnie.pl/type,worst,mrankingi.html',category)
            
        elif name == 'main-menu' and category == 'Kanały - Najnowsze':
            if url == 'None':
                url = 'http://tosiewytnie.pl/mkanaly.html'
            self.listsCategoriesMenu(url,category)

        elif name == 'main-menu' and category == 'Kanały - Alfabetycznie':
            if url == 'None':
                url = 'http://tosiewytnie.pl/type,4,mkanaly.html'
            self.listsCategoriesMenu(url,category)

        elif name == 'main-menu' and category == 'Kanały - Najpopularniejsze':
            if url == 'None':
                url = 'http://tosiewytnie.pl/type,1,mkanaly.html'
            self.listsCategoriesMenu(url,category)

        elif name == 'main-menu' and category == 'Kanały - Ilość produkcji':
            if url == 'None':
                url = 'http://tosiewytnie.pl/type,3,mkanaly.html'
            self.listsCategoriesMenu(url,category)
        
        elif name == 'categories-menu' and category != 'None':
            log.info('url: ' + str(url))
            self.listsItems(url)
        if name == 'playSelectedMovie':
            self.LOAD_AND_PLAY_VIDEO(self.getMovieLink(url), title, icon)

        
  
