import os
from google.genai import types
from functions.get_files_info import *
from prompts import system_prompt
from config import MAX_CHARS
import subprocess


model_name = "gemini-2.0-flash-001"



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


def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    abs_full_path = os.path.abspath(full_path)
    abs_working_directory = os.path.abspath(working_directory)

    if not abs_full_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_full_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        command = ["python", abs_full_path] + args
        completed_process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_directory
        )
        result = f'STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}'
        if completed_process.returncode != 0:
            result += f'\nProcess exited with code {completed_process.returncode}'
        return result
    except Exception as e:
        return f"Error: executing Python file: {e}"




schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)



schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)