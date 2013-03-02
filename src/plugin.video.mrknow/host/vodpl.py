# -*- coding: utf-8 -*-
import urllib, urllib2, re, os, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
from urlparse import urlparse, parse_qs
import urlparser
import urlparse,httplib
import simplejson as json

scriptID = 'plugin.video.mrknow'
scriptname = "Filmy online www.mrknow.pl - vodpl"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, pCommon, Parser

log = pLog.pLog()

jsonurl = 'http://video.external.cms.onetapi.pl/'
imgurl = 'http://m.ocdn.eu/_m/'
mainUrl = 'http://www.vodpl.pl/m/'
playerUrl = 'http://www.youtube.pl/'

HOST = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3'
null = 0
true = 1

MENU_TAB = {2: "filmy",
            3: "polecamy",
            4: "dokumenty",
            5: "Bajki - nie dziala"}


class vodpl:
    def __init__(self):
        log.info('Starting vodpl.pl')
        self.cm = pCommon.common()
        self.parser = Parser.Parser()
        self.up = urlparser.urlparser()

    def getpage(self,data):
        header = {"Content-Type": "application/json-rpc","Accept": "application/json","X-Onet-App": "vod.ios.mobile-apps.onetapi.pl","User-Agent": "pl.vod.onet.pl/1.1 (unknown, iPhone OS 6.1.2, iPhone, Scale/2.000000)"}
        req = urllib2.Request(jsonurl, data, header)
        f = urllib2.urlopen(req)
        response = f.read()
        f.close() 
        return response
