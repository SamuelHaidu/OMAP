import glob
import json
import pafy
import os
import os.path
from kivy.logger import Logger
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.pagelayout import PageLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from os.path import abspath, dirname
from kivy.metrics import dp
from playlistpopup import AddPlaylistPopup, AddPlaylistFromYTPopup
scriptfolder = dirname(abspath(__file__))
sdcard = '/mnt/sdcard/'
class ThumbButton(ButtonBehavior, Image):
    
    def __init__(self, **kwargs):
        self.thumb = scriptfolder + '/images/icon.png'
        super(ThumbButton, self).__init__(**kwargs)
        self.source = self.thumb
        self.allow_stretch = True
    
    def on_press(self):
        pass
    def on_release(self):
        pass

class PlaylistButton(BoxLayout):
    callback = None
    def __init__(self, title, decription ,videolist, thumb=None, **kwargs):
        super(PlaylistButton, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (1, None)
        self.padding = 5
         
        self.thumblayout = BoxLayout(padding=5)
        self.thumblayout.size_hint_x = 0.3
        self.add_widget(self.thumblayout)
        self.labellayout = BoxLayout(orientation='vertical')
        self.add_widget(self.labellayout)
         
        self.thumb = ThumbButton()
        self.thumb.bind(on_press=self._callback)
        if thumb: self.thumb.source=thumb
        self.thumblayout.add_widget(self.thumb)
         
        self.title = '[b]'+title+'[/b]'
        self.description = decription
        self.videolist = videolist
         
        self.label_title = Label(text=self.title, markup=True)
        self.label_title.font_size = '16dp'
        self.label_title.size_hint = (1, None)
        self.label_title.height = 16
        self.labellayout.add_widget(self.label_title)
         
        self.label_description =  Label(text=self.description, valign='top', multiline=True)
        self.label_description.bind(size=self.label_description.setter('text_size'))
        self.label_description.shorten = False
        self.label_description.shorten_from = 'right'
        self.label_description.halign = 'left'
        self.labellayout.add_widget(self.label_description)
    
    def set_thumb(self, thumb):
        self.thumb.source=thumb
    
    def _callback(self, instance):
        if self.callback: self.callback(self.videolist)

class PlaylistScreen(ScrollView):
     call = None
     
     def __init__(self, **kwargs):
         super(PlaylistScreen, self).__init__(**kwargs)
         self.size_hint=(1, 1)
         with self.canvas.before:
             Color(0.2, 0.2, 0.2, 1)
             self.rect = Rectangle(size=self.size,
                                   pos=self.pos)
         self.bind(pos=self.update_rect, size=self.update_rect)
         
         self.playlistgrid = GridLayout(cols=1, spacing=5, size_hint_y=None)
         self.playlistgrid.bind(minimum_height=self.playlistgrid.setter('height'))
         
         self.bt_add_playlist = PlaylistButton('Add Playlists',
                                               'Add playlists manualy',
                                               [],
                                               scriptfolder+'/images/playlist_add.png')
         self.bt_add_playlist.callback = self.add_playlist
         
         self.bt_add_playlistYT = PlaylistButton('Add YT Playlists',
                                                 'Add playlists automatically from YouTube',
                                                 [],
                                                 scriptfolder+'/images/playlistYT_add.png')
                                                 
         self.bt_add_playlistYT.callback = self.add_playlistYT
         
         self.popup_addplaylist = AddPlaylistPopup(self)
         self.popup_addplaylistYT = AddPlaylistFromYTPopup(self)
         
         self.update_playlists()
         self.add_widget(self.playlistgrid)
         
     def update_playlists(self):
         self.playlistgrid.clear_widgets(children=None)
         self.playlistgrid.add_widget(self.bt_add_playlist)
         self.playlistgrid.add_widget(self.bt_add_playlistYT)
         os.chdir(sdcard+'OMAP/Playlists')
         self.playlists = glob.glob('*.json')
         
         for i in range(len(self.playlists)):
             self.file_data = open(self.playlists[i])# Open File
             try:self.data = json.load(self.file_data)# Get Json Data
             except: 
                 Logger.exception('Cant load ', self.playlists[i])
                 continue
             
             if self.data['type']=='local': 
                 self.playlist = PlaylistButton(self.data['title'],#Insert in Button
                                               self.data['description'],
                                               self.data['tracks'])
                 if os.path.isfile(self.data['thumb']): 
                     self.playlist.set_thumb(self.data['thumb'])
                 self.playlist.callback = self._call
                 self.playlistgrid.add_widget(self.playlist)
             
             elif self.data['type']=='yt':
                  self.ppl = pafy.get_playlist(self.data['link'])# Get YT Playlist
                  self.tracks = []                 
                  for item in self.ppl['items']:# Get Tracks
                      self.tracks.append({'title':item['pafy'].title, 'link':item['pafy'].videoid})
                  
                  self.playlist = PlaylistButton(self.data['title'],#instance of button
                                                 self.data['description'],
                                                 self.tracks)
                  
                  if os.path.isfile(self.data['thumb']):
                      self.playlist.set_thumb(self.data['thumb']) # Put the thubnail
                  self.playlist.callback = self._call
                  self.playlistgrid.add_widget(self.playlist)                 
                 
                 
         os.chdir(scriptfolder)
         
     def _call(self, videos):
         if self.call: self.call(videos)
     
     def add_playlist(self, vl):
         self.popup_addplaylist.open()
     def add_playlistYT(self, vl):
         self.popup_addplaylistYT.open()
     def update_rect(instance, value, a):
         instance.rect.pos = instance.pos
         instance.rect.size = instance.size