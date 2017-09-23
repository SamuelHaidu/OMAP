from kivy.core.audio import SoundLoader

class MPlayer():
     def __init__(self):
         self.length = 0
         self.state = 'stop'
         self.savetime = 0.0
         self.pause = False
         
     def load(self, audio):
         self.media = SoundLoader().load(audio)
         self.length = int(self.media.length)
         if self.length == -1: self.lenght = 3000
     def play(self):
         if self.pause == False:
             self.media.play()
             self.state = 'play'
         elif self.pause == True:
             self.media.play()
             self.media.seek(self.savetime)
             self.pause = False
         
     def pause(self):
         if self.state == 'play':
             self.savetime = self.media.get_pos()
             self.media.stop()
             self.state = 'stop'
             self.pause = True
         elif self.state == 'stop': return
         
     def stop(self):
         self.media.stop()
         self.state = 'stop'
     
     def seek(self, position):
         self.media.seek(position)
             
     def get_pos(self):
         return self.media.get_pos()
         
     def set_mute(self):pass
     def set_unmute(self):pass
     def set_volume(self):pass
     