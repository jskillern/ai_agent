from functions.get_files_info import write_file
from config import MAX_CHARS


#result = write_file("calculator", "main.py")
#print("Result for current directory:")
#print(result)
#print("")



result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
print("Result for current directory:")
print(result)
print("")
result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
print("Result for current directory:")
print(result)
print("")
result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
print("Result for current directory:")
print(result)
print("")

if __name__ == "__main__":
    pass