# -*- coding: utf-8 -*-
import urllib, urllib2, re, os, sys, math,  time
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
from urlparse import urlparse, parse_qs
import urlparser, cookielib


scriptID = 'plugin.video.mrknow'
scriptname = "Filmy online www.mrknow.pl - noobroom"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, settings, Parser,libCommon, Player

log = pLog.pLog()


sort_asc = '?o=rosnaco&f=tytul'
sort_desc = '?o=malejaco&f=tytul'
playerUrl = 'http://www.youtube.pl/'

HOST = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3'

MENU_TAB = {1: "Posortowane od A-Z",
            2: "Posortowane według IMDb",
            3: "Posortowane od ostatniego",
            4: "Kategorie",
            5: "Szukaj" }
            
CAT_TAB = { 1: ["Akcja",         "genre.php?b=10000000000000000000000000"],
            2: ["Przygodowy",    "genre.php?b=01000000000000000000000000"],
            3: ["Animacja",      "genre.php?b=00100000000000000000000000"],
            4: ["Biograficzny",  "genre.php?b=00010000000000000000000000"],
            5: ["Komedia",       "genre.php?b=00001000000000000000000000"],
            6: ["Crime",         "genre.php?b=00000100000000000000000000"],
            7: ["Dokumentalny",  "genre.php?b=00000010000000000000000000"],
            8: ["Familijny",     "genre.php?b=00000001000000000000000000"],
            9: ["Fantazy",       "genre.php?b=00000000100000000000000000"],
            10:["Historyczny",   "genre.php?b=00000000000100000000000000"],
            11:["Muzyczny",      "genre.php?b=00000000000000100000000000"],
            12:["Muzykal",       "genre.php?b=00000000000000010000000000"],
            13:["Romans",        "genre.php?b=00000000000000000001000000"],
            14: ["Sci-Fi",        "genre.php?b=00000000000000000000100000"],
            15: ["Sport",         "genre.php?b=00000000000000000000010000"],
            16: ["Thiler",        "genre.php?b=00000000000000000000000100"],
            17: ["Wojenny",       "genre.php?b=00000000000000000000000010"],
            18: ["Western",       "genre.php?b=00000000000000000000000001"] }