#        vod_getcat = [{'method':'cmsQuery','id':'945893BD-21DD-4FED-9CCC-C3BBB056ADB0','jsonrpc':'2.0','params':{'sort':'TITLE_ASC','method':'aggregates','args':{'withoutDRM':'True','device':'mobile','names':'genres','payment':['-svod','-ppv'],'channel':'polecamy'},'context':'onet/vod'}},{'method':'cmsQuery','id':'DEB12D37-2E31-486B-B2A5-10A9C8B3D8BA','jsonrpc':'2.0','params':{'sort':'TITLE_ASC','method':'aggregates','args':{'withoutDRM':'True','device':'mobile','names':'genres','payment':['-svod','-ppv'],'channel':'filmy'},'context':'onet/vod'}},{'method':'cmsQuery','id':'927BE685-2FFC-418F-A743-6325A1DD4A4A','jsonrpc':'2.0','params':{'sort':'TITLE_ASC','method':'aggregates','args':{'withoutDRM':'True','device':'mobile','names':'genres','payment':['-svod','-ppv'],'channel':'seriale'},'context':'onet/vod'}},{'method':'cmsQuery','id':'B3E498C9-16C5-48B9-990A-4135150705C3','jsonrpc':'2.0','params':{'sort':'TITLE_ASC','method':'aggregates','args':{'withoutDRM':'True','device':'mobile','names':'genres','payment':['-svod','-ppv'],'channel':'dokumenty'},'context':'onet/vod'}},{'method':'cmsQuery','id':'BF6B227C-CC5C-4188-A4A1-E0AB7B9E28B8','jsonrpc':'2.0','params':{'sort':'TITLE_ASC','method':'aggregates','args':{'withoutDRM':'True','device':'mobile','names':'genres','payment':['-svod','-ppv'],'channel':'bajki'},'context':'onet/vod'}}]
#        vod_result = [{"jsonrpc": "2.0", "result": {"metrics": {"count": 10, "current": 1, "total": 0, "offset": 0}, "timestamp": 1362168469, "data": [{"structureType": "aggregate", "aggregateName": "genres", "aggregateObject": null, "structureRevision": "1", "metrics": null, "items": []}], "error": {"message": "", "code": 0}}, "id": "945893BD-21DD-4FED-9CCC-C3BBB056ADB0"}, {"jsonrpc": "2.0", "result": {"metrics": {"count": 10, "current": 1, "total": 0, "offset": 0}, "timestamp": 1362168469, "data": [{"structureType": "aggregate", "aggregateName": "genres", "aggregateObject": null, "structureRevision": "1", "metrics": null, "items": [{"structureRevision": "1", "structureType": "simpleattribute", "name": "animowany", "value": 7}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "biograficzny", "value": 16}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "dla dzieci", "value": 16}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "dramat", "value": 160}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "historyczny", "value": 11}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "horror", "value": 24}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "komedia", "value": 125}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "kryminalny", "value": 19}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "melodramat", "value": 9}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "muzyczny", "value": 13}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "obyczajowy", "value": 105}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "psychologiczny", "value": 47}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "sci-fi", "value": 10}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "sensacyjny", "value": 35}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "thriller", "value": 17}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "wojenny", "value": 22}]}], "error": {"message": "", "code": 0}}, "id": "DEB12D37-2E31-486B-B2A5-10A9C8B3D8BA"}, {"jsonrpc": "2.0", "result": {"metrics": {"count": 10, "current": 1, "total": 0, "offset": 0}, "timestamp": 1362168469, "data": [{"structureType": "aggregate", "aggregateName": "genres", "aggregateObject": null, "structureRevision": "1", "metrics": null, "items": [{"structureRevision": "1", "structureType": "simpleattribute", "name": "biograficzny", "value": 1}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "dramat", "value": 2}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "familijny", "value": 28}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "historyczny", "value": 75}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "komedia", "value": 218}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "kryminalny", "value": 180}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "obyczajowy", "value": 904}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "sensacyjny", "value": 193}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "sitcom", "value": 3}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "wojenny", "value": 78}]}], "error": {"message": "", "code": 0}}, "id": "927BE685-2FFC-418F-A743-6325A1DD4A4A"}, {"jsonrpc": "2.0", "result": {"metrics": {"count": 10, "current": 1, "total": 0, "offset": 0}, "timestamp": 1362168469, "data": [{"structureType": "aggregate", "aggregateName": "genres", "aggregateObject": null, "structureRevision": "1", "metrics": null, "items": [{"structureRevision": "1", "structureType": "simpleattribute", "name": "dokumentalny", "value": 73}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "dramat", "value": 1}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "historyczny", "value": 2}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "komedia", "value": 1}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "koncert", "value": 1}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "podr\u00f3\u017cniczy", "value": 1}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "sportowy", "value": 1}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "wojenny", "value": 2}]}], "error": {"message": "", "code": 0}}, "id": "B3E498C9-16C5-48B9-990A-4135150705C3"}, {"jsonrpc": "2.0", "result": {"metrics": {"count": 10, "current": 1, "total": 0, "offset": 0}, "timestamp": 1362168469, "data": [{"structureType": "aggregate", "aggregateName": "genres", "aggregateObject": null, "structureRevision": "1", "metrics": null, "items": []}], "error": {"message": "", "code": 0}}, "id": "BF6B227C-CC5C-4188-A4A1-E0AB7B9E28B8"}]

        

    def listsMainMenu(self, table):
        for num, val in table.items():
            self.add('vodpl', 'main-menu', val, val, 'None', 'None', 'None', 'None', True, False)
        #result = [{"method":"cmsQuery","id":"945893BD-21DD-4FED-9CCC-C3BBB056ADB0","jsonrpc":"2.0","params":{"sort":"TITLE_ASC","method":"aggregates","args":{"withoutDRM":"True","device":"mobile","names":"genres","payment":["-svod","-ppv"],"channel":"polecamy"},"context":"onet/vod"}},{"method":"cmsQuery","id":"DEB12D37-2E31-486B-B2A5-10A9C8B3D8BA","jsonrpc":"2.0","params":{"sort":"TITLE_ASC","method":"aggregates","args":{"withoutDRM":"True","device":"mobile","names":"genres","payment":["-svod","-ppv"],"channel":"filmy"},"context":"onet/vod"}},{"method":"cmsQuery","id":"927BE685-2FFC-418F-A743-6325A1DD4A4A","jsonrpc":"2.0","params":{"sort":"TITLE_ASC","method":"aggregates","args":{"withoutDRM":"True","device":"mobile","names":"genres","payment":["-svod","-ppv"],"channel":"seriale"},"context":"onet/vod"}},{"method":"cmsQuery","id":"B3E498C9-16C5-48B9-990A-4135150705C3","jsonrpc":"2.0","params":{"sort":"TITLE_ASC","method":"aggregates","args":{"withoutDRM":"True","device":"mobile","names":"genres","payment":["-svod","-ppv"],"channel":"dokumenty"},"context":"onet/vod"}},{"method":"cmsQuery","id":"BF6B227C-CC5C-4188-A4A1-E0AB7B9E28B8","jsonrpc":"2.0","params":{"sort":"TITLE_ASC","method":"aggregates","args":{"withoutDRM":"True","device":"mobile","names":"genres","payment":["-svod","-ppv"],"channel":"bajki"},"context":"onet/vod"}}]
        #for d in result:
        #    print d["params"]["args"]["channel"]
        #    print d["id"]
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def listsCategoriesMenu(self,category):

        valTab = [] 
        strTab = []    
        vod_filmyget = '[{"method":"cmsQuery","id":"020E5AD0-006E-41B7-B2F0-35B64BF6FA27","jsonrpc":"2.0","params":{"sort":"TITLE_ASC","method":"aggregates","args":{"withoutDRM":"True","device":"mobile","names":"genres","payment":["-svod","-ppv"],"channel":"'+category+'"},"context":"onet/vod"}}]'
        
        vod_filmy = self.getpage(vod_filmyget)
        vod_filmy = eval(vod_filmy)
        print ("VOD",vod_filmy)
        #vod_filmy = [{"jsonrpc": "2.0", "result": {"metrics": {"count": 10, "current": 1, "total": 0, "offset": 0}, "timestamp": 1362216678, "data": [{"structureType": "aggregate", "aggregateName": "genres", "aggregateObject": null, "structureRevision": "1", "metrics": null, "items": [{"structureRevision": "1", "structureType": "simpleattribute", "name": "animowany", "value": 7}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "biograficzny", "value": 16}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "dla dzieci", "value": 16}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "dramat", "value": 160}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "historyczny", "value": 11}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "horror", "value": 24}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "komedia", "value": 125}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "kryminalny", "value": 19}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "melodramat", "value": 9}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "muzyczny", "value": 13}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "obyczajowy", "value": 105}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "psychologiczny", "value": 47}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "sci-fi", "value": 10}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "sensacyjny", "value": 35}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "thriller", "value": 17}, {"structureRevision": "1", "structureType": "simpleattribute", "name": "wojenny", "value": 22}]}], "error": {"message": "", "code": 0}}, "id": "020E5AD0-006E-41B7-B2F0-35B64BF6FA27"}]

        
        
        for o in vod_filmy:
            
            match = re.compile("'name': '(.*?)', 'value': (.*?)}", re.DOTALL).findall(str(o))
            for i in range(len(match)):
                strTab.append(match[i][0])
                strTab.append(match[i][1])
                strTab.append(o["id"])
                valTab.append(strTab)
                strTab = []
                valTab.sort(key = lambda x: x[0])
