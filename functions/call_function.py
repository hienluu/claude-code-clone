from .get_files_info import schema_get_files_info
from .get_file_content import schema_get_file_content
from .write_file import schema_write_file
from .run_python_file import schema_run_python_file
from google.genai import types

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, 
                           schema_write_file, schema_run_python_file],
)

def call_function(function_call: types.FunctionCall, verbose=False) -> types.Content:
    function_name = function_call.name
    function_args = function_call.args

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}({function_args})")

    # Dictionary mapping function names to their implementations
    def _get_files_info():
        from .get_files_info import get_files_info
        return get_files_info

    def _get_file_content():
        from .get_file_content import get_file_content
        return get_file_content

    def _write_file():
        from .write_file import write_file
        return write_file

    def _run_python_file():
        from .run_python_file import run_python_file
        return run_python_file

    function_registry = {
        "get_files_info": _get_files_info,
        "get_file_content": _get_file_content,
        "write_file": _write_file,
        "run_python_file": _run_python_file,
    }

    if function_name in function_registry:
        func = function_registry[function_name]()
        function_result = func(working_directory="./calculator", **function_args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],            
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
)