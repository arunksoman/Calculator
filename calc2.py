from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.event import EventDispatcher
from kivy.uix.screenmanager import Screen, ScreenManager
import decimal as d
import math


class MyEventDispatcher(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type('on_test')
        super(MyEventDispatcher, self).__init__(**kwargs)
    def do_something(self, value):
        app = App.get_running_app()
        final_result = str(HomeScreen().evaluate(str(app.sm.get_screen('homescreen').ids.input.text)))
        print(f"Final Result: {final_result}")
        app.sm.get_screen('homescreen').ids.result.text = final_result
        app.sm.get_screen('homescreen').ids.input.focus=True
        self.dispatch('on_test', value)
    def on_test(self, *args):
        print ("I am dispatched", args)

def my_callback(value, *args):
    print("Hello, I got an event!", args)

def substract(num1=1.2, num2=1):
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

class HomeScreen(Screen):
    def validate(self):
        operands = ['+', '-', '/', '*', '%']
        for_validation = self.ids.input.text
        print(for_validation)
        check_foroperand = [operand_checker(for_validation, operand) for operand in operands]
        print(check_foroperand)
        if for_validation != "":
            ev = MyEventDispatcher()
            ev.bind(on_test=my_callback)
            ev.do_something('test')

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
        if not calc_operation.find("-") != -1:
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
    substract()
    CalculatorApp().run()