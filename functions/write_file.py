from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a file in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write content to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            )
        },
        required=["file_path", "content"]
    )
   
)

def write_file(working_directory:str, file_path:str, content:str) -> str:
    """
    Write content to a file in a specified directory relative to the working directory
    """
    import os

    try:
        # Get the absolute path of the working directory
        working_directory_abs = os.path.abspath(working_directory)
        
        # full path of the target file
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))

        # Will be True or False
        valid_target_file = os.path.commonpath([working_directory_abs, target_file]) == working_directory_abs

        if not valid_target_file:
            raise ValueError(f"Error: Cann't write to {target_file} as it is outside the permitted working directory")

        if os.path.isdir(target_file):
            raise FileNotFoundError(f"Error: Cannot write to {file_path} as it is a directory")
        
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, 'w') as f:
            f.write(content)

        return f'Successfully wrote to file "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:        
        return f"Error: accessing file {file_path}: {str(e)}"