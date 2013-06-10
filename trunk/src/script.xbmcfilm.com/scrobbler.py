# -*- coding: utf-8 -*-
#

import xbmc
import xbmcaddon
import threading
import time
import urllib
import utilities
#from tmdb import TmdbDatasource
from utilities import Debug, get_float_setting
from rating import ratingCheck


# read settings
__settings__ = xbmcaddon.Addon("script.xbmcfilm.com")
__language__ = __settings__.getLocalizedString
#http://api.themoviedb.org/2.1/Movie.search/en/xml/e6ad14ba5c9d55b7622f943c2efe1c39/Transformers+2007

class Scrobbler(threading.Thread):

    xbmcfilm = None
    totalTime = 1
    watchedTime = 0
    startTime = 0
    pausedTime = 0
    curVideo = None
    curVideoData = None
    pinging = False
    playlistLength = 1
    abortRequested = False
    markedAsWatched = []
    sessionid = 0
    xbmcpath = ''

    def __init__(self, api):
        threading.Thread.__init__(self)
        self.xbmcfilm = api
        self.start()
#        self.imdb = TmdbDatasource()

    def run(self):
        # When requested ping trakt to say that the user is still watching the item
        count = 0
        Debug("[Scrobbler] Starting.")
        while (not (self.abortRequested or xbmc.abortRequested)):
            xbmc.sleep(5000) # sleep for 5 seconds
            if self.pinging and xbmc.Player().isPlayingVideo():
                count += 1
                self.watchedTime = xbmc.Player().getTime()
                self.startTime = time.time()
                if count >= 100:
                    self.watching()
                    count = 0
            else:
                count = 0

        Debug("[Scrobbler] Stopping.")

    def playbackStarted(self, data):
        Debug("[Scrobbler] playbackStarted(data: %s)" % data)
        if self.curVideo != None and self.curVideo != data['item']:
            self.playbackEnded()
        self.curVideo = data['item']
        self.curVideoData = data
        self.xbmcpath = data['xbmcpath']
        if self.curVideo != None:
            if 'type' in self.curVideo: #and 'id' in self.curVideo:
                Debug("[Scrobbler] Watching: "+self.curVideo['type']+" xbmcpath" +self.xbmcpath)
                try:
                    if not xbmc.Player().isPlayingVideo():
                        Debug("[Scrobbler] Suddenly stopped watching item")
                        return
                    time.sleep(1) # Wait for possible silent seek (caused by resuming)
                    self.watchedTime = xbmc.Player().getTime()
                    self.totalTime = xbmc.Player().getTotalTime()
                    if self.totalTime == 0:
                        if self.curVideo['type'] == 'movie':
                            self.totalTime = 90
                        elif self.curVideo['type'] == 'episode':
                            self.totalTime = 30
                        else:
                            self.totalTime = 1
                    #self.playlistLength = utilities.getPlaylistLengthFromXBMCPlayer(data['player']['playerid'])
                    # playerid 1 is video.
                    self.playlistLength = utilities.getPlaylistLengthFromXBMCPlayer(1)
                    if (self.playlistLength == 0):
                        Debug("[Scrobbler] Warning: Cant find playlist length?!, assuming that this item is by itself")
                        self.playlistLength = 1
                    if self.curVideo["type"] == "episode":
                        if self.curVideo.has_key("multi_episode_count"):
                            self.markedAsWatched = []
                            episode_count = self.curVideo["multi_episode_count"]
                            for i in range(episode_count):
                                self.markedAsWatched.append(False)
                except Exception, e:
                    Debug("[Scrobbler] Suddenly stopped watching item, or error: %s" % e.message)
                    self.curVideo = None
                    self.startTime = 0
                    return
                self.startTime = time.time()
                #session id
                response = self.xbmcfilm.getSession(self.curVideo["type"])
                if response != None:
                    Debug("[Scrobbler] Session response: "+str(response))
                    self.sessionid = response
                #
                self.watching()
                self.pinging = True
            else:
                self.curVideo = None
                self.startTime = 0

    def playbackResumed(self):
        Debug("[Scrobbler] playbackResumed()")
        if self.pausedTime != 0:
            p = time.time() - self.pausedTime
            Debug("[Scrobbler] Resumed after: %s" % str(p))
            self.pausedTime = 0
            self.watching()

    def playbackPaused(self):
        Debug("[Scrobbler] playbackPaused()")
        if self.startTime != 0:
            self.watchedTime += time.time() - self.startTime
            Debug("[Scrobbler] Paused after: "+str(self.watchedTime))
            self.startTime = 0
            self.pausedTime = time.time()

    def playbackSeek(self):
        Debug("[Scrobbler] playbackSeek()")
        if self.startTime != 0:
            self.watchedTime = xbmc.Player().getTime()
            self.startTime = time.time()

    def playbackEnded(self):
        Debug("[Scrobbler] playbackEnded()")
        if self.startTime != 0:
            if self.curVideo == None:
                Debug("[Scrobbler] Warning: Playback ended but video forgotten")
                return 
            self.watchedTime += time.time() - self.startTime
            self.pinging = False
            self.markedAsWatched = []

            if self.watchedTime != 0:
                if 'type' in self.curVideo: #and 'id' in self.curVideo:
                    self.check()
                    ratingCheck(self.curVideo, self.watchedTime, self.totalTime, self.playlistLength,self.sessionid)
                self.watchedTime = 0
            self.startTime = 0
            self.curVideo = None
            self.sessionid = 0

    def _currentEpisode(self, watchedPercent, episodeCount):
        split = (100 / episodeCount)
        for i in range(episodeCount - 1, 0, -1):
            if watchedPercent >= (i * split):
                return i
        return 0
    def chkdic(self,value,dic):
        if value in dic.itervalues():
            return dic[value]
        else:
            return ""
    def watching(self):
        Debug("[Scrobbler] watching()")
        scrobbleMovieOption = __settings__.getSetting("scrobble_movie")
        scrobbleEpisodeOption = __settings__.getSetting("scrobble_episode")
        if self.curVideo['type'] == 'movie' and scrobbleMovieOption == 'true':
            match = None
            if 'id' in self.curVideo:
                match = utilities.getMovieDetailsFromXbmc(self.curVideo['id'], ['imdbnumber', 'title', 'year'])
                match['file'] = self.chkdic('file',self.curVideo)
                match['thumbnail'] = self.chkdic('thumbnail',self.curVideo)
            elif 'title' in self.curVideo and 'year' in self.curVideo:
                match = {}

                match['imdbnumber'] = self.curVideo['imdbnumber']
                match['title'] = self.curVideo['title']
                match['year'] = self.curVideo['year']
                match['file'] = self.chkdic('file',self.curVideo)
                match['thumbnail'] = self.curVideo['thumbnail']

            if match == None:
                return
            
            duration = self.totalTime / 60
            watchedPercent = int((self.watchedTime / self.totalTime) * 100)
            response = self.xbmcfilm.watchingMovie(match['imdbnumber'], match['title'], match['year'], duration, watchedPercent, match['file'], match['thumbnail'],self.sessionid,self.xbmcpath)
            response =''
            if response != None:
                Debug("[Scrobbler] Watch response: "+str(response))
                
        elif self.curVideo['type'] == 'episode' and scrobbleEpisodeOption == 'true':
            match = None
            if 'id' in self.curVideo:
                if self.curVideo.has_key("multi_episode_count"):
                    cur_episode = self._currentEpisode((self.watchedTime / self.totalTime) * 100, self.curVideo['multi_episode_count'])
                    if cur_episode > 0:
                        if not self.markedAsWatched[cur_episode - 1]:
                            Debug("[Scrobbler] Attempting to scrobble episode part %d of %d." % (cur_episode, self.curVideo['multi_episode_count']))
                            episode_data = utilities.getEpisodeDetailsFromXbmc(self.curVideo["multi_episode_data"][cur_episode - 1], ['showtitle', 'season', 'episode', 'tvshowid', 'uniqueid'])
                            response = self.xbmcfilm.scrobbleEpisode(episode_data['tvdb_id'], episode_data['showtitle'], episode_data['year'], episode_data['season'], episode_data['episode'], episode_data['uniqueid']['unknown'], self.totalTime/60, 100)
                            if response != None:
                                Debug("[Scrobbler] Scrobble response: %s" % str(response))
                            self.markedAsWatched[cur_episode - 1] = True

                    Debug("[Scrobbler] Multi-part episode, watching part %d of %d." % (cur_episode + 1, self.curVideo['multi_episode_count']))
                    match = utilities.getEpisodeDetailsFromXbmc(self.curVideo["multi_episode_data"][cur_episode], ['showtitle', 'season', 'episode', 'tvshowid', 'uniqueid'])
                else:
                    match = utilities.getEpisodeDetailsFromXbmc(self.curVideo['id'], ['showtitle', 'season', 'episode', 'tvshowid', 'uniqueid'])
            elif 'showtitle' in self.curVideoData and 'season' in self.curVideoData and 'episode' in self.curVideoData:
                match = {}
                match['tvdb_id'] = None
                match['year'] = None
                match['showtitle'] = self.curVideoData['showtitle']
                match['season'] = self.curVideoData['season']
                match['episode'] = self.curVideoData['episode']
                match['uniqueid'] = None
            if match == None:
                return
                
            duration = self.totalTime / 60
            watchedPercent = int((self.watchedTime / self.totalTime) * 100)
            response = self.xbmcfilm.watchingEpisode(match['tvdb_id'], match['showtitle'], match['year'], match['season'], match['episode'], match['uniqueid']['unknown'], duration, watchedPercent)
            if response != None:
                Debug("[Scrobbler] Watch response: "+str(response))

    def stoppedWatching(self):
        Debug("[Scrobbler] stoppedWatching()")
        scrobbleMovieOption = __settings__.getSetting("scrobble_movie")
        scrobbleEpisodeOption = __settings__.getSetting("scrobble_episode")

        if self.curVideo['type'] == 'movie' and scrobbleMovieOption == 'true':
            response = self.xbmcfilm.cancelWatchingMovie()
            if response != None:
                Debug("[Scrobbler] Cancel watch response: "+str(response))
        elif self.curVideo['type'] == 'episode' and scrobbleEpisodeOption == 'true':
            response = self.xbmcfilm.cancelWatchingEpisode()
            if response != None:
                Debug("[Scrobbler] Cancel watch response: "+str(response))

    def scrobble(self):
        Debug("[Scrobbler] scrobble()")
        scrobbleMovieOption = __settings__.getSetting("scrobble_movie")
        scrobbleEpisodeOption = __settings__.getSetting("scrobble_episode")

        if self.curVideo['type'] == 'movie' and scrobbleMovieOption == 'true':
            match = None
            if 'id' in self.curVideo:
                match = utilities.getMovieDetailsFromXbmc(self.curVideo['id'], ['imdbnumber', 'title', 'year'])
                match['file'] = self.chkdic('file',self.curVideo)
                match['thumbnail'] = self.chkdic('thumbnail',self.curVideo)
            elif 'title' in self.curVideo and 'year' in self.curVideo:
                match = {}
                match['imdbnumber'] = self.curVideo['imdbnumber']
                match['title'] = self.curVideo['title']
                match['year'] = self.curVideo['year']
                match['file'] = self.chkdic('file',self.curVideo)
                match['thumbnail'] = self.curVideo['thumbnail']
                
            if match == None:
                return

            duration = self.totalTime / 60
            watchedPercent = int((self.watchedTime / self.totalTime) * 100)
            response = self.xbmcfilm.scrobbleMovie(match['imdbnumber'], match['title'], match['year'], duration, watchedPercent,match['file'], match['thumbnail'],self.sessionid,self.xbmcpath)
            response = ''
            if response != None:
                Debug("[Scrobbler] Scrobble response: "+str(response))

        elif self.curVideo['type'] == 'episode' and scrobbleEpisodeOption == 'true':
            match = None
            if 'id' in self.curVideo:
                if self.curVideo.has_key("multi_episode_count"):
                    #cur_episode = self._currentEpisode((self.watchedTime / self.totalTime) * 100, self.curVideo['multi_episode_count'])
                    cur_episode = self.curVideo['multi_episode_count'] - 1
                    Debug("[Scrobbler] Multi-part episode, scrobbling part %d of %d." % (cur_episode + 1, self.curVideo['multi_episode_count']))
                    match = utilities.getEpisodeDetailsFromXbmc(self.curVideo["multi_episode_data"][cur_episode], ['showtitle', 'season', 'episode', 'tvshowid', 'uniqueid'])
                else:
                    match = utilities.getEpisodeDetailsFromXbmc(self.curVideo['id'], ['showtitle', 'season', 'episode', 'tvshowid', 'uniqueid'])
            elif 'showtitle' in self.curVideoData and 'season' in self.curVideoData and 'episode' in self.curVideoData:
                match = {}
                match['tvdb_id'] = None
                match['year'] = None
                match['showtitle'] = self.curVideoData['showtitle']
                match['season'] = self.curVideoData['season']
                match['episode'] = self.curVideoData['episode']
                match['uniqueid'] = self.curVideoData['uniqueid']['unknown']
            if match == None:
                return
            
            duration = self.totalTime / 60
            watchedPercent = int((self.watchedTime / self.totalTime) * 100)
            response = self.xbmcfilm.scrobbleEpisode(match['tvdb_id'], match['showtitle'], match['year'], match['season'], match['episode'], match['uniqueid']['unknown'], duration, watchedPercent)
            if response != None:
                Debug("[Scrobbler] Scrobble response: "+str(response))

    def check(self):
        scrobbleMinViewTimeOption = get_float_setting("scrobble_min_view_time")

        Debug("[Scrobbler] watched: %s / %s" % (str(self.watchedTime), str(self.totalTime)))
        if ((self.watchedTime / self.totalTime) * 100) >= scrobbleMinViewTimeOption:
            self.scrobble()
        else:
            self.stoppedWatching()
