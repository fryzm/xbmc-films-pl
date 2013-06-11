# -*- coding: utf-8 -*-
import urllib, urllib2, re, os, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
from urlparse import urlparse, parse_qs
import urlparser,json


scriptID = 'plugin.video.mrknow'
scriptname = "Filmy online www.mrknow.pl - kinoliveseriale"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, settings, Parser,pCommon

log = pLog.pLog()

mainUrl = 'http://alekino.tv/'
catUrl = 'http://alekino.tv/seriale_online/'

HOST = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3'

MENU_TAB = {0: "Alfabetycznie",
            1: "Top 30",
            2: "Ostatnie dodane seriale",
            3: "Ostatnie dodane odcinki"
#            12: "Kategorie",
#            15: "Szukaj"
            }

class kinoliveseriale:
    def __init__(self):
        log.info('Starting kinoliveseriale.pl')
        self.settings = settings.TVSettings()
        self.parser = Parser.Parser()
        self.up = urlparser.urlparser()
        self.cm = pCommon.common()
        self.COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "kinoliveseriale.cookie"
        query_data = {'url': 'http://alekino.tv/login', 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': False, 'return_data': True}
        data = self.cm.getURLRequestData(query_data)

    def getstring(self,data):
        data = data.replace('\xe5\x9a','Ś')
        data = data.replace('\xe5\x81','Ł')
        return data
        
    def listsMainMenu(self, table):
        for num, val in table.items():
            self.add('kinoliveseriale', 'main-menu', val, 'None', 'None', 'None', 'None', 'None', True, False)
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
                self.add('kinoliveseriale', 'categories-menu', match1[i][1].strip(), 'None', 'None', catUrl, 'None', 'None', True, False,'1','kat='+match1[i][0])
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
                        self.add('kinoliveseriale', 'playSelectedMovie', 'None', match1[i][3],  match1[i][0], mainUrl+ match1[i][2], 'aaaa', 'None', True, False)

            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
    def listsItems(self, url,strona):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }        
        link = self.cm.getURLRequestData(query_data)
        match = re.compile('<span class="pl-titleblock">Sezon'+strona+'</span>(.*?)</ul>', re.DOTALL).findall(link)
        match2 = re.compile('<meta property="og:image" content="(.*?)" />', re.DOTALL).findall(link)
        match1 = re.compile('<li>\n\t\t\t\t\t<a href="(.*?)"(.*?)><span>(.*?)</span>(.*?)\n\t\t\t\t\t\t\t\t\t\t</a>\n\t\t\t\t</li>', re.DOTALL).findall(match[0])
#        match3 = re.compile('<li>\n\t\t\t\t\t<a href="/seriale_online/(.*?)" style="background:#616161;"><span>(.*?)</span>(.*?)\n\t\t\t\t\t\t\t\t\t\t<span style="color:red;position:absolute;margin-top:-0px;margin-left:2px;">new</span>\n\t\t\t\t\t\t\t\t\t\t</a>\n\t\t\t\t</li>', re.DOTALL).findall(match[0])
        print ("Link",link)
        print ("Link",match1)
        
        if len(match1) > 0:
            for i in range(len(match1)):
                title = match1[i][2]+match1[i][3].replace('<span style="color:red;position:absolute;margin-top:-0px;margin-left:2px;">new</span>',' - [NOWY]')
                self.add('kinoliveseriale', 'playSelectedMovie', 'None', title.replace('\n',''), match2[0], mainUrl+ match1[i][0], 'aaaa', 'None', True, False)
