# from functions.get_file_info import get_file_info
from functions.get_file_content import get_file_content

# print(get_file_info("calculator", "."))
# print(get_file_info("calculator", "pkg"))
# print(get_file_info("calculator", "/bin"))
# print(get_file_info("calculator", "../"))

# print(get_file_content("calculator", "lorem.txt"))
print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))
