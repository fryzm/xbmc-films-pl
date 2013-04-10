# -*- coding: utf-8 -*-
import urllib, urllib2, re, os, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
from urlparse import urlparse, parse_qs
import urlparser,json


scriptID = 'plugin.video.mrknow'
scriptname = "Filmy online www.mrknow.pl - scs"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, settings, Parser,pCommon

log = pLog.pLog()

mainUrl = 'http://scs.pl/'
catUrl = 'http://scs.pl/seriale.html'

HOST = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3'

MENU_TAB = {0: "Alfabetycznie",
#            1: "Top 30",
#            2: "Ostatnie dodane seriale",
#            3: "Ostatnie dodane odcinki"
#            12: "Kategorie",
#            15: "Szukaj"
            }

class scs:
    def __init__(self):
        log.info('Starting scs.pl')
        self.settings = settings.TVSettings()
        self.parser = Parser.Parser()
        self.up = urlparser.urlparser()
        self.cm = pCommon.common()
        self.COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "scs.cookie"
        query_data = {'url': 'http://scs.pl/logowanie.html', 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': False, 'return_data': True}
        data = self.cm.getURLRequestData(query_data)
        if ptv.getSetting('scs.pl_login') == 'true':
            post_data = {'email': ptv.getSetting('scs.pl_user'), 'password': ptv.getSetting('scs.pl_pass'), 'submit_login': 'Zaloguj'}
            query_data = {'url': 'http://scs.pl/logowanie.html', 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True}
            data = self.cm.getURLRequestData(query_data, post_data)

    def getstring(self,data):
        data = data.replace('\xe5\x9a','Ś')
        data = data.replace('\xe5\x81','Ł')
        return data
        
    def listsMainMenu(self, table):
        for num, val in table.items():
            self.add('scs', 'main-menu', val, 'None', 'None', 'None', 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def listsCategoriesMenu(self):
        query_data = { 'url': catUrl, 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }        
        link = self.cm.getURLRequestData(query_data)
        match = re.compile('<ul class="select-movie-type movie-kat-selection">(.*?)</ul>', re.DOTALL).findall(link)
        match1 = re.compile('<a href="#" rel="filter" type="kat" value="(.*?)" >&#9632; (.*?)</a>', re.DOTALL).findall(match[0])
        
        if len(match1) > 0:
            log.info('Listuje kategorie: ')
            for i in range(len(match1)):
                url = mainUrl + match1[i][0].replace('.html','')
                self.add('scs', 'categories-menu', match1[i][1].strip(), 'None', 'None', catUrl, 'None', 'None', True, False,'1','kat='+match1[i][0])
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getSearchURL(self, key):
        if key != None:
            url = mainUrl + '/search?search_query='+ urllib.quote_plus(key)+'&x=0&y=0'  
            return url
        else:
            return False
        #req = urllib2.Request(url)
        #req.add_header('User-Agent', HOST)
        #openURL = urllib2.urlopen(req)
        #readURL = openURL.read()
        
    def listsItemsOther(self, url):
            query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }        
            link = self.cm.getURLRequestData(query_data)
            match = re.compile('<!-- Filmy start -->(.*?)<!-- Filmy koniec -->', re.DOTALL).findall(link)
            match1 = re.compile('<img src="(.*?)" alt="film online" title="(.*?)" height="133" width="100"></a>\n                            <a href="(.*?)" class="en pl-white">(.*?)</a>', re.DOTALL).findall(match[0])
            if len(match1) > 0:
                for i in range(len(match1)):
                        #add(self, service, name,               category, title,     iconimage, url, desc, rating, folder = True, isPlayable = True):
                        self.add('scs', 'playSelectedMovie', 'None', match1[i][3],  match1[i][0], mainUrl+ match1[i][2], 'aaaa', 'None', True, False)

            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
    def listsItems(self, url,strona):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }        
        link = self.cm.getURLRequestData(query_data)
        match = re.compile('<meta itemprop="seasonNumber" content="'+strona+'">(.*?)</ul>', re.DOTALL).findall(link)
        match1 = re.compile('<img itemprop="image" src="(.*?)" alt="(.*?)">', re.DOTALL).findall(link)
        match2 = re.compile('<li itemprop="episode" itemscope itemtype="http://schema.tv/TVEpisode">(.*?)</li>', re.DOTALL).findall(match[0])
        if len(match2) > 0:
            for i in range(len(match2)):
                match3 = re.compile('<div class="green" itemprop="episodeNumber">(.*?)</div><div class="serialSeasons_text"><a title="(.*?)" class="aLink " href="(.*?)"><span itemprop="name">(.*?)</span></a>', re.DOTALL).findall(match2[i])
                if len(match3) > 0:
                    title = match3[0][0]+ '. ' + match3[0][3]
                    self.add('scs', 'playSelectedMovie', 'None', title.replace('\n',''), match1[0][0], mainUrl+ match3[0][2], 'aaaa', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def listsItemsA(self, url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }        
        link = self.cm.getURLRequestData(query_data)
        match = re.compile('<div class="serialCatName">\r\n                <h2>(.*?)</h2>\r\n            </div>', re.DOTALL).findall(link)
        for i in range(len(match)):
            self.add('scs', 'page-menu', 'None',  match[i].decode('iso-8859-2'),  'None', mainUrl, 'aaaa', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def listsItemsS(self, url, strona):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }        
        link = self.cm.getURLRequestData(query_data)
        match = re.compile('<h2>'+strona+'</h2>(.*?)<h2>', re.DOTALL).findall(link)
        match1 = re.compile('<div class="serialBox2">\r\n                            <a class="serial_green" href="(.*?)">(.*?)</a><br/>\r\n                <a class="serial_gray" href="(.*?)">(.*?)</a><br/>', re.DOTALL).findall(match[0])
        if len(match1) > 0:
            for i in range(len(match1)):
                title = match1[i][1] + ' / ' + match1[i][3]
                self.add('scs', 'serial-menu', 'None', title,  'None', mainUrl+ match1[i][0], 'aaaa', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
    def listsItemsTop(self, url,str1,str2):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }        
        link = self.cm.getURLRequestData(query_data)
        match = re.compile(str1+'(.*?)'+str2, re.DOTALL).findall(link)
        match1 = re.compile('<a href="(.*?)" title="(.*?)" class="useTooltip" style="width:180px;"><img src="(.*?)" alt=""(.*?)/></a>', re.DOTALL).findall(match[0])
        if len(match1) > 0:
            for i in range(len(match1)):
                title = match1[i][1].replace('<span style="color:red;position:absolute;margin-top:-0px;margin-left:2px;">new</span>','')
                self.add('scs', 'serial-menu', 'None', title,  match1[i][2], mainUrl+ match1[i][0], 'aaaa', 'None', True, False,'',match1[i][2])
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def listsItemsOst(self, url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }        
        link = self.cm.getURLRequestData(query_data)
        match = re.compile('Ostatnie dodane odcinki(.*?)Najwyżej oceniane seriale', re.DOTALL).findall(link)
        match1 = re.compile('<div class="pl-serial-mini-module">(.*?)</ul>', re.DOTALL).findall(match[0])
        if len(match1) > 0:
            for i in range(len(match1)):
                match2 = re.compile('<div class="serial-title">(.*?)</div>', re.DOTALL).findall(match1[i])
                match3 = re.compile('<div class="serial-image"><img src="(.*?)" width="68" height="90" alt="" /></div>', re.DOTALL).findall(match1[i])
                match4 = re.compile('<li><a href="(.*?)">(.*?)</a></li>', re.DOTALL).findall(match1[i])
                for j in range(len(match4)):
                    self.add('scs', 'playSelectedMovie', 'None', match2[0] + match4[j][1],  match3[0], mainUrl+ match4[j][0], 'aaaa', 'None', True, False,'',match1[i][2])
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
                self.add('scs', 'items-menu', 'None', title, 'None', destUrl, 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))        


    def listsSeasons(self, url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }        
        link = self.cm.getURLRequestData(query_data)
        match = re.compile('<meta itemprop="seasonNumber" content="(.*?)">', re.DOTALL).findall(link)
        match1 = re.compile('<img itemprop="image" src="(.*?)" alt="(.*?)">', re.DOTALL).findall(link)
        for i in range(len(match)):
            self.add('scs', 'items-menu', 'None',  'Sezon '+match[i],  match1[0][0], url, 'None', 'None', True, False,match[i])
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
 
    def getMovieLinkFromXML(self, url):
        HOST = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3'
        query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match1 = re.compile('<input type="hidden" name="currentmirrorload" value="(.*?)"', re.DOTALL).findall(link)
        match2 = re.compile('c\[(.*?)\] = "(.*?)"; ccc\[(.*?)\] = "(.*?)"; cd\[(.*?)\] = "(.*?)"; ci\[(.*?)\] = "(.*?)"; cccc\[(.*?)\] = "(.*?)";', re.DOTALL).findall(link)
        tab = []
        match4 = []
        for i in range(len(match2)):
            post_data = {'f': match2[i][1]}
 #           query_data = {'url': 'http://scs.pl/getVideo.html', 'use_host': False, 'use_cookie': True, 'save_cookie': False, 'load_cookie': True, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True}
            query_data = {'url': 'http://scs.pl/getVideo.html', 'use_host': False, 'use_cookie': False, 'save_cookie': False, 'use_post': True, 'return_data': True}
            data = self.cm.getURLRequestData(query_data, post_data)
            match3 = re.compile('<iframe src="(.*?)" (.*?)></iframe>', re.DOTALL).findall(data)
            if len(match3)>0:
                tab.append('Wideo  - ' + self.up.getHostName(match3[0][0]))
                match4.append(match3[0][0])
        if ptv.getSetting('scs.pl_login') == 'true':
                    match5 = re.compile('data: "f=(.*?)",', re.DOTALL).findall(data)
                    post_data = {'f': match5[1]}
                    query_data = {'url': 'http://scs.pl/getVideo.html', 'use_host': False, 'use_cookie': True, 'save_cookie': False, 'load_cookie': True, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True}
                    data = self.cm.getURLRequestData(query_data, post_data)
                    match6 = re.compile("url: '(.*?)',", re.DOTALL).findall(data)
                    tab.append('Wideo  - Premium')
                    match4.append(match6[0])
        d = xbmcgui.Dialog()        
        video_menu = d.select("Wybór jakości video", tab)
        if video_menu != "":
            url = match4[video_menu]
            return self.up.getVideoLink(url)

    def searchInputText(self):
        text = None
        k = xbmc.Keyboard()
        k.doModal()
        if (k.isConfirmed()):
            text = k.getText()
        return text
    

    def add(self, service, name, category, title, iconimage, url, desc, rating, folder = True, isPlayable = True, strona = '', img = ''):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category + "&title=" + title + "&url=" + urllib.quote_plus(url) + "&icon=" + urllib.quote_plus(iconimage)+ "&strona=" + urllib.quote_plus(strona)+ "&img=" + urllib.quote_plus(img)
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
        liz.setInfo( type = "Video", infoLabels={ "Title": title, } )
        try:
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(videoUrl+'|Referer=http://kinolive.pl/media/player.swf', liz)
            
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
        img = self.parser.getParam(params, "img")
        #print ("DANE",url,title,strona)
        
        
        if name == None:
            self.listsMainMenu(MENU_TAB)
        elif name == 'main-menu' and category == 'Alfabetycznie':
            log.info('Jest Alfabetycznie: ')
            self.listsItemsA(catUrl)
        elif name == 'page-menu' and category == 'None':
            log.info('Jest Alfabetycznie Litera: '+ title)
            self.listsItemsS(catUrl,title)
        elif name == 'serial-menu' and category == 'None':
            log.info('Jest Serial Menu: ')
            self.listsSeasons(url)
        elif name == 'items-menu' and category == 'None':
            log.info('Jest Sezon: '+strona)
            self.listsItems(url,strona)
        elif name == 'main-menu' and category == 'Top 30':
            log.info('Jest Top 30: ')
            self.listsItemsTop(catUrl,'TOP 30','Ostatnie dodane seriale')
        elif name == 'main-menu' and category == 'Ostatnie dodane seriale':
            self.listsItemsTop(catUrl,'Ostatnie dodane seriale', 'Ostatnie dodane odcinki')
        elif name == 'main-menu' and category == 'Ostatnie dodane odcinki':
            log.info('Jest Gorące: ')
            self.listsItemsOst(catUrl)
        elif name == 'main-menu' and category == "Szukaj":
            key = self.searchInputText()
            if key != None:
                self.listsItemsOther(self.getSearchURL(key))
        elif name == 'categories-menu' and category != 'None':
            log.info('url: ' + str(url))
            self.listsItems(url,strona,filtrowanie)
        if name == 'playSelectedMovie':
            self.LOAD_AND_PLAY_VIDEO(self.getMovieLinkFromXML(url), title, icon)

        
  
