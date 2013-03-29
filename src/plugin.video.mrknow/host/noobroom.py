# -*- coding: utf-8 -*-
import urllib, urllib2, re, os, sys, math,  time
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
from urlparse import urlparse, parse_qs
import urlparser


scriptID = 'plugin.video.mrknow'
scriptname = "Filmy online www.mrknow.pl - noobroom"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, settings, Parser

log = pLog.pLog()


sort_asc = '?o=rosnaco&f=tytul'
sort_desc = '?o=malejaco&f=tytul'
playerUrl = 'http://www.youtube.pl/'

HOST = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3'

MENU_TAB = {1: "Ordered by A-Z",
            2: "Ordered by IMDb Rating",
            3: "Ordered by latest",
            4: "Search  - broken..." }


class Noobroom:
    def __init__(self):
        log.info('Starting Noobroom')
        self.settings = settings.TVSettings()
        self.parser = Parser.Parser()
        noobroom_ip = ptv.getSetting('noobroom_ip')
        if noobroom_ip == '':
            self.settings.showSettings()

        self.mainUrl = 'http://'+noobroom_ip+'/'


    def listsMainMenu(self, table):
        for num, val in table.items():
            self.add('noobroom', 'main-menu', val, 'None', 'None', 'None', 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def listsCategoriesMenu(self):
        req = urllib2.Request(self.mainUrl)
        req.add_header('User-Agent', HOST)
        openURL = urllib2.urlopen(req)
        readURL = openURL.read()
        openURL.close()
        match = re.compile("<a href='/?(.*?)'>(.*?)</a>", re.DOTALL).findall(readURL)
        print len(match)
        print match
        
        if len(match) > 0:
            log.info('Listuje kategorie: ')
            for i in range(len(match)):
                url = self.mainUrl + match[i][0]
                self.add('noobroom', 'categories-menu', match[i][1].strip(), 'None', 'None', url, 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getSearchURL(self, key):
        url = self.mainUrl + 'search.php?phrase=' + urllib.quote_plus(key) 
        return url
        #req = urllib2.Request(url)
        #req.add_header('User-Agent', HOST)
        #openURL = urllib2.urlopen(req)
        #readURL = openURL.read()
        
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
        req = urllib2.Request(url)
        req.add_header('User-Agent', HOST)
        openURL = urllib2.urlopen(req)
        readURL = openURL.read()
        openURL.close()
        match = re.compile("<a class='.+?' id='(.+?)' style='color:.+?' href='.+?'>(.+?)</a><br>", re.DOTALL).findall(readURL)
        print match
        if len(match) > 0:
            for i in range(len(match)):
                strid = match[i][0]

            #add(self, service, name,               category, title,     iconimage, url, desc, rating, folder = True, isPlayable = True):
                self.add('noobroom', 'playSelectedMovie', 'None', match[i][1], self.mainUrl + '2img/'+strid+'.jpg', strid, 'aaaa', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
    def listsItemsOther(self, url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', HOST)
        openURL = urllib2.urlopen(req)
        readURL = openURL.read()
        openURL.close()
        match = re.compile("""<a class='.+?' id='(.+?)' style="text-decoration:underline;color:.+?;" href='.+?'>(.+?)</a><br>""", re.DOTALL).findall(readURL)
        print match
        if len(match) > 0:
            for i in range(len(match)):
                strid = match[i][0]

            #add(self, service, name,               category, title,     iconimage, url, desc, rating, folder = True, isPlayable = True):
                self.add('noobroom', 'playSelectedMovie', 'None', match[i][1], self.mainUrl + '2img/'+strid+'.jpg', strid, 'aaaa', 'None', True, False)
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
        urlLink = 'None'
        stream_url = ''
        print url 
        wybierz = ['Server 1', 'Server 2', 'Server 3']
#        wybierz = ['Server 1']
        d = xbmcgui.Dialog()
        item = d.select("Choose Server", wybierz)
        if item == 0:
            stream_url =  self.mainUrl+ '/fork.php?type=flv&auth=0&loc=15&hd=0&tv=0&file='+url
        elif item == 1:
            stream_url =  self.mainUrl+ '/fork.php?type=flv&auth=0&loc=12&hd=0&tv=0&file='+url
        elif item == 2:
            stream_url =  self.mainUrl+ '/fork.php?type=flv&auth=0&loc=14&hd=0&tv=0&file='+url
        return stream_url
        

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
            xbmcPlayer.play(videoUrl+'|Referer=http://noobroom1.com/player.swf', liz )
            
        except:
            d = xbmcgui.Dialog()
            d.ok('Błąd przy przetwarzaniu.', 'Problem')        
        return ok

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
            self.listsMainMenu(MENU_TAB)
        elif name == 'main-menu' and category == 'Ordered by A-Z':
            log.info('Ordered by A-Z: ')
            self.listsItems(self.mainUrl + 'azlist.php')

        elif name == 'main-menu' and category == 'Ordered by IMDb Rating':
            log.info('Ordered by IMDb Rating: ')
            self.listsItems(self.mainUrl + 'rating.php')
        elif name == 'main-menu' and category == 'Ordered by latest':
            log.info('Ordered by latest: ')
            self.listsItemsOther(self.mainUrl + 'latest.php')
#
            
        elif name == 'main-menu' and category == "Szukaj":
            key = self.searchInputText()
            self.listsItems(self.getSearchURL(key))
        elif name == 'categories-menu' and category != 'None':
            log.info('url: ' + str(url))
            self.listsItems(url)
        if name == 'playSelectedMovie':
            self.LOAD_AND_PLAY_VIDEO(self.getMovieLinkFromXML(url), title, icon)
            #self.play(self.getMovieLinkFromXML(url), title, icon)

        
  
