# -*- coding: utf-8 -*-
import urllib, urllib2, re, os, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
from urlparse import urlparse, parse_qs
import urlparser,httplib
import xml.etree.ElementTree as ET
import json

scriptID = 'plugin.video.mrknow'
scriptname = "Filmy online www.mrknow.pl - filmboxmoovie"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, pCommon, Parser,Player

log = pLog.pLog()

mainUrl = 'http://pl.filmboxlive.com/'
catUrl = 'http://api.invideous.com/plugin/get_package_videos?package_id=12&publisher_id=5842&records_per_page=50&filter_by_live=0&custom_order_by_order_priority=asc&custom_filter_by_genre='
#chanels = 'http://www.filmboxliveapp.com/channel/channels_pl.json'
#playerUrl = 'http://www.youtube.pl/'

HOST = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3'

MENU_TAB = {1: "Wszystkie",
            3: "Szukaj" }


class filmboxmoovie:
    def __init__(self):
        log.info('Starting filmboxmoovie.pl')
        self.cm = pCommon.common()
        self.parser = Parser.Parser()
        self.up = urlparser.urlparser()
        self.p = Player.Player()


    def listsMainMenu(self, table):
        for num, val in table.items():
            self.add('filmboxmoovie', 'main-menu', val, 'None', 'None', 'None', 'None', 'None', True, False)

        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def listsCategoriesMenu(self):
        req = urllib2.Request('http://www.filmboxliveapp.net/mobilev2/ios/AppConfig_pl.xml')
        req.add_header('User-Agent', HOST)
        openURL = urllib2.urlopen(req)
        readURL = openURL.read()
        openURL.close()
        match = re.compile('<el name="Kategorie">(.*?)</el>', re.DOTALL).findall(readURL)
        match1 = re.compile('<el name="(.*?)" type="movie" action="custom_filter_by_genre" value="(.*?)" package="(.*?)"/>', re.DOTALL).findall(match[0])

        #Niestandardowe Kategorie
        self.add('filmboxmoovie', 'categories-menu', 'Wszystkie Filmy', 'None', 'None', 'http://api.invideous.com/plugin/get_package_videos?package_id=12&publisher_id=5842&records_per_page=50&filter_by_live=0&custom_order_by_order_priority=asc&custom_filter_by_genre=Action%7CDrama%7CComedy%7CRomance%7CHorror%7CThriller%7CFamily', 'None', 'None', True, False)
        self.add('filmboxmoovie', 'categories-menu', 'Polecane', 'None', 'None', 'http://api.invideous.com/plugin/get_package_videos?package_id=12&publisher_id=5842&records_per_page=30&filter_by_live=0&custom_order_by_order_priority=asc&custom_filter_by_genre=recommended', 'None', 'None', True, False)
        query_data = { 'url': 'http://admin.filmboxliveapp.com/GetList?ctr=poland', 'use_host': False, 'use_cookie': False,  'use_post': False,'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match11 = re.compile('"latestvideos":\[(.*?)\]', re.DOTALL).findall(link)
        match12 = re.compile('"mostwatched":\[(.*?)\]', re.DOTALL).findall(link)
        self.add('filmboxmoovie', 'categories-menu', 'Nowości', 'None', 'None', 'http://api.invideous.com/plugin/get_videos_details?videos='+match11[0]+'&publisher_id=5842', 'None', 'None', True, False)
        self.add('filmboxmoovie', 'categories-menu', 'Wybór redakcji', 'None', 'None', 'http://api.invideous.com/plugin/get_videos_details?videos='+match12[0]+'&publisher_id=5842', 'None', 'None', True, False)
        
        #Szukaj
        self.add('filmboxmoovie', 'main-menu', 'Szukaj', 'None', 'None', 'http://api.invideous.com/plugin/get_package_videos?package_id=12&publisher_id=5842&filter_by_live=0&records_per_page=50&filter_by_title=', 'None', 'None', True, False)
        
        if len(match1) > 0:
            log.info('Listuje kategorie: ')
            match2 = re.compile('<option label="(.*?)" value="(.*?)">(.*?)</option>', re.DOTALL).findall(match[0])
            for i in range(len(match1)):
            #http://api.invideous.com/plugin/get_package_videos?package_id=12&publisher_id=5842&records_per_page=30&page=1&filter_by_live=0&custom_order_by_order_priority=asc&custom_filter_by_genre=Comedy

                self.add('filmboxmoovie', 'categories-menu', match1[i][0].strip(), 'None', 'None', catUrl+match1[i][1], 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getSearchURL(self, key):
        url = mainUrl + 'search.php?phrase=' + urllib.quote_plus(key) 
        return url
        #req = urllib2.Request(url)
        #req.add_header('User-Agent', HOST)
        #openURL = urllib2.urlopen(req)
        #readURL = openURL.read()
        

    def listsItems(self, url,strona='1'):
        
        self.COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "filmboxmoovie.cookie"
        print ("Strona",strona)
        url1 = url + '&page=' + strona
        query_data = { 'url': url1, 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True }
        #postdata = {'page' : strona, 'package' : 'UltimatePackage', 'genre' : category, 'sort' : 'created_at', 'records_per_page' : '30', 'live' : '0',}
        link = self.cm.getURLRequestData(query_data)
        objs = json.loads(link)
        #print ("Link",objs)
        #match1 = re.compile('<div class="movie-box">\r\n        <div>\r\n            <a href="(.*?)" class="play">\r\n            Odtw\xc3\xb3rz film</a>\r\n            <img src="(.*?)" alt="(.*?)" />\r\n', re.DOTALL).findall(link)
        #match1 = re.compile('<div class="film">\r\n\t\t\t<div class="caption" onclick="location.href=\'(.*?)\'">(.*?)</div>\r\n\t\t\t\r\n            <img src="(.*?)" alt="(.*?)" />', re.DOTALL).findall(link)
        #if len(match1) > 0:
        #    for i in range(len(match1)):
        #        match2 = re.compile('/video/details/(.*?)/(.*?)/auto', re.DOTALL).findall(match1[i][0])
        #        self.add('filmboxmoovie', 'playSelectedMovie', 'None', match1[i][1], match1[i][2], mainUrl + '/video/details/' +match2[0][0], 'aaaa', 'None', True, False)
        for o in objs['response']['result']['videos']:
            #print ("O",o)
            self.add('filmboxmoovie', 'playSelectedMovie', 'None', o['title'], o['custom_attributes']['largeImage'], o['source_url'], 'aaaa', 'None', True, False)

        self.add('filmboxmoovie', 'categories-menu', 'Następna', 'None', 'None', url, 'None', 'None', True, False,str(int(strona)+1))
        
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
                self.add('filmboxmoovie', 'items-menu', 'None', title, 'None', destUrl, 'None', 'None', True, False)
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
                self.add('filmboxmoovie', 'items-menu', 'None', title, 'None', destUrl, 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1])) 


    def getMovieLinkFromXML(self, url):
        VideoData = {}
        self.COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "filmboxmoovie.cookie"
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }        
        link = self.cm.getURLRequestData(query_data)
        VideoData['year'] = self.getMovieYear(link)
        VideoData['desc'] = self.getMovieDesc(link)
        
        match = re.compile('<embed width="(.*?)" height="(.*?)" src="(.*?)" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" wmode="transparent" flashvars="(.*?)">', re.DOTALL).findall(link)
        matchswf = re.compile('<param value="(.*?)" name="movie">', re.DOTALL).findall(link)
        movieurl = url
        params = match[0][3].split('&amp;')
        params = params[2].replace('config=','').replace('%26','&')
        movieid = self.parser.getParams(params)
        query_data = { 'url': params, 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)

        tree = ET.fromstring(link)
        p = tree.find('FlashVars').text
        params = self.parser.getParams(p)
        data = '<ume:Request xmlns:ume="http://external.unicornmedia.com/"><ume:RequestHeader/></ume:Request>'
        query_data = { 'url': params['apihost0'] + '/External/Application/'+params['session_appid']+'/APIHost/', 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_xml' : True, 'use_post': True, 'return_data': True , 'post_data':data}
        link = self.cm.getURLRequestData(query_data,data)
        query_data = { 'url': params['apihost0'] + '/External/Credentials/'+params['session_appid']+'/', 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': True, 'cookiefile': self.COOKIEFILE, 'use_xml' : True, 'use_post': True, 'return_data': True }
        linksec = self.cm.getURLRequestData(query_data,data)
        match = re.compile('<ume\:Hash>(.*?)</ume\:Hash>', re.DOTALL).findall(linksec)
        match1 = re.compile('<ume\:ApplicationGUID>(.*?)</ume\:ApplicationGUID>', re.DOTALL).findall(linksec)
        match2 = re.compile('<ume\:Timestamp>(.*?)</ume\:Timestamp>', re.DOTALL).findall(linksec)
        match3 = re.compile('<ume\:Token>(.*?)</ume\:Token>', re.DOTALL).findall(linksec)
        match4 = re.compile('<ume\:VisitGUID>(.*?)</ume\:VisitGUID>', re.DOTALL).findall(linksec)
        
        data = '<ume:Request xmlns:ume="http://external.unicornmedia.com/"><ume:RequestHeader><ume:Parameters><ume:Parameter><ume:Key>ApplicationGUID</ume:Key><ume:Value>'
        data = data + '<ume:Simple>'+match1[0]+'</ume:Simple></ume:Value></ume:Parameter><ume:Parameter><ume:Key>Token</ume:Key><ume:Value>'
        data = data + '<ume:Simple>'+match3[0]+'</ume:Simple></ume:Value></ume:Parameter><ume:Parameter><ume:Key>VisitGUID</ume:Key><ume:Value>'
        data = data + '<ume:Simple>'+match4[0]+'</ume:Simple></ume:Value></ume:Parameter><ume:Parameter><ume:Key>Timestamp</ume:Key><ume:Value>'
        data = data + '<ume:Simple>'+match2[0]+'</ume:Simple></ume:Value></ume:Parameter></ume:Parameters></ume:RequestHeader></ume:Request>'
        url =  '/External/MediaItem/'+movieid['view_id']+'/'
        query_data = { 'url': params['apihost0'] + '/External/Application/Session/'+match[0]+'/', 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': True, 'cookiefile': self.COOKIEFILE, 'use_xml' : True, 'use_post': True, 'return_data': True }
        linkses = self.cm.getURLRequestData(query_data,data)
        data = '<ume:Request xmlns:ume="http://external.unicornmedia.com/"><ume:RequestHeader>'
        data += '<ume:Hash>'+match[0]+'</ume:Hash><ume:Parameters><ume:Parameter><ume:Key>ApplicationGUID</ume:Key><ume:Value>'
        data += '<ume:Simple>'+match1[0]+'</ume:Simple></ume:Value></ume:Parameter><ume:Parameter><ume:Key>Token</ume:Key><ume:Value>'
        data += '<ume:Simple>'+match3[0]+'</ume:Simple></ume:Value></ume:Parameter><ume:Parameter><ume:Key>Timestamp</ume:Key><ume:Value>'
        data += '<ume:Simple>'+match2[0]+'</ume:Simple></ume:Value></ume:Parameter></ume:Parameters></ume:RequestHeader></ume:Request>'
        query_data = { 'url': params['apihost0'] + '/External/Application/Beacon/', 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': True, 'cookiefile': self.COOKIEFILE, 'use_xml' : True, 'use_post': True, 'return_data': True }
        linkses = self.cm.getURLRequestData(query_data,data)
        
        data = '<ume:Request xmlns:ume="http://external.unicornmedia.com/"><ume:RequestHeader><ume:Hash>'+match[0]+'</ume:Hash><ume:Parameters/></ume:RequestHeader></ume:Request>'
        query_data = { 'url': params['apihost0'] + '/External/MediaItem/'+movieid['view_id']+'/URLs/', 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': True, 'cookiefile': self.COOKIEFILE, 'use_xml' : True, 'use_post': True, 'return_data': True }
        linkses = self.cm.getURLRequestData(query_data,data)
        match5 = re.compile('<ume\:URL>(.*?)</ume\:URL>', re.DOTALL).findall(linkses)
        link = match5[0] + ' swfUrl=' + matchswf[0] + ' pageUrl='+movieurl+' swfVfy=true'
        VideoData['link'] = link
        return VideoData

    def getMovieYear(self,link):
        match = re.compile('<li><strong>Rok:</strong> (.*?)</li>', re.DOTALL).findall(link)
        print match
        return match[0]

    def getMovieDesc(self,link):
        match = re.compile('<h3 class="ttl-section">Opis</h3>\r\n(.*?)<ul class="list-lines">', re.DOTALL).findall(link)
        print match
        return match[0]
    
        
    def getpage(self,host,url,data, referer='http://cdn7.unicornapp.com/customer/nexeven/swf/UnicornOSMFPlayer-1.3.swf'):
        conn = httplib.HTTPConnection(host)
        headers = {"Content-Type": "text/xml","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:19.0) Gecko/20100101 Firefox/19.0","Content-Length": "%d" % len(data),"Referer":referer}
        conn.request("POST", url, "", headers)
        conn.send(data)
        response = conn.getresponse()
        conn.close()
        return response.read()
        
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
    

    def add(self, service, name, category, title, iconimage, url, desc, rating, folder = True, isPlayable = True,strona='1'):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category + "&title=" + title + "&url=" + urllib.quote_plus(url) + "&icon=" + urllib.quote_plus(iconimage)+ "&strona=" + urllib.quote_plus(strona)
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
        print("Dane",url)
        
        if name == None:
            #self.listsMainMenu(MENU_TAB)
            self.listsCategoriesMenu()
            
        elif name == 'main-menu' and category == 'Wszystkie':
            log.info('Jest Wszystkie: ')
            self.listsItems('http://www.filmboxliveapp.net/mobilev2/ios/AppConfig_pl.xml')         
        elif name == 'main-menu' and category == "Szukaj":
            key = self.searchInputText()
            self.listsItems(url +key)
        elif name == 'categories-menu' and category != 'None':
            log.info('url: ' + str(url))
            self.listsItems(url,strona)
        if name == 'playSelectedMovie':
            #data = self.getMovieLinkFromXML(url)
            #self.p.LOAD_AND_PLAY_VIDEO(data['link'], title, icon,data['year'],data['desc'])
            self.LOAD_AND_PLAY_VIDEO(url,title,icon)
            
        if name == 'playselectedmovie':
            data = self.getMovieLinkFromXML(url)
            self.p.LOAD_AND_PLAY_VIDEO(data['link'], title, icon,data['year'],data['desc'])

        
  
