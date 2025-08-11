import os
from config import MAX_CHARS


def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    abs_working_dir = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)
    
    if not abs_full_path.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        
    try:
        result_lines = []
        for dir_contents in os.listdir(full_path):
            item_path = os.path.join(full_path, dir_contents)
            size = os.path.getsize(item_path)
            is_directory = os.path.isdir(item_path)
            line = f'- {dir_contents}: file_size={size} bytes, is_dir={is_directory}'
            result_lines.append(line)
        return "\n".join(result_lines)
    except Exception as e:
         return f"Error: {str(e)}"
    

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    abs_full_path = os.path.abspath(full_path)
    abs_working_directory = os.path.abspath(working_directory)

    if not abs_full_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_full_path):
         return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(abs_full_path, "r") as f:
            content = f.read(MAX_CHARS + 1)
        if len(content) > MAX_CHARS:
            content = content[:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content 
    except Exception as e:
        return f"Error: {str(e)}"
    


def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    abs_full_path = os.path.abspath(full_path)
    abs_working_directory = os.path.abspath(working_directory)

    if not abs_full_path.startswith(abs_working_directory):
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
    
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    try:
        with open(full_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {str(e)}"
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'