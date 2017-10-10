import os
from os.path import abspath, dirname
scriptfolder = dirname(abspath(__file__))
os.chdir(scriptfolder)
import json
import __main__
from kivy.app import App
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.metrics import dp
from shutil import copy2
from glob import glob

PLAYLISTS_PATH = __main__.PLAYLIST_PATH
FCHOOSER_DEFALT = '/storage/sdcard0'

class ErrorPopup(Popup):
    
    def __init__(self, text,**kwargs):
        super(ErrorPopup, self).__init__(**kwargs)
        self.size_hint=(0.7,0.3)
        if not self.title == 'INFO': self.title = "ERROR"; self.size_hint=(1,0.5)
        self.label_error = Label(text=text, valign='top', multiline=True, size_hint=(1,1))
        self.label_error.bind(size=self.label_error.setter('text_size'))
        self.label_error.halign = 'left'
        self.content = self.label_error
        

class ThumbButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ThumbButton, self).__init__(**kwargs)
        self.source = scriptfolder+'/images/add_image.png'
        self.allow_stretch = True
        
    def on_press(self):
        pass

    def on_release(self):
        pass
    
    def set_img(self, img):
        self.source = img

class FolderPopup(Popup):
    def __init__(self, **kwargs):
        super(FolderPopup, self).__init__(**kwargs)
        self.title = 'Select a Folder'
        self.layout = BoxLayout(orientation='vertical')
        self.btlayout = BoxLayout(orientation='horizontal', size_hint=(1,0.15))
        
        self.FChooser = FileChooserListView(path=FCHOOSER_DEFALT)
        self.layout.add_widget(self.FChooser)
        
        self.bt_load = Button(text='Select')
        self.bt_load.bind(on_press=self.bt_load_click)
        self.btlayout.add_widget(self.bt_load)
        
        self.bt_calcel = Button(text='Calcel')
        self.bt_calcel.bind(on_press=self.bt_calcel_click)
        self.btlayout.add_widget(self.bt_calcel)
        self.layout.add_widget(self.btlayout)
        self.content = self.layout
        self.selection = ''
    
    def bt_load_click(self, instance):
        print self.FChooser.path
        self.selection = self.FChooser.path
        self.dismiss()
    def bt_calcel_click(self, instance):
        self.selection = ''
        self.dismiss()
        
class FilePopup(Popup):
    def __init__(self, **kwargs):
        super(FilePopup, self).__init__(**kwargs)
        self.title = 'Select a File'
        self.layout = BoxLayout(orientation='vertical')
        self.btlayout = BoxLayout(orientation='horizontal', size_hint=(1,0.15))
        
        self.FChooser = FileChooserListView(path=FCHOOSER_DEFALT)
        self.layout.add_widget(self.FChooser)
        
        self.bt_load = Button(text='Open')
        self.bt_load.bind(on_press=self.bt_load_click)
        self.btlayout.add_widget(self.bt_load)
        
        self.bt_calcel = Button(text='Calcel')
        self.bt_calcel.bind(on_press=self.bt_calcel_click)
        self.btlayout.add_widget(self.bt_calcel)
        self.layout.add_widget(self.btlayout)
        self.content = self.layout
        self.selection = ''
    
    def bt_load_click(self, instance):
        self.selection = self.FChooser.selection[0]
        self.dismiss()
    def bt_calcel_click(self, instance):
        self.selection = ''
        self.dismiss()
                
