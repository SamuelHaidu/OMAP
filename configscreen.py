import json
import __main__
from playlistpopup import FolderPopup, ErrorPopup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.app import App
from os.path import abspath, dirname
scriptfolder = dirname(abspath(__file__))

class ConfigScreen(ScrollView):
    def __init__(self, **kwargs):
        super(ConfigScreen, self).__init__(**kwargs)
        self.grid = GridLayout(cols=1, spacing=1, size_hint=(1,None))
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.add_widget(self.grid)
        
        self.image_about = Image(source=scriptfolder+'/images/about.png', 
                                 size_hint_y=None, mipmap=False, 
                                 allow_stretch=True)
        self.image_about.bind(size=self.image_size)
        self.grid.add_widget(self.image_about)
        
        # Button to set the downloads folder
        self.bt_download_folder = Button(text='Set Folder for downloads', 
                                         size_hint_y=None, height='46dp')
        self.bt_download_folder.bind(on_release=self.bt_download_folder_click)
        self.grid.add_widget(self.bt_download_folder)
        
        # Button to set the playslists folder
        self.bt_playlists_folder = Button(text='Set Folder for save playlists', 
                                          size_hint_y=None, height='46dp')
        self.bt_playlists_folder.bind(on_release=self.bt_playlists_folder_click)
        self.grid.add_widget(self.bt_playlists_folder)
    
                            
    def image_size(self, instance, b):
        instance.height = instance.width*0.4297
        
    def bt_download_folder_click(self, instance):
        self.fpopup = FolderPopup(size_hint=(1,0.6))
        self.fpopup.bind(on_dismiss=self.set_folder)
        self.config_type = 'download'
        self.fpopup.open()
        
    def bt_playlists_folder_click(self, instance):
        self.fpopup = FolderPopup(size_hint=(1,0.6))
        self.fpopup.bind(on_dismiss=self.set_folder)
        self.config_type = 'playlist'
        self.fpopup.open()
        
    def set_folder(self, instance):
        if self.fpopup.selection == '': return
        else:
            if self.config_type == 'download':
                with open(scriptfolder+'/internal/config.json') as config_file:
                    config_data = json.load(config_file)
                    config_data['download_path'] = self.fpopup.selection
                    with open(scriptfolder+'/internal/config.json', 'w') as config_file:
                        json_data = json.dumps(config_data, sort_keys=True,
                                               indent=4, separators=(',', ': '))
                        config_file.write(json_data)
                        config_file.close()
            elif self.config_type == 'playlist':
                with open(scriptfolder+'/internal/config.json') as config_file:
                    config_data = json.load(config_file)
                    config_data['playlist_path'] = self.fpopup.selection
                    with open(scriptfolder+'/internal/config.json', 'w') as config_file:
                        json_data = json.dumps(config_data, sort_keys=True,
                                               indent=4, separators=(',', ': '))
                        config_file.write(json_data)
                        config_file.close()
        ErrorPopup('Changes takes effect at next startup ',title='INFO',).open()
