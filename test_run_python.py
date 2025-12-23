from functions.run_python_file import run_python_file
from functions.write_file import write_file
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info

# Example usage:
print("=== Run python file ===")

run_python_file_result = run_python_file("calculator", file_path="main.py")
print(run_python_file_result)

run_python_file_result = run_python_file("calculator", "main.py", ["3 + 5"])
print(run_python_file_result)


run_python_file_result = run_python_file("calculator", "tests.py")
print(run_python_file_result)

run_python_file_result = run_python_file("calculator", "../main.py")
print(run_python_file_result)

run_python_file_result = run_python_file("calculator", "nonexist.py")
print(run_python_file_result)

run_python_file_result = run_python_file("calculator", "lorem.txt")
print(run_python_file_result)