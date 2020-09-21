from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager

class HomeScreen(Screen):
    pass

class CalculatorApp(App):
    sm = ScreenManager()
    def build(self):
        CalculatorApp.sm.add_widget(HomeScreen(name ="homescreen"))
        return CalculatorApp.sm


if __name__ == "__main__":
    CalculatorApp().run()