class AddPlaylistPopup(Popup):
    title = 'Add Playlist'
    def __init__(self, **kwargs):
        super(AddPlaylistPopup, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(350)
        self.mainlayout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(300))
        self.img_title_decri_layout = BoxLayout(orientarion='horizontal', size_hint_y=None)
        self.img_title_decri_layout.height = dp(120)
        self.title_descri_layout = BoxLayout(orientation='vertical')
        self.bt_add_save_layout = BoxLayout(orientarion='horizontal', size_hint_y=None)
        self.bt_add_save_layout.height = dp(46)
        
        self.thumbname = '' 
        self.playlist_data = {
        "title":"",
        "description":"",
        "type":"local",
        "thumb": "",
        "tracks":[]
        }
        
        
        # Thumbnail
        self.bt_thumb = ThumbButton()
        self.bt_thumb.size_hint = (0.46,1)
        self.bt_thumb.bind(on_press=self.bt_thumb_click)
        self.img_title_decri_layout.add_widget(self.bt_thumb)
        self.mainlayout.add_widget(self.img_title_decri_layout)
        # Title And Description
        self.txtbx_playlisttitle = TextInput(text='Playlist Title', size_hint_y=None)
        self.txtbx_playlisttitle.height = dp(32)
        self.title_descri_layout.add_widget(self.txtbx_playlisttitle)
        
        self.txtbx_description = TextInput(text='Playlist description')
        self.title_descri_layout.add_widget(self.txtbx_description)
        self.img_title_decri_layout.add_widget(self.title_descri_layout)
        
        
        #Music Title and Music Link
        self.txtbx_musictitle = TextInput(text='Music Title', size_hint_y=None)
        self.txtbx_musictitle.height = dp(32)
        self.mainlayout.add_widget(self.txtbx_musictitle)
        
        self.txtbx_musiclink = TextInput(text='YouTube Video Link/ID', size_hint_y=None)
        self.txtbx_musiclink.height = dp(32)
        self.mainlayout.add_widget(self.txtbx_musiclink)
         
        self.bt_addmusic = Button(text='Add Music', size_hint_y=None)
        self.bt_addmusic.height = dp(46)
        self.bt_addmusic.bind(on_press=self.bt_addmusic_click)
        self.bt_add_save_layout.add_widget(self.bt_addmusic)
         
        self.bt_save = Button(text='Save', size_hint_y=None)
        self.bt_save.height = dp(46)
        self.bt_save.bind(on_press=self.bt_save_click)
        self.bt_add_save_layout.add_widget(self.bt_save)
        self.mainlayout.add_widget(self.bt_add_save_layout)
        
        self.bt_close = Button(text='Close', size_hint_y=None)
        self.bt_close.height = dp(46)
        self.bt_close.bind(on_press=self.dismiss) 
        self.mainlayout.add_widget(self.bt_close)
        
        self.filepop = FilePopup()
        self.filepop.bind(on_dismiss=self.load_image)
        
        self.content = self.mainlayout
    
    def bt_addmusic_click(self, instance):
        self.musictitle = self.txtbx_musictitle.text
        self.musiclink = self.txtbx_musiclink.text
        self.playlist_data['tracks'].append({'title':self.musictitle,'link':self.musiclink})
        self.txtbx_musictitle.text = ''
        self.txtbx_musiclink.text = ''
    
    def bt_save_click(self,instance):
        self.playlist_data['title'] = self.txtbx_playlisttitle.text
        self.playlist_data['description'] = self.txtbx_description.text
        try: 
            copy2(self.filepop.selection, 
                  PLAYLISTS_PATH+self.playlist_data['title'].replace(' ','_')+'.png')
        except: pass
        self.playlist_data['thumb'] = self.playlist_data['title'].replace(' ', '_')+'.png'
        self.jsondata = json.dumps(self.playlist_data, sort_keys=True, indent=4, separators=(',', ': '))
        self.fname = self.playlist_data['title'].replace(' ', '_') + '.json'
        self.playlistfile = open(PLAYLISTS_PATH+self.fname, 'w')
        self.playlistfile.write(self.jsondata)
        self.playlistfile.close()
        self.dismiss()
        self.playlist_data['tracks'] = []
        
    def bt_thumb_click(self, instance):
        self.filepop.open()
        
    def load_image(self, instance):
        if self.filepop.selection == '':
           return
        else:
           self.bt_thumb.set_img(self.filepop.selection)