#             
        print valTab
        for i in valTab:
            self.add('vodpl', 'categories-menu', category, i[0], 'None', 'None', 'None', 'None', True, False,str(i[1]),i[2])
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        #if len(match) > 0:
        #    log.info('Listuje kategorie: ')
        #    for i in range(len(match)):
        #        url = mainUrl + match[i][1]
        #        self.add('vodpl', 'categories-menu', match[i][2].strip(), 'None', 'None', url, 'None', 'None', True, False)
        #xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def getSearchURL(self, key):
        url = mainUrl + 'search.php?phrase=' + urllib.quote_plus(key) 
        return url
        #req = urllib2.Request(url)
        #req.add_header('User-Agent', HOST)
        #openURL = urllib2.urlopen(req)
        #readURL = openURL.read()
        

    def listsItems(self, category, title,id1='',id2=''):
        #print("DATA",title,id1,id2)

#        test1 = {'method':'cmsQuery','id':'613E92D5-1D78-44D5-8294-C991540F68DB','jsonrpc':'2.0','params':{'sort':'TITLE_ASC','method':'aggregates','args':{'withoutDRM':'True','device':'mobile','names':'genres','payment':['-svod','-ppv'],'channel':'polecamy'},'context':'onet/vod'}},{'method':'cmsQuery','id':'A564F3E3-9074-4847-9C2A-8902B2B43B76','jsonrpc':'2.0','params':{'sort':'TITLE_ASC','method':'aggregates','args':{'withoutDRM':'True','device':'mobile','names':'genres','payment':['-svod','-ppv'],'channel':'filmy'},'context':'onet/vod'}},{'method':'cmsQuery','id':'A9C7A298-FF2D-4E32-A8F9-D3B286FAFC89','jsonrpc':'2.0','params':{'sort':'TITLE_ASC','method':'aggregates','args':{'withoutDRM':'True','device':'mobile','names':'genres','payment':['-svod','-ppv'],'channel':'seriale'},'context':'onet/vod'}},{'method':'cmsQuery','id':'CD01FEB2-201B-42F2-AB21-E380491F2AA6','jsonrpc':'2.0','params':{'sort':'TITLE_ASC','method':'aggregates','args':{'withoutDRM':'True','device':'mobile','names':'genres','payment':['-svod','-ppv'],'channel':'dokumenty'},'context':'onet/vod'}},{'method':'cmsQuery','id':'BE5A6E6B-D2A1-4DCC-A431-6692DDA1AAAC','jsonrpc':'2.0','params':{'sort':'TITLE_ASC','method':'aggregates','args':{'withoutDRM':'True','device':'mobile','names':'genres','payment':['-svod','-ppv'],'channel':'bajki'},'context':'onet/vod'}}
#        test2 = {"method":"cmsQuery","id":"ACA830DA-1FBF-4D45-88D5-A18F3509237E","jsonrpc":"2.0","params":{"sort":"DATE_DESC","method":"search","args":{"withoutDRM":"True","device":"mobile","noSeriesGroup":"True","payment":["-svod","-ppv"]},"context":"onet/bajki","range":[0,10000]}}
#        test3 = {"method":"cmsGet","id":"B51DE533-CCEC-47CA-BA71-5F8DDFF02AEA","jsonrpc":"2.0","params":{"context":"onet/vod","id":"86419","object":"Video"}}
        
        vod_getitems = '[{"method":"cmsQuery","id":"'+id2+'","jsonrpc":"2.0","params":{"sort":"DATE_DESC","method":"search","args":{"withoutDRM":"True","device":"mobile","payment":["-svod","-ppv"],"genre":"'+title+'","channel":"'+category+'"},"context":"onet/vod","range":[0,10000]}}]'
        vod_items = self.getpage(vod_getitems)
        match1 = re.compile('"structureType": "video", "title": "(.*?)",', re.DOTALL).findall(str(vod_items))
        match2 = re.compile('"videoId": "(.*?)",', re.DOTALL).findall(str(vod_items))
        match3 = re.compile('"ckmId": "(.*?)",', re.DOTALL).findall(str(vod_items))  
        match4 = re.compile('"poster": {"structureType": "content.media.image", "structureRevision": "2.1.1", "modificationEpoch": 0, "imageId": "(.*?)",', re.DOTALL).findall(str(vod_items))  
         
        print match1, len(match1) 
        print match4,len(match4)
        
        print vod_items
        
        for i in range(len(match1)):
            if len(match4)>0:
                image = imgurl + match4[i] + ',10,1.jpg'
            else:
                image =''          
            #add(    service,    name,            category, title, iconimage, url, desc, rating, folder = True, isPlayable = True,id1='',id2='')       
            self.add('vodpl', 'playSelectedMovie', 'None', match1[i].decode('utf-8'), image, 'None', 'None', 'None', False, False,match2[i],match3[i])
        
        
        #req = urllib2.Request(url)
        #req.add_header('Content-Type', 'application/json')
        #response = urllib2.urlopen(req, jdata1)
        #print ('Link',response)
