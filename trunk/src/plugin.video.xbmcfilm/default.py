# -*- coding: utf-8 -*-
import urllib, urllib2, re, sys, xbmcplugin, xbmcgui
import cookielib, os, string, cookielib, StringIO
import os, time, base64, logging, calendar
import xbmcaddon



ptv = xbmcaddon.Addon()
scriptID = ptv.getAddonInfo('id')
scriptname = ptv.getAddonInfo('name')
#dbg = ptv.getSetting('default_debug') in ('true')
ptv = xbmcaddon.Addon(scriptID)

#BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "resources" )
BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
#sys.path.append( os.path.join( ptv.getAddonInfo('path'), "host" ) )

import pLog, settings, mrknow_Parser, xbmcfilmapi, mrknow_urlparser, mrknow_Player, mrknow_pCommon
import json

log = pLog.pLog()

#my_hello_string = ptv.getLocalizedString(30300)

#mainUrl = 'http://xbmcfilm.com/'
mainUrl = 'http://127.0.0.1:5000/'

HOST = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3'

MENU_TAB = {1: ptv.getLocalizedString(30400),
            4: ptv.getLocalizedString(30401),
            2: ptv.getLocalizedString(30402),
            3: ptv.getLocalizedString(30403),
            5: ptv.getLocalizedString(30404)
            }

