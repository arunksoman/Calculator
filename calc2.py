from kivy.app import App
from kivy.event import EventDispatcher
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock
import decimal as d
import re
import calculation

def show_keyboard(event):
    app = App.get_running_app()
    app.sm.get_screen('homescreen').ids.input.focus=True

    
def operand_checker(validation_string):
    print(f"Validation String {validation_string}")
    operand_list = ['+', '-', '*', '/', '%']
    print("Hai")
    return [False if validation_string.find(operand) == -1 else True for operand in operand_list]


class NumberInput(TextInput):
        r = re.compile(r'^[-+]*?\d*[\*,\-,/,., +,(,), %]?\d*$')
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
            else:
                app.sm.get_screen('homescreen').ids.warning.text = "[b][color=ff0000]Please Enter Valid number[/color][/b]"
                s = substring.replace(substring, "")
            return super(NumberInput, self).insert_text(s, from_undo=from_undo)
class HomeScreen(Screen):
    def validate(self):
        calc_operation = self.ids.input.text
        if calc_operation.count('(') != calc_operation.count(')'):
            self.ids.warning.text = "[b][color=ff0000]Bracket count mismatching[/color][/b]"
        else:
            self.ids.warning.text = ""
        # print("Hai")
        print("value: ", self.ids.input.text)
        final_result = str(HomeScreen().evaluate(str(self.ids.input.text)))
        print(f"Final Result: {final_result}")
        self.ids.input.focus=True
        self.ids.result.text = final_result

    def clear_result(self):
        self.ids.result.text = ""
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
            # return calc_operation[:-1]
        if calc_operation.endswith(('+', '-', '*', '/', '%', '(')):
            return calc_operation[:-1]
        # try:
        # result = eval(calc_operation)
        # splitted_operation = list(filter(lambda x: x, re.split(r'([-+*/%()])|\s+', calc_operation)))
        # if operand_checker(calc_operation).count(True) > 1:
        #     return "To Do"
        bracket_matching = re.findall("[^()]+", calc_operation)
        print(bracket_matching)
        operation_list = []
        for operation in bracket_matching:
            if not (operation.endswith(('+', '-', '*', '/', '%')) or operation.startswith(('+', '-', '*', '/', '%'))):
                if operand_checker(operation).count(True) == 1 or operand_checker(operation).count(False) == 5:
                    operation = eval(operation)
                else:
                    splitted_operation = list(filter(lambda x: x, re.split(r'([-+*/%()])|\s+', operatioin)))
                    for item in operation:
                        print(item)
                    return "To Do"
            operation_list.append(operation)
        new_operation_str = ''.join([str(operation) for operation in operation_list])
        splitted_operation = list(filter(lambda x: x, re.split(r'([-+*/%()])|\s+', new_operation_str)))
        print(operand_checker(new_operation_str))
        if operand_checker(new_operation_str).count(False) == 5:
            return new_operation_str
        if operand_checker(new_operation_str).count(True) == 1:
            return eval(new_operation_str)
        # except Exception:
        #     return "Error"
            
class CalculatorApp(App):
    sm = ScreenManager()
    Clock.schedule_interval(show_keyboard, 0.2)
    def build(self):
        CalculatorApp.sm.add_widget(HomeScreen(name ="homescreen"))
        return CalculatorApp.sm


if __name__ == "__main__":
    Window.size = (440, 600)
    CalculatorApp().run()