class Noobroom:
    def __init__(self):
        log.info('Starting Noobroom')
        self.settings = settings.TVSettings()
        self.parser = Parser.Parser()
        self.cm = libCommon.common()
        noobroom_ip = ptv.getSetting('noobroom_ip')
        if noobroom_ip == '':
            self.settings.showSettings()

        self.mainUrl = 'http://'+noobroom_ip+'/'
        self.settings = settings.TVSettings()
        self.COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "noobroom.cookie"
        self.zalogowany = 0
        self.p = Player.Player()
        
    def login(self):    
        print "Zalogowany--->", self.zalogowany
        
        if len(ptv.getSetting('noobroom_user')) > 0:
            post_data = {'email': ptv.getSetting('noobroom_user'), 'password': ptv.getSetting('noobroom_pass'), 'remember':'on'}
            query_data = {'url': self.mainUrl+'login2.php', 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True}
            data = self.cm.getURLRequestData(query_data, post_data)
            if self.isLoggedIn(data) == True:
                xbmc.executebuiltin("XBMC.Notification(" + ptv.getSetting('noobroom_user') + ", Zostales poprawnie zalogowany,4000)")
                self.zalogowany = 2
            else:
                xbmc.executebuiltin("XBMC.Notification(Blad logowania, sprawdź login i hasło.,4000)")  
        else:
            query_data = { 'url': 'http://plej.tv/ajax/alert.php', 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': False, 'return_data': True }
            link = self.cm.getURLRequestData(query_data)
            xbmc.executebuiltin("XBMC.Notification(Skonfiguruj konto w ustawieniach, obecnie uzywam Player z limitami,4000)")         
            self.settings.showSettings()
            exit
    
    def isLoggedIn(self, data):
        lStr = '<li><a href="logout.php">Logout</a></li>'
        if lStr in data:
          return True
        else:
          return False

    def listsMainMenu(self, table):
        for num, val in table.items():
            self.add('noobroom', 'main-menu', val, 'None', 'None', 'None', 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def listsCategoriesMenu(self, table):
        for num, val in table.items():
            #print val[1]
            self.add('noobroom', 'categories-menu', val[0], 'None', 'None', self.mainUrl+val[1], 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getSearchURL(self, key):
        url = self.mainUrl + 'search.php?q=' + urllib.quote_plus(key) 
        return url
        
    def listsItems2(self, url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', HOST)
        openURL = urllib2.urlopen(req)
        readURL = openURL.read()
        openURL.close()
        match = re.compile("<b>(.*?)</b>(.*?)<a style='color:#fff' href='/?(.*?)'>(.*?)</a>", re.DOTALL).findall(readURL)
        print match
        if len(match) > 0:
        #http://72.8.190.49/2img/336.jpg
        #s = url.replace('?','')
            for i in range(len(match)):
                strid = match[i][0]
                strid = strid.replace('?','')

            #add(self, service, name,               category, title,     iconimage, url, desc, rating, folder = True, isPlayable = True):
                self.add('noobroom', 'playSelectedMovie', 'None', match[i][1], self.mainUrl + '2img/'+strid+'.jpg', strid, 'aaaa', 'None', True, False)
               
        xbmcplugin.endOfDirectory(int(sys.argv[1]))



    def listsItems(self, url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': True, 'cookiefile': self.COOKIEFILE, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match = re.compile("<a class='.+?' id='(.+?)' style='color:.+?' href='.+?'>(.+?)</a><br>", re.DOTALL).findall(link)
        print match
        if len(match) > 0:
            for i in range(len(match)):
                strid = match[i][0]

            #add(self, service, name,               category, title,     iconimage, url, desc, rating, folder = True, isPlayable = True):
                self.add('noobroom', 'playSelectedMovie', 'None', match[i][1], self.mainUrl + '2img/'+strid+'.jpg', strid, 'aaaa', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
    def listsItemsOther(self, url):
        query_data = { 'url': url, 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': True, 'cookiefile': self.COOKIEFILE, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match = re.compile('<a class=\'tippable\' id=\'(.*?)\' style="text-decoration:underline;color:#fff;font-family: verdana,geneva,sans-serif;" href=\'(.*?)\'>(.*?)</a>', re.DOTALL).findall(link)
        print match
        if len(match) > 0:
            for i in range(len(match)):
                strid = match[i][0]
            #add(self, service, name,               category, title,     iconimage, url, desc, rating, folder = True, isPlayable = True):
                self.add('noobroom', 'playSelectedMovie', 'None', match[i][2], self.mainUrl + '2img/'+strid+'.jpg', strid, 'aaaa', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def listsItemsPage(self, url):
        if not url.startswith("http://"):
            url = self.mainUrl + url
        if self.getSizeAllItems(url) > 0  and self.getSizeItemsPerPage(url) > 0:
            a = math.ceil(float(self.getSizeAllItems(url)) / float(self.getSizeItemsPerPage(url)))
            for i in range(int(a)):
                num = i + 1
                title = 'Lista ' + str(num)
                destUrl = url + sort_asc + '&page=' + str(num)
                self.add('noobroom', 'items-menu', 'None', title, 'None', destUrl, 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))        


    def listsItemsSerialPage(self, url, sizeOfSerialParts):
        if not url.startswith("http://"):
            url = self.mainUrl + url
        if sizeOfSerialParts > 0  and self.getSizeItemsPerPage(url) > 0:
            a = math.ceil(float(sizeOfSerialParts) / float(self.getSizeItemsPerPage(url)))
            for i in range(int(a)):
                num = i + 1
                title = 'Lista ' + str(num)
                destUrl = url + sort_asc + '&page=' + str(num)
                self.add('iptak', 'items-menu', 'None', title, 'None', destUrl, 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1])) 


    def getMovieLinkFromXML(self, url):
        #noobroom9.com/?2798
        query_data = { 'url': 'http://noobroom9.com/?'+url, 'use_host': False, 'use_cookie': True, 'save_cookie': False, 'load_cookie': True, 'cookiefile': self.COOKIEFILE, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match = re.compile('"streamer": "(.*?)",', re.DOTALL).findall(link)
        print ("Match",match, self.cm.getCookieItem(self.COOKIEFILE,'auth'))
        urlLink = 'None'
        stream_url = ''
        wybierz = ['Server 1','Serwer 2']
        d = xbmcgui.Dialog()
        item = d.select("Choose Server", wybierz)
        if item == 0:
            stream_url =  match[0]
        if item == 0:
            stream_url =  match[0].replace('loc=22','loc=15')
        mycookie = 'auth=' + self.cm.getCookieItem(self.COOKIEFILE,'auth') + '&noob=' + self.cm.getCookieItem(self.COOKIEFILE,'noob') +'&place=' + self.cm.getCookieItem(self.COOKIEFILE,'place') 
        #+ Cookie: place=1; noob=MzA2Nw%3D%3D; auth=NDMzYzAwYzUwZDc4NDA0OWRmZjY5NmVhMWEwZjlhNzU2YmI3YzdhZg%3D%3D; __PPU_CHECK=1; lvca_unique_user=1; __PPU_SESSION_c-f=Xde073,1390069022,1,1390067282X
        cj = cookielib.MozillaCookieJar()
        cj.load(self.COOKIEFILE, ignore_discard=True)
        cookiestr = ''
        for cookie in cj:
            cookiestr += '%s=%s;' % (cookie.name, cookie.value)
        fullvid = ('%s|Cookie="%s"' % (stream_url, cookiestr + "__PPU_CHECK=1; lvca_unique_user=1"))
        return fullvid
 

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
            
 

    def seekhack(self,player, url, item):
        print ("*** SEEK *** " )
        
        if url.find("start=") >= 0:
            flag, lastseek = url.split("&")[-1].split("=")
            lastseek = int(lastseek)
            if flag:
                import json
                import socket
                import select
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(("127.0.0.1", 9090))

                while player.isPlaying():
                    xbmc.sleep(1000)	
                    print "Sniffing for notifications..."
                    
                    if len(select.select([sock], [], [], 0)[0]) != 0:
                        notific_str = sock.recv(4096)
                        print ("###??", notific_str)
                        notifs = ['{"jsonrpc"' + noti for noti in notific_str.split('{"jsonrpc"')]
                        print notifs
                        for notific in notifs[1:]:
                            print ("!??", notific)
                            notific = json.loads(notific)
                            if notific["method"] == "Player.OnSeek":
                                ctime = sum(
                                        int(notific["params"]["data"]["player"]["time"][k]) * mul
                                        for k, mul in ( ("hours", 3600 ), ("minutes", 60), ("seconds", 1))
                                    )

                                seekoff = sum(
                                        int(notific["params"]["data"]["player"]["seekoffset"][k]) * mul
                                        for k, mul in ( ("hours", 3600 ), ("minutes", 60), ("seconds", 1))
                                    )
                                curtime = player.getTime()
                                alltime = player.getTotalTime()
                                print ("--- MOVIE TIME --- :",curtime,alltime)
                                #UGLY hack because going backwards can take us beyond the current played item's start time, have to provide a good default (10min)
                                if ctime < 1:
                                    seekoff = -600
                                lastseek =  int(94499*curtime)
                                #lastseek=4631466
                                if lastseek < 0:
                                    lastseek = 0
                                print ("??", lastseek)
                                #player.stop()
                                #item.setProperty("StartPercent",  "20")
                                #item.setInfo("video", {"Player.Time" :  str(seek), "VideoPlayer.Time" :  str(seek)})
                                #xbmc.sleep(8000)	
                                #player.play("&".join(url.split("&")[:-1]) + "&start={0}".format(lastseek), item)
                                player.play('http://178.159.0.10/index.php?file=1238&start=34746738&hd=0&auth=0&type=flv&tv=0|Referer=http://noobroom1.com/player.swf')
                                
                                #xbmc.sleep(8000)	
                                xbmc.executebuiltin("PlayerControl(Play)")
                            
    def play(self, url, title, icon):
        #scraper = resources.scraper.SCRAPER
        #addon	= xbmcaddon.Addon( id=ID )
        #bitrate	= int(addon.getSetting( "vid_quality" ))
        #obj,fmt		= scraper.menu_play(params["url"])
        #diff, sbitrate, url = sorted([(abs(int(sbitrate) - int(bitrate)), sbitrate, pl) for sbitrate, pl in sorted(obj.iteritems())])[0]	
        print ("using:", url)
        #item = xbmcgui.ListItem(params["name"])
        item=xbmcgui.ListItem(title, iconImage=icon, thumbnailImage=icon)
        item.setInfo( type="Video", infoLabels={ "Title": title, } )
        
        player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        player.play(url, item)
        
        xbmc.sleep(4000)	
        #xbmc.executebuiltin("PlayerControl(Play)")
        self.seekhack(player, url, item)

    def handleService(self):
    	params = self.parser.getParams()
        name = self.parser.getParam(params, "name")
        category = self.parser.getParam(params, "category")
        url = self.parser.getParam(params, "url")
        title = self.parser.getParam(params, "title")
        icon = self.parser.getParam(params, "icon")
        if name == None:
            self.login()
            self.listsMainMenu(MENU_TAB)
        elif name == 'main-menu' and category == 'Posortowane od A-Z':
            log.info('Ordered by A-Z: ')
            self.listsItems(self.mainUrl + 'azlist.php')

        elif name == 'main-menu' and category == 'Posortowane według IMDb':
            log.info('Ordered by IMDb Rating: ')
            self.listsItems(self.mainUrl + 'rating.php')
        elif name == 'main-menu' and category == 'Posortowane od ostatniego':
            log.info('Ordered by latest: ')
            self.listsItemsOther(self.mainUrl + 'latest.php')
        elif name == 'main-menu' and category == 'Kategorie':
            log.info('Ordered by latest: ')
            self.listsCategoriesMenu(CAT_TAB)
#listsCategoriesMenu

            
        elif name == 'main-menu' and category == "Szukaj":
            key = self.searchInputText()
            self.listsItemsOther(self.getSearchURL(key))
        elif name == 'categories-menu' and category != 'None':
            log.info('url: ' + str(url))
            self.listsItems(url)
        if name == 'playSelectedMovie':
            self.p.LOAD_AND_PLAY_VIDEO(self.getMovieLinkFromXML(url), title, icon)
            #self.play(self.getMovieLinkFromXML(url), title, icon)

        
  
