from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
    
)

def get_files_info(working_directory, directory="."):
    import os
    from datetime import datetime

    try:
        # Get the absolute path of the working directory
        working_directory_abs = os.path.abspath(working_directory)
        
        #print(f"Working directory absolute path: {working_directory_abs}")

        # full path of the target directory
        #print(f"directory: {directory}")
        target_dir = os.path.normpath(os.path.join(working_directory_abs, directory))
        #print(f"target_dir: {target_dir}")

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs
        #print(f"valid_target_dir: {valid_target_dir}")

        if not valid_target_dir:
            raise ValueError(f"Error: Target directory {target_dir} is outside the permitted working directory")

        if not os.path.isdir(target_dir):
            raise FileNotFoundError(f"Error: directory {directory} does not exist")
        
        file_metadata = []        
        for entry in os.scandir(target_dir):
            file_type = "True" if entry.is_dir() else "False"
            file_size = entry.stat().st_size
            file_metadata.append(f"- {entry.name}: file_size={file_size}, id_dir={file_type}")

        return "\n".join(file_metadata)
    except Exception as e:        
        return f"Error: accessing directory {directory}: {str(e)}"