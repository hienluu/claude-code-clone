from functions.get_file_content import get_file_content

file_context = get_file_content("calculator", file_path="lorem.txt")
print(len(file_context))

file_context = get_file_content("calculator", file_path="main.py")
print(file_context)

#file_context = get_file_content("calculator", file_path="/bin/cat")
#print(file_context)

file_context = get_file_content("calculator", file_path="pkg/does-not-exist.txt")
print(file_context)