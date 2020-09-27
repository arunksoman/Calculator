from kivy.app import App
from kivy.event import EventDispatcher
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.animation import Animation
import decimal as d
import math
import re


class KeypressListener(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type('on_test')
        super(KeypressListener, self).__init__(**kwargs)
    def calculation_from_keyboard(self, value):
        app = App.get_running_app()
        print("value: ", app.sm.get_screen('homescreen').ids.input.text)
        final_result = str(HomeScreen().evaluate(str(value)))
        print(f"Final Result: {final_result}")
        app.sm.get_screen('homescreen').ids.input.focus=True
        app.sm.get_screen('homescreen').ids.result.text = final_result
        self.dispatch('on_test', value)
    def on_test(self, *args):
        pass

def my_callback(value, *args):
    # print("Hello, I got an event!", args)
    pass

def substract(num1, num2):
    if num2 is not isinstance(num2, float):
        num2 = float(num2)
    len_num2 = len(str(num2).split('.')[1])
    quantization_num = "{}.{}".format(0, "".zfill(len_num2))
    unquantized_result = d.Decimal(num1) - d.Decimal(num2)
    quantized_result = unquantized_result.quantize(d.Decimal(quantization_num))
    print(quantized_result)
    return quantized_result

def operand_checker(validation_string, operand):
    if validation_string.find(operand) != -1:
        return True
    return False


class NumberInput(TextInput):
        r = re.compile(r'^[-+]*?\d*[\*,\-,/,., +]?\d*$')
        def insert_text(self, substring, from_undo=False):
            r = self.r
            app = App.get_running_app()
            cursor_col = app.sm.get_screen('homescreen').ids.input.cursor_col
            if r.match(substring):
                print("Substring: ", substring)
                print(cursor_col)
                print("String: ", substring)
                s = substring
                app.sm.get_screen('homescreen').ids.warning.text = ""
                ev = KeypressListener()
                ev.bind(on_test=my_callback)
                ev.calculation_from_keyboard('test')
                
            else:
                app.sm.get_screen('homescreen').ids.warning.text = "[b][color=ff0000]Please Enter Valid number[/color][/b]"
                s = substring.replace(substring, "")
            return super(NumberInput, self).insert_text(s, from_undo=from_undo)
class HomeScreen(Screen):
    def backspace(self, cursor):
        print(cursor)
        if cursor != (0, 0):
            calculation = self.ids.input.text
            calculation = calculation.replace(calculation[cursor[0] - 1], "")
            print(calculation)
            self.ids.input.text = calculation
            final_result = str(HomeScreen().evaluate(str(self.ids.input.text)))
            self.ids.result.text = final_result

    def fill_input(self, digit="", operation=""):
        if digit != "":
            self.ids.input.text += digit
        if operation != "":
            self.ids.input.text += operation
        final_result = str(HomeScreen().evaluate(str(self.ids.input.text)))
        self.ids.result.text = final_result

    def evaluate(self, calc_operation):
        if calc_operation == "":
            return ""
        if calc_operation.endswith(('+', '-', '*', '/', '%')):
            return calc_operation[:-1]

        #Fixed number cannot start with - symbol
        if not calc_operation.find("-") != -1 or calc_operation.startswith('-'):
            try:
                result = eval(calc_operation)
                return result
            except Exception:
                return "Error"
        else:
            # for now do same
            num1, num2 = calc_operation.split('-')
            num1, num2 = float(num1), float(num2)
            return substract(num1, num2)

class CalculatorApp(App):
    sm = ScreenManager()
    def build(self):
        CalculatorApp.sm.add_widget(HomeScreen(name ="homescreen"))
        return CalculatorApp.sm


if __name__ == "__main__":
    Window.size = (440, 600)
    CalculatorApp().run()