from kivy.app import App
from kivy.event import EventDispatcher
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock
import re
# import calculation

def show_keyboard(event):
    app = App.get_running_app()
    app.sm.get_screen('homescreen').ids.input.focus=True

    
def operand_checker(validation_string):
    # print(f"Validation String {validation_string}")
    operand_list = ['+', '-', '*', '/', '%']
    # print("Hai")
    return [False if validation_string.find(operand) == -1 else True for operand in operand_list]


class NumberInput(TextInput):
        r = re.compile(r'^[-+]*?\d*[\*,\-,/,., +,(,), %]?\d*$')
        def insert_text(self, substring, from_undo=False):
            r = self.r
            app = App.get_running_app()
            cursor_col = app.sm.get_screen('homescreen').ids.input.cursor_col
            if r.match(substring):
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
        final_result = str(HomeScreen().evaluate(str(self.ids.input.text)))
        self.ids.input.focus=True
        self.ids.result.text = final_result

    def clear_result(self):
        self.ids.result.text = ""

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
        if calc_operation.endswith(('+', '-', '*', '/', '%', '(')):
            return calc_operation[:-1]
        try:
            if operand_checker(calc_operation)[3]:
                print("Operation has division")
                splitted_operation = list(filter(lambda x: x, re.split(r'([-+*/%()])|\s+', calc_operation)))
                print("Splitted Operation: ", splitted_operation)
                for index, item in enumerate(splitted_operation):
                    if item == '/':
                        print(splitted_operation[index + 1])
                        if splitted_operation[index + 1] == "0":
                            # self.ids.warning.text = "[b][color=ff0000]Cannot Divide by Zero[/color][/b]"
                            return "[b][color=ff0000]Cannot Divided by Zero.[/b][/color]"
                        splitted_operation[index - 1] = "({}".format(splitted_operation[index-1])
                        splitted_operation[index + 1] = "{})".format(splitted_operation[index+1])
                calc_operation = "".join(splitted_operation)
                # print("Clac Operation with Brackets: ", calc_operation)
            bracket_matching = re.findall("[^()]+", calc_operation)
            print("bracket_matching: ",bracket_matching)
            operation_list = []
            count = 0
            for operation in bracket_matching:
                if not (operation.endswith(('+', '-', '*', '/', '%')) or operation.startswith(('+', '-', '*', '/', '%'))):
                    if operand_checker(operation).count(True) == 1 or operand_checker(operation).count(False) == 5:
                        operation = eval(operation)
                    else:
                        splitted_operation = list(filter(lambda x: x, re.split(r'([-+*/%()])|\s+', operation)))
                        operation = ""
                        result = ""
                        for index, item in enumerate(splitted_operation):
                            print(f"item: {item}")
                            if index < 3:
                                operation += item
                            if index >= 3:
                                # print("I am in else")
                                operation += item
                                # item = str(eval(operation))
                            if index % 2 == 0 and not operation.endswith(('+', '-', '*', '/', '%')):
                                # print(f"Operation: {operation}")
                                result = str(eval(operation))
                                print(40*"*")
                                operation =  result
                            print(f"result: {result}")
                            print(f"index: {index}")
                            print(f"operation: {operation}")
                        print(f"result: {result}")
                        return result
                operation_list.append(operation)
            new_operation_str = ''.join([str(operation) for operation in operation_list])
            print(f"New Operation: {new_operation_str}")
            splitted_operation = list(filter(lambda x: x, re.split(r'([-+*/%()])|\s+', new_operation_str)))
            # print(operand_checker(new_operation_str))
            if operand_checker(new_operation_str).count(True) == 1:
                result = eval(new_operation_str)
                print(f"Result1: {result}")
                return result
            else:
                splitted_operation = list(filter(lambda x: x, re.split(r'([-+*/%()])|\s+', new_operation_str)))
                operation = ""
                result = ""
                for index, item in enumerate(splitted_operation):
                    print(f"item: {item}")
                    if index < 3:
                        operation += item
                    if index >= 3:
                        # print("I am in else")
                        operation += item
                        # item = str(eval(operation))
                    if index % 2 == 0 and not operation.endswith(('+', '-', '*', '/', '%')):
                        # print(f"Operation: {operation}")
                        result = str(eval(operation))
                        print(40*"*")
                        operation =  result
                    print(f"result: {result}")
                    print(f"index: {index}")
                    print(f"operation: {operation}")
                print(f"result: {result}")
                return str(eval(str(operation)))
        except Exception:
            return "Error"
            
class CalculatorApp(App):
    sm = ScreenManager()
    Clock.schedule_interval(show_keyboard, 0.2)
    def build(self):
        CalculatorApp.sm.add_widget(HomeScreen(name ="homescreen"))
        return CalculatorApp.sm


if __name__ == "__main__":
    Window.size = (440, 600)
    CalculatorApp().run()