
from pkg.calculator import Calculator
from pkg.render import format_json_output

calculator = Calculator()
expression = "2 + 3 * 4"
result = calculator.evaluate(expression)
print(format_json_output(expression, result))
