import urllib,urllib2,re,xbmcplugin,xbmcgui
import urlresolver
from urlparse import urlparse, parse_qs

#TV DASH - by You 2008.

def CATEGORIES():
#        addDir('','',1,'')
        addDir("Mrknow.pl - ostatnio dodane","http://www.mrknow.pl/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - Akcja","http://www.mrknow.pl/videoscategory/akcja/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - Animacja","http://www.mrknow.pl/videoscategory/animacja/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - Biograficzny","http://www.mrknow.pl/videoscategory/biograficzny/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - Czarna komedia","http://www.mrknow.pl/videoscategory/czarna-komedia/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - Dla dzieci","http://www.mrknow.pl/videoscategory/dla-dzieci/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - Dla mlodziezy","http://www.mrknow.pl/videoscategory/dla-mlodziezy/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - Dokumentalny","http://www.mrknow.pl/videoscategory/dokumentalny/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - Dramat","http://www.mrknow.pl/videoscategory/dramat/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - Dramat Historyczny","http://www.mrknow.pl/videoscategory/dramat-historyczny/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - dramat-obyczajowy","http://www.mrknow.pl/videoscategory/dramat-obyczajowy/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - fantasy","http://www.mrknow.pl/videoscategory/fantasy/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - Familijny","http://www.mrknow.pl/videoscategory/familijny/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - Gangsterski","http://www.mrknow.pl/videoscategory/gangsterski/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - Historyczny","http://www.mrknow.pl/videoscategory/historyczny/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - Horror","http://www.mrknow.pl/videoscategory/horror/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - Katastroficzny","http://www.mrknow.pl/videoscategory/katastroficzny/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - Komedia","http://www.mrknow.pl/videoscategory/komedia/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - komedia-dokumentalna","http://www.mrknow.pl/videoscategory/komedia-dokumentalna/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - komedia-kryminalna","http://www.mrknow.pl/videoscategory/komedia-kryminalna/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - komedia-obycz","http://www.mrknow.pl/videoscategory/komedia-obycz/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - komedia-rom","http://www.mrknow.pl/videoscategory/komedia-rom/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - kostiumowy","http://www.mrknow.pl/videoscategory/kostiumowy/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - kryminal","http://www.mrknow.pl/videoscategory/kryminal/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - melodramat","http://www.mrknow.pl/videoscategory/melodramat/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - musical","http://www.mrknow.pl/videoscategory/musical/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - Muzyczny","http://www.mrknow.pl/videoscategory/muzyczny/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - Obyczajowy","http://www.mrknow.pl/videoscategory/obyczajowy/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - Polityczny","http://www.mrknow.pl/videoscategory/polityczny/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - Przygodowy","http://www.mrknow.pl/videoscategory/przygodowy/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - Psychologiczny","http://www.mrknow.pl/videoscategory/psychologiczny/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - Romans","http://www.mrknow.pl/videoscategory/romans/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - sci-fi","http://www.mrknow.pl/videoscategory/sci-fi/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - sensacyjny","http://www.mrknow.pl/videoscategory/sensacyjny/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - sportowy","http://www.mrknow.pl/videoscategory/sportowy/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - sztuki-walki","http://www.mrknow.pl/videoscategory/sztuki-walki/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - thriller","http://www.mrknow.pl/videoscategory/thriller/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - western","http://www.mrknow.pl/videoscategory/western/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       
        addDir("Mrknow.pl - wojenny","http://www.mrknow.pl/videoscategory/wojenny/",1,"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg")                       

def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        print "URL:"+url
#        match=re.compile('<a href="(.+?)"><img src="(.+?)" alt="" width="90" height="90"></a>(.\s+)<a class="en" href="(.+?)">(.+?)</a>').findall(link)
#        match=re.compile('<a class="video_thumb" href="(.+?)" rel="bookmark" title="(.+?)">(.\s+)<img src="(.+?)" alt="(.+?)" title="(.+?)"  />(.\s+)</a>(.\s+)<p class="title"><a href="(.+?)" rel="bookmark" title="">(.+?)</a></p><br>').findall(link)
        match=re.compile(' <a class="video_thumb" href="(.+?)" rel="bookmark" title="(.+?)">(.\s+)<img src="(.+?)" alt="(.+?)" title="(.+?)"  /> ').findall(link)
        for i in match:
                addDir(i[1],i[0],2,i[3])
        #<span class="i_next fr"><a href="http://www.mrknow.pl/videoscategory/akcja/page/2/">Next</a> </span>
        match1=re.compile('<span class="i_next fr" ><a href="(.+?)" >Next</a> </span>').findall(link)
        if len(match1) > 0:
                addDir('Natepna strona',match1[0],1,'')

def VIDEOLINKS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<IFRAME SRC="(.+?)" SCROLLING=no></IFRAME>').findall(link)
#        match=re.compile('<IFRAME SRC="/wp-content/themes/player/miromare.php?page=(.+?)&t=(.+?)" SCROLLING=no></IFRAME>').findall(link)
        print 'znalazlem-------'
        print match
#o =  urlparse('http;//www.mrknow.pl/'+match[0])
        o = parse_qs(urlparse('http;//www.mrknow.pl/'+match[0]).query)
        print o['t'][0]
        if o['t'][0] == 'p':
                txthost = 'putlocker.com'
        elif o['t'][0] == 'y':
                txthost = 'youtube.com'
        print txthost
        sources = []
        hosted_media = urlresolver.HostedMediaFile(host=txthost, media_id=o['page'][0])
        sources.append(hosted_media)
        source = urlresolver.choose_source(sources)
        print source 
        print hosted_media
        if source:
                stream_url = source.resolve()
        else:
                return
        print 'Stream:'+stream_url        
#        stream_url = source.resolve()
#        listitem = xbmcgui.ListItem()
#        xbmc.Player().play(stream_url, listitem)        
        addLink(name,stream_url,'')
                
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param




def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url)
        
elif mode==2:
        print ""+url
        VIDEOLINKS(url,name)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
