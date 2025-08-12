from functions.get_files_info import run_python_file
from config import MAX_CHARS


#result = write_file("calculator", "main.py")
#print("Result for current directory:")
#print(result)
#print("")



print(run_python_file("calculator", "main.py"))
print(run_python_file("calculator", "main.py", ["3 + 5"]))
print(run_python_file("calculator", "tests.py"))
print(run_python_file("calculator", "../main.py"))
print(run_python_file("calculator", "nonexistent.py"))

if __name__ == "__main__":
    pass