class AddPlaylistFromYTPopup(Popup):
    title = 'Add Playlist from Youtube'
    def __init__(self, **kwargs):
        super(AddPlaylistFromYTPopup, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(260)
        self.mainlayout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(350))
        self.img_title_decri_layout = BoxLayout(orientarion='horizontal', size_hint_y=None)
        self.img_title_decri_layout.height = dp(120)
        self.title_descri_layout = BoxLayout(orientation='vertical')
        self.bt_close_save_layout = BoxLayout(orientarion='horizontal', size_hint_y=None)
        self.bt_close_save_layout.height = dp(46)
        
        self.thumbname = '' 
        self.playlist_data = {
        "title":"",
        "description":"",
        "type":"yt",
        "thumb": "",
        "link":''
        }
       
        self.bt_thumb = ThumbButton()
        self.bt_thumb.bind(on_press=self.bt_thumb_click)
        self.img_title_decri_layout.add_widget(self.bt_thumb)
        
        
        self.txtbx_playlisttitle = TextInput(text='Playlist Title',multiline=False)
        self.txtbx_playlisttitle.size_hint_y = None
        self.txtbx_playlisttitle.height = dp(32)
        self.title_descri_layout.add_widget(self.txtbx_playlisttitle)
        
        self.txtbx_description = TextInput(text='Playlist description',multiline=False)
        self.title_descri_layout.add_widget(self.txtbx_description)
        self.img_title_decri_layout.add_widget(self.title_descri_layout)
        self.mainlayout.add_widget(self.img_title_decri_layout)
        
        self.txtbx_playlistlink = TextInput(text='YouTube Playlist Link/ID', multiline=False)
        self.txtbx_playlistlink.size_hint_y = None
        self.txtbx_playlistlink.height = dp(32)
        self.mainlayout.add_widget(self.txtbx_playlistlink)
        
        self.bt_save = Button(text='Save', size_hint_y=None)
        self.bt_save.bind(on_press=self.bt_save_click)
        self.bt_save.height = dp(46)
        self.bt_close_save_layout.add_widget(self.bt_save)
        
        self.bt_close = Button(text='Close', size_hint_y=None)
        self.bt_close.bind(on_press=self.dismiss)
        self.bt_close.height = dp(46)
        self.bt_close_save_layout.add_widget(self.bt_close)
        
        self.mainlayout.add_widget(self.bt_close_save_layout)
        self.content = self.mainlayout
        
        self.filepop = FilePopup()
        self.filepop.bind(on_dismiss=self.load_image)
    
    def bt_save_click(self,instance):
        self.playlist_data['title'] = self.txtbx_playlisttitle.text
        self.playlist_data['description'] = self.txtbx_description.text
        try: 
            copy2(self.filepop.selection, 
                  PLAYLISTS_PATH+self.playlist_data['title'].replace(' ','_')+'.png')
        except: pass
        self.playlist_data['thumb'] = self.playlist_data['title'].replace(' ','_')+'.png'
        self.playlist_data['link'] = self.txtbx_playlistlink.text
        self.fname = self.playlist_data['title'].replace(' ', '_') + '.json'
        self.jsondata = json.dumps(self.playlist_data, sort_keys=True, 
                                   indent=4, 
                                   separators=(',', ': '))
        self.playlistfile = open(PLAYLISTS_PATH+self.fname, 'w')
        self.playlistfile.write(self.jsondata)
        self.playlistfile.close()
                                   
        self.playlist_data['title'] = ''
        self.playlist_data['description'] = ''
        self.playlist_data['thumb'] = ''
        self.playlist_data['link'] = ''
        self.txtbx_playlisttitle.text = 'Playlist Title'
        self.txtbx_description.text = 'Playlist description' 
        self.txtbx_playlistlink.text = 'YouTube Playlist Link'
        self.filepop.selection = ''
        self.dismiss()
    def bt_thumb_click(self, instance):
        self.filepop.open()
        
    def load_image(self, instance):
        if self.filepop.selection == '':
           return
        else:
           self.bt_thumb.set_img(self.filepop.selection)

class PlButtonWidget(ButtonBehavior, BoxLayout):
    def __init__(self, musictitle, musicurl, pltitle, file_location, popup, **kwargs):
        super(PlButtonWidget, self).__init__(**kwargs)
        self.musictitle = musictitle
        self.musicurl = musicurl
        self.pltitle = pltitle
        self.flocation = file_location
        self.popup = popup
        
        self.size_hint_y = None
        self.height = dp(46)
        # Create a label title
        self.label_title = Label(text=self.pltitle, valing='midle')
        self.add_widget(self.label_title)
        
        with self.canvas.before:
            Color(0.2,0.2,0.2,1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
            
    def on_press(self):
        self.canvas.before.clear()
        with self.canvas.before:
            color = Color(0.8, 0.8, 0.8, 1, mode='rgba')
            self.rect = Rectangle(pos=self.pos, size=self.size, color=color)
        
    def on_release(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1, mode='rgba')
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.data = json.load(open(self.flocation ,'r'))
        self.track = {'title': self.musictitle, 'link': self.musicurl}
        self.data['tracks'].append(self.track)
        self.jsondata = json.dumps(self.data, 
                                   sort_keys=True,
                                   indent=4, 
                                   separators=(',', ': '))
        open(self.flocation, 'w').close()
        open(self.flocation, 'w').write(self.jsondata)
        __main__.app.main.pl.PlaylistScreen.update_playlists()
        self.popup.dismiss()
        
class addTrackPopup(Popup):
    title='Add to'
    def __init__(self, videowidget, **kwargs):
        super(addTrackPopup, self).__init__(**kwargs)
        
        self.url = videowidget.url
        self.title = videowidget.title
        
        self.size_hint_y = None
        self.height = dp(260)
        
        self.playlistgrid = GridLayout(cols=1, spacing=1, size_hint=(1,None)) 
        self.playlistgrid.bind(minimum_height=self.playlistgrid.setter('height'))
        
        self.scroll = ScrollView()

        self.scroll.size_hint= (1, 1)
        self.scroll.add_widget(self.playlistgrid)
        
        self.content = self.scroll
        os.chdir(PLAYLISTS_PATH)
        self.playlistfiles = glob('*.json')
        
        for pfile in self.playlistfiles:
            pfile = open(pfile, 'r')
            self.data = json.load(pfile)
            if self.data['type']=='local':
                self.pbutton = PlButtonWidget(self.title, 
                                              self.url, 
                                              self.data['title'], 
                                              PLAYLISTS_PATH+pfile.name, 
                                              self)
                self.playlistgrid.add_widget(self.pbutton)
        