class xbmcfilm:

    def __init__(self):
        log.info('Starting xbmcfilm.pl')
        self.p = mrknow_Player.mrknow_Player()
        self.parser = mrknow_Parser.mrknow_Parser()
        self.up = mrknow_urlparser.mrknow_urlparser()
        #self.settings = settings.TVSettings()
        self.api = xbmcfilmapi.XbmcFilmAPI()
        self.cm = mrknow_pCommon.common()


    def chkdict(self,dict,item):
        if item not in dict.keys():
            dict[item] = ''
        if item in dict.keys() and dict[item] == None:
            dict[item] = ''
        return dict[item]


    def listsMain(self, table):
        for num, val in table.items():
            self.add('cdapl', 'main'+str(num), val, val, 'None', 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def listsMainMenu(self, id):
        data = {'id': id}
        marek = json.dumps(self.api.getcatalogs(data))
        objs = json.loads(marek)

        if "status" in objs.keys() and objs["status"] == 'fail_authenticated':
            d = xbmcgui.Dialog()
            d.ok(ptv.getLocalizedString(30010),ptv.getLocalizedString(30405))
            return False
        if id=="0":
            for o in objs["data"][0]["children"]:
                poster = self.chkdict(o,'poster')
                self.add('cdapl', 'main-menu', '[COLOR white]'+ o['title'].encode('utf-8', 'ignore') + '[/COLOR]', poster, 'None', 'None', 'None', True, False,str(o['id']))
        else:
            for o in objs["data"]:
                poster = self.chkdict(o,'poster')
                self.add('cdapl', 'main-menu', '[COLOR white]'+ o['title'].encode('utf-8', 'ignore') + '[/COLOR]', poster, 'None', 'None', 'None', True, False,str(o['id']))

        files = json.dumps(self.api.getfiles(data))
        filesobj = json.loads(files)
        for i in filesobj["data"]:
            print("I",i)
            poster = self.chkdict(i,'poster')
            plot = self.chkdict(i,'plot')
            self.add('cdapl', 'playSelectedMovie','None',i['title'] ,poster, i['url'], plot, False, False,str(i['id']))

        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
    def listsItems(self, type, dane=''):
        if dane != '':
            data = {'type': type, 'dane':dane}
        else:
            data = {'type': type}
        files = json.dumps(self.api.getfilestype(data))
        filesobj = json.loads(files)
        if "status" in filesobj.keys() and objs["status"] == 'fail_authenticated':
            d = xbmcgui.Dialog()
            d.ok(ptv.getLocalizedString(30010),ptv.getLocalizedString(30405))
            return False
        print ("Marel",files)
        print ("objs", filesobj["data"])
        for i in filesobj["data"]:
            poster = self.chkdict(i,'poster')
            plot = self.chkdict(i,'plot')
            self.add('cdapl', 'playSelectedMovie','None',i['title'].encode('utf-8', 'ignore'), poster.encode('utf-8', 'ignore'), i['url'], plot.encode('utf-8', 'ignore'), False, False,str(i['id']))
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
       
    def listsItemsFollow(self, type, dane=''):
        if dane != '':
            data = {'type': type, 'dane':dane}
        else:
            data = {'type': type}
        files = json.dumps(self.api.getfollow(data))
        filesobj = json.loads(files)
        if "status" in filesobj.keys() and objs["status"] == 'fail_authenticated':
            d = xbmcgui.Dialog()
            d.ok(ptv.getLocalizedString(30010),ptv.getLocalizedString(30405))
            return False
        if type == 'users':
            for i in filesobj["data"]:
                data2 = {'type': 'follow', 'dane':str(i['id'])}
                usercat = json.dumps(self.api.getfollow(data2))
                catobj = json.loads(usercat)
                for o in catobj["data"]:
                    print ("O",o)
                    self.add('cdapl', 'follow-cat','User','[COLOR white]'+o['title'].encode('utf-8', 'ignore') + '[/COLOR]', 'None', 'None', 'None', True, False,str(o['id']))
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def listsItemsFollowCat(self, type, dane=''):
        if dane != '':
            data = {'type': type, 'dane':dane}
        else:
            data = {'type': type}
        marek = json.dumps(self.api.getfollow(data))
        objs = json.loads(marek)
        print ("objs",objs)
        for o in objs["data"]:
            print ("o",o)
            self.add('cdapl', 'follow-cat','User','[COLOR white]'+o['title'].encode('utf-8', 'ignore') + '[/COLOR]', 'None', 'None', 'None', True, False,str(o['id']))
        data2 = {'type': type, 'dane':dane, 'pliki':True}
        files = json.dumps(self.api.getfollow(data2))
        filesobj = json.loads(files)
        for i in filesobj["data"]:
            poster = self.chkdict(i,'poster')
            plot = self.chkdict(i,'plot')
            self.add('cdapl', 'playSelectedMovie','None',i['title'].encode('utf-8', 'ignore') ,poster, i['url'], plot.encode('utf-8', 'ignore'), False, False,str(i['id']))

        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def add(self, service, name, category, title, iconimage, url, desc='', folder = True, isPlayable = True,myid = "0"):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category +\
          "&title=" + title + "&url=" + urllib.quote_plus(url) + \
          "&icon=" + urllib.quote_plus(iconimage) + "&desc=" + desc +"&myid="+myid
        #log.info(str(u))
        if name == 'main-menu' or name == 'categories-menu':
            title = category 
        if iconimage == '':
            iconimage = "DefaultVideo.png"

        liz=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        if isPlayable:
            liz.setProperty("IsPlayable", "true")
        liz.setInfo( type="Video", infoLabels={ "Title": title, "Plot": desc} )
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)

    def searchInputText(self):
        text = None
        k = xbmc.Keyboard()
        k.doModal()
        if (k.isConfirmed()):
            text = k.getText()
        return text


    def LOAD_AND_PLAY_VIDEO(self, url, title, icon,year='',plot='', id=''):
        data = {'id': id}
        self.api.getplay(data)
        progress = xbmcgui.DialogProgress()
        progress.create('Postęp', '')
        message = ptv.getLocalizedString(30406)
        progress.update( 10, "", message, "" )
        xbmc.sleep( 1000 )
        progress.update( 30, "", message, "" )
        progress.update( 50, "", message, "" )
        VideoLink = ''
        subs=''
        VideoLink = self.up.getVideoLink(url)
        if isinstance(VideoLink, basestring):
            videoUrl = VideoLink
        else:
            videoUrl = VideoLink[0]
            subs = VideoLink[1]
        progress.update( 70, "", message, "" )
        #progress.close()
        if videoUrl == '':
            progress.close()
            d = xbmcgui.Dialog()
            d.ok('Nie znaleziono streamingu', 'Mo�e to chwilowa awaria.', 'Spr�buj ponownie za jaki� czas')
            return False
        if icon == '' or  icon == 'None':
            icon = "DefaultVideo.png"
        if plot == '' or plot == 'None':
            plot = ''
        liz=xbmcgui.ListItem(title, iconImage=icon, thumbnailImage=icon)
        liz.setInfo( type="video", infoLabels={ "Title": title,"Plot": plot} )

        if subs != '':
            subsdir = os.path.join(ptv.getAddonInfo('path'), "subs")
            if not os.path.isdir(subsdir):
                os.mkdir(subsdir)
            query_data = { 'url': subs, 'use_host': False, 'use_header': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
            progress.update( 90, "", message, "" )
            data = self.cm.getURLRequestData(query_data)
            output = open((os.path.join(subsdir, "napisy.txt" )),"w+")
            progress.update( 100, "", message, "" )
            output.write(data)
            output.close()
            time.sleep(6)
            progress.close()
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(videoUrl, liz)

            for _ in xrange(30):
                if xbmcPlayer.isPlaying():
                    break
                time.sleep(1)
            else:
                raise Exception('No video playing. Aborted after 30 seconds.')
            xbmcPlayer.setSubtitles((os.path.join(subsdir, "napisy.txt" )))
            xbmcPlayer.showSubtitles(True)
            return True
        else:
            progress.update( 90, "", message, "" )
            progress.close()
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(videoUrl, liz)
            return True

    def handleService(self):
    	params = self.parser.getParams()
        name = self.parser.getParam(params, "name")
        category = self.parser.getParam(params, "category")
        url = self.parser.getParam(params, "url")
        title = self.parser.getParam(params, "title")
        icon = self.parser.getParam(params, "icon")
        myid = self.parser.getParam(params, "myid")
        desc = self.parser.getParam(params, "desc")

        print(myid,name,category,url,title,icon,desc)

        if name == None:
            self.listsMain(MENU_TAB)
        elif name == 'main1':
            self.listsMainMenu("0")
        elif name == 'main2':
             self.listsItems('watchlist')
        elif name == 'main3':
             self.listsItems('favorite')
        elif name == 'main4':
             self.listsItemsFollow('users')
        elif name == 'follow-cat':
             self.listsItemsFollowCat('followfiles',myid)

        elif name == 'main5':
            key = self.searchInputText()
            if key != None:
                self.listsItems('search', key)

        elif name == 'main-menu':
            self.listsMainMenu(myid)
        if name == 'playSelectedMovie':
            self.LOAD_AND_PLAY_VIDEO(url, title, icon, '',desc,myid)

init = xbmcfilm()
init.handleService()