#        if len(match3) > 0:
#            for i in range(len(match3)):
#                    self.add('kinoliveseriale', 'playSelectedMovie', 'None', match3[i][1] + match3[i][2], match2[0], mainUrl+ match3[i][0], 'aaaa', 'None', True, False)
        
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def listsItemsA(self, url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }        
        link = self.cm.getURLRequestData(query_data)
        match = re.compile('<div class="pl-module" id="letter_(.*?)">', re.DOTALL).findall(link)
        for i in range(len(match)):
            self.add('kinoliveseriale', 'page-menu', 'None',  match[i].decode('iso-8859-2'),  'None', mainUrl, 'aaaa', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def listsItemsS(self, url, strona):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }        
        link = self.cm.getURLRequestData(query_data)
        match = re.compile('<div class="pl-module" id="letter_'+str.lower(strona)+'">(.*?)</ul>', re.DOTALL).findall(link)
        match1 = re.compile('<li><a href="(.*?)" class="pl-corners">(.*?)</a></li>', re.DOTALL).findall(match[0])
        print match1
        if len(match1) > 0:
            for i in range(len(match1)):
                title = match1[i][1].replace('<span style="color:red;position:absolute;margin-top:-0px;margin-left:2px;">new</span>','')
                self.add('kinoliveseriale', 'serial-menu', 'None', title,  'None', mainUrl+ match1[i][0], 'aaaa', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
    def listsItemsTop(self, url,str1,str2):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }        
        link = self.cm.getURLRequestData(query_data)
        match = re.compile(str1+'(.*?)'+str2, re.DOTALL).findall(link)
        match1 = re.compile('<a href="(.*?)" title="(.*?)" class="useTooltip" style="width:180px;"><img src="(.*?)" alt=""(.*?)/></a>', re.DOTALL).findall(match[0])
        if len(match1) > 0:
            for i in range(len(match1)):
                title = match1[i][1].replace('<span style="color:red;position:absolute;margin-top:-0px;margin-left:2px;">new</span>','')
                self.add('kinoliveseriale', 'serial-menu', 'None', title,  match1[i][2], mainUrl+ match1[i][0], 'aaaa', 'None', True, False,'',match1[i][2])
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
                    self.add('kinoliveseriale', 'playSelectedMovie', 'None', match2[0] + match4[j][1],  match3[0], mainUrl+ match4[j][0], 'aaaa', 'None', True, False,'',match1[i][2])
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
                self.add('kinoliveseriale', 'items-menu', 'None', title, 'None', destUrl, 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))        


    def listsSeasons(self, url,img):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': True, 'return_data': True }        
        link = self.cm.getURLRequestData(query_data)
        match = re.compile('<span class="pl-titleblock">Sezon(.*?)</span>', re.DOTALL).findall(link)
        print match
        if img == '' or img ==None:
            img = 'None'
        for i in range(len(match)):
            self.add('kinoliveseriale', 'items-menu', 'None',  'Sezon'+match[i],  img, url, 'None', 'None', True, False,match[i])
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
 
    def getMovieLinkFromXML(self, url):
        HOST = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3'
        query_data = { 'url': url, 'use_host': True, 'host': HOST, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match1 = re.compile('<input type="hidden" name="currentmirrorload" value="(.*?)"', re.DOTALL).findall(link)
        #match2 = re.compile('{ serial: "(.*?)", source: (.*?), token:"(.*?)", time:"(.*?)"}', re.DOTALL).findall(link)
        match2 = re.compile('{ serial: "(.*?)", source:(.*?), token:"(.*?)", time:"(.*?)"}', re.DOTALL).findall(link)
        #{serial:"54999",source:$('input[name=currentmirrorload]').val(),token:"3fc31a090e88126951d230552d982730",time:"1370467193"},function(data)
        #        #{ video: "21710", source: $('input[name=currentmirrorload]').val(), token:"d057f6157b594762b1b972cd48fe1861", time:"1370953147"}, function(data)

        print ("M2",match2)
        post_data = {'serial': match2[0][0], 'source': match1[0], 'token': match2[0][2], 'time': match2[0][3]}
        query_data = {'url': 'http://alekino.tv/players?timer='+match2[0][3], 'use_host': False, 'use_cookie': True, 'save_cookie': False, 'load_cookie': True, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True}
        data = self.cm.getURLRequestData(query_data, post_data)
        print ("D",data)
        marian = json.loads(data)
        match3 = re.compile('<iframe src="(.*?)" style="(.*?)" frameborder="0" scrolling="no"></iframe>', re.DOTALL).findall(marian["player_code"])
        linkVideo = self.up.getVideoLink(match3[0][0].decode('utf8'))
        return linkVideo
        

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
        print ("DANE",url,title,strona)
        
        
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
            self.listsSeasons(url,img)
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

        
  
