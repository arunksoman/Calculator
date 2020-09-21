from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
import decimal as d
import math

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
    return validation_string.find(operand)
class HomeScreen(Screen):
    def validate(self):
        operands = ['+', '-', '/', '*', '%']
        for_validation = self.ids.input.text
        print(for_validation)
        check_foroperand = [operand_checker(for_validation, operand) for operand in operands]
        print(check_foroperand)
    def backspace(self, cursor):
        print(cursor)
    def fill_input(self, digit="", operation=""):
        # print(f"Digit: {digit}")
        # print(f"Operation: {operation}")
        if digit is not "":
            self.ids.input.text += digit
        if operation is not "":
            self.ids.input.text += operation
        final_result = str(HomeScreen().evaluate(str(self.ids.input.text)))
        self.ids.result.text = final_result
    def evaluate(self, calc_operation):
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
            return eval(calc_operation)
class CalculatorApp(App):
    sm = ScreenManager()
    def build(self):
        CalculatorApp.sm.add_widget(HomeScreen(name ="homescreen"))
        return CalculatorApp.sm


if __name__ == "__main__":
    substract()
    CalculatorApp().run()