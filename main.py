from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from hoverable import HoverBehavior
import json, glob
from datetime import datetime
from pathlib import Path
import random

Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def login(self,uname,pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong Username or Password!"

class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self,user,pwd):
        with open("users.json") as file:
            users = json.load(file)
        if user:
            if user not in users:
                # add user to dictionary
                datetime_format = "%Y-%m-%d %H:%M:%S.%f"
                users[user] = {'username': user, 'password': pwd, 'created': datetime.now().strftime(datetime_format)}
                # overwrite users file
                with open("users.json", "w") as file:
                    json.dump(users, file)
                self.manager.current = "sign_up_screen_success"
            else:
                self.ids.wrong_signup.text = "Username already exists"
        else:
            self.ids.wrong_signup.text = "Enter a valid username"

class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    def get_quote(self,feel):
        feel = feel.lower()
        available_feelings = glob.glob("quotes/*txt")

        available_feelings = [Path(filename).stem for filename in available_feelings]

        if feel in available_feelings:
            with open(f"quotes/{feel}.txt",encoding="utf8") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling"

class ImageButton(ButtonBehavior,HoverBehavior,Image):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
