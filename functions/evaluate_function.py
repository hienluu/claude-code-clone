from google.genai import types
from calculator.pkg.calculator import Calculator


schema_evaluate = types.FunctionDeclaration(
    name="evaluate",
    description="Evaluate a math expression",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "expression": types.Schema(
                type=types.Type.STRING,
                description="A mathematical expression",
            )
        },
        required=["expression"]
    )
    
)

def evaluate(working_directory : str, expression:str="") -> str:
    """
    Perform the evaluation of the given math expression
    """
    
    print(f"evaluate with expression: {expression}")
    calc = Calculator()

    result = calc.evaluate(expression)
    print(f"evaluate with result: {result}")