from kivy.app import App  # main app
from kivy.lang import Builder # python file to kv file connection
from kivy.uix.screenmanager import ScreenManager, Screen
# from kivy.uix.gridlayout import GridLayout # not needed since the objects are being added from kivy App
import json, glob
from datetime import datetime
from pathlib import Path
import random
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

Builder.load_file('design.kv')

class LoginScreen(Screen): # same as kv name
    def sign_up(self):
        self.manager.current = "signup_screen" # change screen to signup_screen name kv
        print("Sign up button pressed")
    def login(self,uname,pword):
        # check the file to make sure it is there
        with open("Other/users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.current ="login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong username or password!"
    pass

class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open("Other/users.json") as file:
            users = json.load(file)
            users[uname] = {'username':uname,'password':pword,
                            'created':datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
        with open("Other/users.json","w") as file:
            json.dump(users,file)
        self.manager.current = "sign_up_screen_success"
    pass

class SignUpScreenSuccess(Screen):
    def back_to_login(self):
        # here we can change the transitiion to the login screen back to right
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
    pass

# For logout button
# REMEMBER ButtonBehaviour must be first for the logout button to work
class ImageButton(ButtonBehavior,HoverBehavior,Image):
    pass

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    def get_quote(self,feel):
        feel = feel.lower()
        available_feelings = glob.glob("Other/Quotes/*txt")
        available_feelings = [Path(filename).stem for filename in
                              available_feelings]
        if feel in available_feelings:
            with open(f"Other/Quotes/{feel}.txt",encoding="utf8") as file:
                quotes = file.readlines()
            self.ids.displayed_text.text = random.choice(quotes)
        else:
            self.ids.displayed_text.text = "Please try a valid feeling"

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget() # The Object is being initialized

if __name__ == "__main__":
    MainApp().run()