#        data = { "data":"ur data"}
        
        
        #add(self, service, name, category, title, iconimage, url, desc, rating, folder = True, isPlayable = True,id1='',id2=''):

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
                self.add('vodpl', 'items-menu', 'None', title, 'None', destUrl, 'None', 'None', True, False)
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
                self.add('vodpl', 'items-menu', 'None', title, 'None', destUrl, 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1])) 


    def getMovieLinkFromXML(self, id1,id2):
        #match = re.compile('<blockquote cite="(.*?)"', re.DOTALL).findall(link)
        #vod_item = '{"method":"cmsGet","id":"BAEAC0C3-1FC5-48D2-BC01-671AFC429C11","jsonrpc":"2.0","params":{"context":"onet/vod","id":"112363","object":"Video"}}'
        #response = self.getpage(vod_item)
        #url = 'http://vod.pl/'+id2+',d2dd64302895d26784c706717a1996b0.html?dv=aplikacja_iosVOD/filmy'
        url = 'http://qi.ckm.onetapi.pl/?callback=jQuery18301641132461372763_1362164907154&body[id]=EBBAE1E4326E4CE9343FFEEF56A9198D&body[jsonrpc]=2.0&body[method]=get_asset_detail&body[params][ID_Publikacji]='+id2+'&body[params][Service]=vod.onet.pl&content-type=application%2Fjsonp&x-onet-app=player.front.onetapi.pl&_=1362164913145'
        query_data = { 'url': url, 'use_host': True, 'host':'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Mobile/10B146', 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        #link = 'jQuery18301641132461372763_1362164907154({"jsonrpc": "2.0", "result": {"0": {"playlist": [{"type": "movie", "format": "wideo"}], "meta": {"description": "<STRONG>&quot;Disco Robaczki&quot; to animowana komedia przygodowa dla ca\u0142ej rodziny w rytmie najwi\u0119kszych przeboj\u00f3w tanecznych! Tomasz Karolak, Zbigniew Wodecki, Agnieszka Chyli\u0144ska i Anna Mucha w polskiej wersji j\u0119zykowej filmu. </STRONG><br><br>\nD\u017cd\u017cownica Bogdan nie mo\u017ce pogodzi\u0107 si\u0119 z szar\u0105 egzystencj\u0105 pracownika fabryki kompostu. Pewnego dnia odkrywa w rzeczach taty zakurzon\u0105 p\u0142yt\u0119, odpala gramofon i doznaje ol\u015bnienia... Jego serce zawsze bi\u0142o w rytmie disco. Zak\u0142ada zesp\u00f3\u0142 i wraz z grup\u0105 przyjaci\u00f3\u0142, kt\u00f3rzy braki talentu nadrabiaj\u0105 ambicj\u0105, zg\u0142asza si\u0119 do udzia\u0142u w konkursie wokalnym.<br><br>\nBogdan i jego rozbujane Disco Robaczki - Gocha, Tytus, Nerwal i Kadrowa Danuta - zrobi\u0105 wszystko, \u017ceby udowodni\u0107 jurorom i ca\u0142emu \u015bwiatu, \u017ce... d\u017cd\u017cownice s\u0105 gor\u0105ce i nie ma haka na robaka! Zanim spe\u0142ni\u0105 si\u0119 ich marzenia - czeka je ca\u0142e mn\u00f3stwo szalonych przyg\u00f3d, w tym spotkanie oko w haczyk z gro\u017anym w\u0119dkarzem, uwi\u0119zienie przez zbieracza \u017cywej przyn\u0119ty i konfrontacja z robalami-gorylami dyrektora Pastewnego.<br><br>\nObok komicznych i trzymaj\u0105cych w napi\u0119ciu perypetii sympatycznych bohater\u00f3w, nieocenionym walorem tego filmu jest muzyka. Widzowie us\u0142ysz\u0105 najwi\u0119ksze hity lat 70., mi\u0119dzy innymi <STRONG>&quot;Disco Inferno&quot;</STRONG>, <STRONG>&quot;YMCA&quot;</STRONG>, <STRONG>&quot;I Will Survive&quot;</STRONG> w ca\u0142kowicie nowych, wsp\u00f3\u0142czesnych wykonaniach.", "reference": "OnetDB-7854:856:403", "tags": ["film", "disco", "muzyka", "konkurs", "rywalizacja", "animacja"], "lenght": 4510, "OID_CKM_Media": 35150, "UUID": "fff4ab1f-cb26-4dcc-8a56-5ebc031119de", "service": "vod", "title": "Disco Robaczki", "addDate": "2012-10-01 09:09:00", "OID": "351763026", "ID_Publikacji": "351763026", "drm": "{\"PlayReady\": \"NFvdzPg5G0S0UwiWMn+ipw==\"}", "licenseurl": "/351763026,2013030213151362226514,drmlicense.xml", "nobanner": 0, "image": "5a494526d403f1ad5e3756cb12f572c1.jpg"}, "license": {"service": 1, "geoIP": 1, "allowedEmmisionDevices": {"mobile": 1, "PC": 1, "TV": 1, "Lajt": 1}, "period": 1, "source": {"name": "Kino \u015awiat", "copyright": "", "url": "", "text": "", "imageUrl": "", "providerLogo": {"position": "", "imageUrl": ""}}, "adult": 0}, "formats": {"wideo": {"ismc": [{"url": "http://media.onet.pl/vod/7072407_11_350_14088_0000.ism/Manifest", "video_bitrate": null, "audio_bitrate": null}], "mp4": [{"url": "http://media.onet.pl/_mv/aIvtLxlfoQ.d.mp4", "video_bitrate": "200.00", "audio_bitrate": "128.00"}, {"url": "http://media.onet.pl/_mv/aIvtLxlfoQ.c.mp4", "video_bitrate": "450.00", "audio_bitrate": "128.00"}, {"url": "http://media.onet.pl/_mv/aIvtLxlfoQ.b.mp4", "video_bitrate": "900.00", "audio_bitrate": "128.00"}, {"url": "http://media.onet.pl/_mv/aIvtLxlfoQ.a.mp4", "video_bitrate": "1800.00", "audio_bitrate": "128.00"}]}}}}, "id": "EBBAE1E4326E4CE9343FFEEF56A9198D"});'
        #print link
        #{"url": "http://media.onet.pl/_mv/YcnPH7o2pO.d.mp4", "video_bitrate": "200.00", "audio_bitrate": "128.00"}
        match1 = re.compile('"mp4": \[\{(.*?)\}\]', re.DOTALL).findall(link)
        match2 = re.compile('"url": "(.*?)", "video_bitrate": "(.*?)", "audio_bitrate": "(.*?)"', re.DOTALL).findall(match1[0])
        
        print match1
        print match2
        tab = []
        for i in range(len(match2)):
            tab.append('Wideo bitrate - ' + match2[i][1])
            
        d = xbmcgui.Dialog()        
        video_menu = d.select("Wybór jakości video", tab)

        if video_menu != "":
            #print match2[video_menu][0]
            url = match2[video_menu][0]
            return url
            
          



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
    

    def add(self, service, name, category, title, iconimage, url, desc, rating, folder = True, isPlayable = True,id1='0',id2='0'):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category + "&title=" + title + "&url=" + urllib.quote_plus(url) + "&icon=" + urllib.quote_plus(iconimage) + "&id1=" + urllib.quote_plus(id1) + "&id2=" + urllib.quote_plus(id2)
        #log.info(str(u))
#        if name == 'main-menu' or name == 'categories-menu':
#            title = category 
        if iconimage == '':
            iconimage = "DefaultVideo.png"
        liz=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        if isPlayable:
            liz.setProperty("IsPlayable", "true")
        liz.setInfo( type="Video", infoLabels={ "Title": title } )
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
            

    def LOAD_AND_PLAY_VIDEO(self, videoUrl, title, icon):
        liz=xbmcgui.ListItem(title, iconImage=icon, thumbnailImage=icon)
        liz.setInfo( type="Video", infoLabels={ "Title": title, } )
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
        id1 = self.parser.getParam(params, "id1")
        id2 = self.parser.getParam(params, "id2")
        print ("ID",id1,id2, params)
        
        if name == None:
            self.listsMainMenu(MENU_TAB)
        elif name == 'main-menu' and category != '':
            log.info('Jest Filmy: ')
            self.listsCategoriesMenu(category)
            
        elif name == 'main-menu' and category == "Szukaj":
            key = self.searchInputText()
            self.listsItems(self.getSearchURL(key))
        elif name == 'categories-menu' and category != 'None':
            log.info('url: ' + str(title))
            self.listsItems(category,title,id1,id2)
        if name == 'playSelectedMovie':
            #self.LOAD_AND_PLAY_VIDEO(self.getMovieLinkFromXML(id1,id2), title, icon)
            #print self.getMovieLinkFromXML(id1,id2)
            self.LOAD_AND_PLAY_VIDEO(self.getMovieLinkFromXML(id1,id2), 'None', 'None')

        
  
