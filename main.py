import kivy
#from kivy.app import App
#from kivy.uix.button import Button
#from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
#from kivy.uix.gridlayout import GridLayout
#from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.button import MDRectangleFlatButton

from kivy.uix.camera import Camera
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang.builder import Builder
import time


def button_to_camera(instance):
    Myapp.sm.current='camera_window'

class take_pic(FloatLayout):
    
    camera_reference=ObjectProperty()     # will be used for Reference

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        camera_widget=Camera(play=True)
        #camera_widget.resolution=(720,1080)
        #camera_widget.orientation='vertical'
        camera_widget.resolution=(Window.size)
        camera_widget.pos_hint={'center_x':0.5,'center_y':0.5}
        button_widget=MDRectangleFlatButton(text='Search',pos_hint={'center_x': 0.5,'center_y' : 0.1})
        button_widget.bind(on_press=self.capture)
        self.add_widget(camera_widget)
        self.add_widget(button_widget)

        self.camera_reference=camera_widget    #referencing camera_widget(camera object) to camera_refernce

    def capture(self,instance):
        timestr = time.strftime("%Y%m%d_%H%M%S")
        self.camera_reference.export_to_png("IMG_{}.png".format(timestr))
        self.camera_reference.play=False
        #print("Captured")



class pp(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.btn1=MDRectangleFlatButton(text='Camera',pos_hint={'center_x': 0.5,'center_y' : 0.60})
        self.btn2=MDRectangleFlatButton(text='Gallery',pos_hint={'center_x': 0.5,'center_y' : 0.45})
        self.btn1.bind(on_press=button_to_camera)        
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)



class MyprojectApp(MDApp):
    def build(self):
        self.sm=ScreenManager()

        self.button_function=pp()
        screen=Screen(name='front_window')
        screen.add_widget(self.button_function)
        self.sm.add_widget(screen)

        self.camera_function=take_pic()
        screen=Screen(name='camera_window')
        screen.add_widget(self.camera_function)
        self.sm.add_widget(screen)
        
        return self.sm

if __name__=="__main__":
    Myapp=MyprojectApp()        #for reference
    Myapp.run()
    