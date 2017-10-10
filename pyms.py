__version__ = "0.2.0"
__author__ = "Samuel Haidu"
__license__ = "MIT"

'''
Module for search music videos in youtube.com and get info in discogs.com
You can:
 -Search videos and artists in youtube
 -Get the top100 in youtube music
 -Make a artist search in Discogs
 -Get the albuns of artist(listed in Discogs from url)
 -Get the tracks of album(listed in Discogs from url)
 
 BASED IN HTTP REQUEST, its not a api. If the sites change your webpage format the script can't work
'''

from bs4 import BeautifulSoup
import requests

PARSER = 'html.parser'

def yts(query):
    '''Search youtube videos and return the title, url, channel, 
       thumbnail and duration of video'''
    query = query.replace(' ', '+')
    webdata = requests.get('http://www.youtube.com/results?q='+query+'&sp=EgIQAVAU', verify=False).text
    soupdata = BeautifulSoup(webdata, PARSER)
    VideoList = []
    for link in soupdata.findAll(attrs={'class':'yt-lockup-tile'}):
        # Get info from HTML tags
        if link.find('a').get('href')[0:36] == 'https://googleads.g.doubleclick.net/': continue
        videolink = 'https://www.youtube.com' + link.find('a').get('href')
        videotitle = link.find(attrs={'class':'yt-lockup-title'}).find('a').get('title')
        try:
            videoduration = link.find(attrs={'class':'yt-lockup-title'}).find('span').text[3:-1]
            videoduration = videoduration.split()[1]
        except:videoduration = '00:00'
        try:thumbnailurl = link.find(attrs={'class':'yt-thumb-simple'}).find('img').get('src')
        except:thumbnailurl = ''
        try:channelname = link.find(attrs={'class':'yt-lockup-byline'}).find('a').text
        except:channelname = ''
        try: channelurl = 'https://www.youtube.com' + link.find(attrs={'class':'yt-lockup-byline'}).find('a').get('href')
        except: channelurl = ''
        VideoList.append({'title': videotitle, 'link': videolink, 
                         'duration': videoduration, 'channelname': channelname, 
                         'channelurl': channelurl, 'thumbnail': thumbnailurl})
    return VideoList

def ytspl(query):
    query = query.replace(' ', '+')
    webdata = requests.get('https://www.youtube.com/results?sp=EgIQA1AU&q='+query, verify=False).text
    soupdata = BeautifulSoup(webdata, PARSER)
    playlists = []
    for link in soupdata.findAll(attrs={'class':'yt-lockup-tile'}):
        playlisttitle = link.find('h3').find('a').get('title')
        try:playlistlink = 'https://www.youtube.com/playlist?'+link.find('h3').find('a').get('href').split('&')[1]
        except:continue
        try:numtracks = link.find(attrs={'class':'sidebar'}).text.split(' ')[0]
        except:numtracks='--'
        pl = {"title":playlisttitle, "link":playlistlink, "numtracks":numtracks}
        playlists.append(pl)
    return playlists
   
def ytsArtist(query):
    ''' Get the most famous music of artist from yotube if not found returns VideoList = []'''
    query = query.replace(' ', '+')
    webdata = requests.get("http://www.youtube.com/results?search_query=" + query, verify=False).text
    soupdata = BeautifulSoup(webdata, PARSER)
    VideoList = []
    try:
        for link in soupdata.findAll(attrs={'class':'watch-card'})[0].findAll(attrs={'class':'watch-card-main-col'}):
            videolink = 'http://www.youtube.com/' + link.find('a').get('href')[:21]
            videotitle = link.get('title')
            videoduration = '00:00'
            VideoList.append({'title':videotitle, 'link':videolink, 'duration':videoduration})
        return VideoList
    except:
        return VideoList

def getyttop():
    ''' Get the top 100 music on youtube '''
    playlisturl = "http://www.youtube.com/playlist?list=PLFgquLnL59alcyTM2lkWJU34KtfPXQDaX"
    webdata = requests.get(playlisturl, verify=False).text
    soupdata = BeautifulSoup(webdata, PARSER)
    VideoList = []
    for link in soupdata.findAll(attrs={'class':'pl-video'}):
        # Get info from HTML tags
        videotitle = link.get('data-title')
        videolink = 'http://www.youtube.com/watch?v=' + link.get('data-video-id')
        videoduration = link.find(attrs={'class':'timestamp'}).text
        thumbnailurl = link.find(attrs={'class':'yt-thumb-clip'}).find('img').get('data-thumb')
        VideoList.append({'title': videotitle, 'link': videolink, 
                         'duration': videoduration, 'thumbnail': thumbnailurl})
    return VideoList
    
