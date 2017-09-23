from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from shutil import copy2
from os.path import abspath, dirname
import os
import json
scriptfolder = dirname(abspath(__file__))
sdcard = '/mnt/sdcard/'
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
class FilePopup(Popup):
    def __init__(self, **kwargs):
        super(FilePopup, self).__init__(**kwargs)
        self.title = 'Select a File'
        self.layout = BoxLayout(orientation='vertical')
        self.btlayout = BoxLayout(orientation='horizontal', size_hint=(1,0.15))
        
        self.FChooser = FileChooserListView(path='/mnt/sdcard/')
        self.layout.add_widget(self.FChooser)
        
        self.bt_load = Button(text='Load')
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
    def __init__(self, playlistscreen,**kwargs):
        super(AddPlaylistPopup, self).__init__(**kwargs)
        self.popupcontent = BoxLayout(orientation='vertical')
        self.btlayout = BoxLayout(orientarion='horizontal')
        
        self.thumbname = '' 
        self.playlist_data = {
        "title":"",
        "description":"",
        "type":"local",
        "thumb": "",
        "tracks":[]
        }
        self.playlistscreen = playlistscreen
        self.txtbx_playlisttitle = TextInput(text='Playlist Title')
        self.popupcontent.add_widget(self.txtbx_playlisttitle)
        
        self.txtbx_description = TextInput(text='Playlist description')
        self.popupcontent.add_widget(self.txtbx_description)
        
        self.txtbx_musictitle = TextInput(text='Music Title')
        self.popupcontent.add_widget(self.txtbx_musictitle)
        
        self.txtbx_musiclink = TextInput(text='YouTube Video Link/ID')
        self.popupcontent.add_widget(self.txtbx_musiclink)
         
        self.bt_addmusic = Button(text='Add Music')
        self.bt_addmusic.bind(on_press=self.bt_addmusic_click)
        self.btlayout.add_widget(self.bt_addmusic)
         
        self.bt_save = Button(text='Save')
        self.bt_save.bind(on_press=self.bt_save_click)
        self.btlayout.add_widget(self.bt_save)
         
        self.bt_thumb = ThumbButton()
        self.bt_thumb.bind(on_press=self.bt_thumb_click)
        self.btlayout.add_widget(self.bt_thumb)
        self.popupcontent.add_widget(self.btlayout)
         
        self.bt_close = Button(text='Close')
        self.bt_close.bind(on_press=self.dismiss)
        self.popupcontent.add_widget(self.bt_close)         
        
        self.filepop = FilePopup()
        self.filepop.bind(on_dismiss=self.load_image)
        self.content = self.popupcontent
    
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
                  sdcard+'OMAP/Playlists/'+self.playlist_data['title'].replace(' ','_')+'.png')
        except: pass
        self.playlist_data['thumb'] = self.playlist_data['title'].replace(' ', '_')+'.png'
        self.jsondata = json.dumps(self.playlist_data, sort_keys=True, indent=4, separators=(',', ': '))
        self.fname = self.playlist_data['title'].replace(' ', '_') + '.json'
        self.playlistfile = open(sdcard+'OMAP/Playlists/'+self.fname, 'w')
        self.playlistfile.write(self.jsondata)
        self.playlistfile.close()
        self.dismiss()
        self.playlistscreen.update_playlists()
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
    def __init__(self, playlistscreen,**kwargs):
        super(AddPlaylistFromYTPopup, self).__init__(**kwargs)
        self.popupcontent = BoxLayout(orientation='vertical')
        self.btlayout = BoxLayout(orientarion='horizontal')
        
        self.thumbname = '' 
        self.playlist_data = {
        "title":"",
        "description":"",
        "type":"yt",
        "thumb": "",
        "link":''
        }
        self.playlistscreen = playlistscreen
        self.txtbx_playlisttitle = TextInput(text='Playlist Title')
        self.popupcontent.add_widget(self.txtbx_playlisttitle)
        
        self.txtbx_description = TextInput(text='Playlist description')
        self.popupcontent.add_widget(self.txtbx_description)
        
        self.txtbx_playlistlink = TextInput(text='YouTube Playlist Link')
        self.popupcontent.add_widget(self.txtbx_playlistlink)
         
        self.bt_save = Button(text='Save')
        self.bt_save.bind(on_press=self.bt_save_click)
        self.btlayout.add_widget(self.bt_save)
         
        self.bt_thumb = ThumbButton()
        self.bt_thumb.bind(on_press=self.bt_thumb_click)
        self.btlayout.add_widget(self.bt_thumb)
        self.popupcontent.add_widget(self.btlayout)
         
        self.bt_close = Button(text='Close')
        self.bt_close.bind(on_press=self.dismiss)
        self.popupcontent.add_widget(self.bt_close)         
        
        self.filepop = FilePopup()
        self.filepop.bind(on_dismiss=self.load_image)
        self.content = self.popupcontent
    
    def bt_save_click(self,instance):
        self.playlist_data['title'] = self.txtbx_playlisttitle.text
        self.playlist_data['description'] = self.txtbx_description.text
        try: 
            copy2(self.filepop.selection, 
                  sdcard+'OMAP/Playlists/'+self.playlist_data['title'].replace(' ','_')+'.png')
        except: pass
        self.playlist_data['thumb'] = self.playlist_data['title'].replace(' ','_')+'.png'
        self.playlist_data['link'] = self.txtbx_playlistlink.text
        self.fname = self.playlist_data['title'].replace(' ', '_') + '.json'
        self.jsondata = json.dumps(self.playlist_data, sort_keys=True, 
                                   indent=4, 
                                   separators=(',', ': '))
        self.playlistfile = open(sdcard+'OMAP/Playlists/'+self.fname, 'w')
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
           
class TestApp(App):
    def build(self):
        self.bt = Button(text='popup')
        self.bt.bind(on_press=self.on_press)
        self.pop = AddPlaylistFromYTPopup(self)
        return self.bt
    
    def on_press(self, instance):
        self.pop.open()

if __name__ == "__main__":
    TestApp().run()