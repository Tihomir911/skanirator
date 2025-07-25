from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
import cv2
import numpy as np
import requests
from pyzbar.pyzbar import decode

class ScannerLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            buf = cv2.flip(frame, 0).tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.ids.camera_display.texture = image_texture

            decoded_objs = decode(frame)
            for obj in decoded_objs:
                self.show_result(obj.data.decode())

    def show_result(self, data):
        popup = Popup(title='Результат',
                      content=TextInput(text=data, readonly=True),
                      size_hint=(0.8, 0.3))
        popup.open()

class SkaniratorApp(App):
    def build(self):
        return ScannerLayout()

if __name__ == '__main__':
    SkaniratorApp().run()