from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the content of a files in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to get content from, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
    
)

def get_file_content(working_directory, file_path):
    import os

    try:
        # Get the absolute path of the working directory
        working_directory_abs = os.path.abspath(working_directory)
        
        # full path of the target file
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))

        # Will be True or False
        valid_target_file = os.path.commonpath([working_directory_abs, target_file]) == working_directory_abs

        if not valid_target_file:
            raise ValueError(f"Error: Target file {target_file} is outside the permitted working directory")

        if not os.path.isfile(target_file):
            raise FileNotFoundError(f"Error: File {file_path} does not exist")
        
        MAX_CHARS = 10000  # Define the maximum number of characters to read
        with open(target_file, 'r') as f:
            content = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content
    except Exception as e:        
        return f"Error: accessing file {file_path}: {str(e)}"