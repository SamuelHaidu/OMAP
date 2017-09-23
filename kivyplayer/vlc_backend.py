import vlc
from time import sleep
class MPlayer():
     def __init__(self):
         self.instance = vlc.Instance()
         self.player = self.instance.media_player_new()
         self.length = 0
         self.state = 'stop'
     
     def load(self, audio):
         self.media = self.instance.media_new(audio)
         self.player.set_media(self.media)
         self.player.play()
         self.player.audio_set_volume(0)
         sleep(4)
         self.length = (self.player.get_length()/1000)
         self.player.audio_set_volume(100)
         self.player.stop()
         
     def play(self):
         self.player.play()
         self.state = 'play'
     
     def pause(self):
         self.player.pause()
         self.state = 'stop'
         
     def stop(self):
         self.player.stop()
         self.state = 'stop'
     
     def seek(self, position):
         self.player.set_time(int(position*1000))
              
     def get_pos(self):
         return self.player.get_time()/1000
     
     def set_mute(self):
         self.player.audio_set_volume(0)
     
     def set_unmute(self):
         self.player.audio_set_volume(100)
     
     def set_volume(self, volume):
         self.player.audio_set_volume(volume)