def artistSearch(query,limit=5): 
    ''' Search artists in discogs.com and return name, 
        image url and url of artist '''
    query = query.replace(' ', '+')
    webdata = requests.get("http://www.discogs.com/search/?q=" + query + "&type=artist", verify=False).text
    soupdata = BeautifulSoup(webdata, PARSER)
    artists = []
    countlimit = 0
    for link in soupdata.findAll(attrs={'class':'card'}):
        # Get info from HTML tags
        url = 'http://www.discogs.com' + link.find('a').get('href')
        name = link.find('h4').find('a').get('title')
        imageurl = link.find('img').get('data-src')
        artists.append({'name': name, 'url': url, 'image': imageurl})
        countlimit += 1
        if countlimit == limit:break
    return artists

def getAlbunsFromArtist(artisturl): 
    ''' Set the artist url from discogs and return 
        the master albuns from artist '''
    webdata = requests.get(artisturl, verify=False).text
    soupdata = BeautifulSoup(webdata, PARSER)
    albuns = []
    # Filter tags with have the class = card and master
    for link in soupdata.findAll(attrs={'class':'card','class': 'master'}):
        # Get info from HTML tags
        name = link.find(attrs = {'class': 'title'}).find('a').text
        url = 'http://www.discogs.com' + link.find(attrs = {'class': 'image'}).find('a').get('href')
        artistname = link.find(attrs = {'class': 'artist'}).find('a').text
        image = link.find(attrs = {'class': 'thumbnail_center'}).find('img').get('data-src')
        year = link.find(attrs = {'class': 'year'}).text
        country = link.find(attrs = {'class': 'country'}).find('span').text 
        recorderlistHTML = link.find(attrs = {'class': 'label'}).findAll('a') # Get a list of HTML tags with recorders info
        recorders = ''
        for i in recorderlistHTML:
            recorders = recorders + i.text + ", "
        # Make a list of dict with the albuns in discogs page
        albuns.append({'name': name, 'url': url, 'artistname': artistname, 
                     'image': image, 'year':year, 'country': country,
                     'recorder': recorders})
    return albuns

def getTracksFromAlbum(albumurl): 
    ''' Set the album url from discogs and return 
        the complete info from album '''
    webdata = requests.get(albumurl, verify=False).text
    soupdata = BeautifulSoup(webdata, PARSER)
    tracks = []
    # Filter tag with have the class = playlist and after find tags that have class = tackslist_track
    soupdataPlaylist = soupdata.find(attrs = {'class': 'playlist'}).findAll(attrs = {'class': 'tracklist_track'})
    # This loop gets the tacklist
    
    for link in soupdataPlaylist:
        tracknum = link.get('data-track-position')
        name = link.find(attrs = {'class': 'tracklist_track_title'}).text
        duration = link.find(attrs = {'class': 'tracklist_track_duration'}).find('span').text
        # Create a list of dict with name of track, number and duration
        tracks.append({'name': name, 'tracknum': tracknum, 'duration': duration})
    
    genlist =  soupdata.find(attrs={'class': 'profile'}).findAll(attrs={'itemprop': 'genre'})[0].findAll('a')
    stylelist = soupdata.find(attrs={'class': 'profile'}).findAll(attrs={'class': 'content'})[1].findAll('a')
    generes = ''
    styles = ''
    for i in genlist: generes = generes + i.text + ', '
    for i in stylelist: styles = styles + i.text + ', '
    albumgenre = generes
    albumstyle = styles
    albumname = soupdata.find(attrs={'class': 'profile'}).find('h1').findAll('span')[1].find('a').text
    albumartist = soupdata.find(attrs={'class': 'profile'}).find('h1').find('span').find('span').get('title')
    albumyear = soupdata.find(attrs={'class': 'profile'}).findAll(attrs={'class': 'content'})[2].findAll('a')[0].text
    coverurl = soupdata.find(attrs={'class': 'thumbnail_center'}).find('img').get('src')
    tracks.append({'genre':albumgenre, 'style':albumstyle, 'albumname': albumname, 
                  'year': albumyear, 'cover': coverurl}) # Create the last dict, with all info of album
    
    return tracks