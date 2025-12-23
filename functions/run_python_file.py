from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a Python file in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the Python file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An array of arguments to pass to the Python file",
                items=types.Schema(type=types.Type.STRING),
            )
        },
        required=["file_path"]
    )
    
)

def run_python_file(working_directory, file_path, args=None):
    import os

    try:
        # Get the absolute path of the working directory
        working_directory_abs = os.path.abspath(working_directory)
        
        # full path of the target file
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))

        # Will be True or False
        valid_target_file = os.path.commonpath([working_directory_abs, target_file]) == working_directory_abs

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        # If the file name doesn't end with .py, return an error string:
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        # execute the python file and capture the output
        command = ["python", target_file]
        if args:
            command.extend(args)
    
        import subprocess
        result = subprocess.run(command, capture_output=True, text=True,
                                cwd=working_directory_abs, timeout=30)
        
        if result.returncode != 0:
            return f'Error Process exited with code {result.returncode}'
        else:
            return f'STDOUT: {result.stdout}\nSTDERR: {result.stderr}'
    except Exception as e:        
        return f"Error: executing Python file {file_path}: {str(e)}"