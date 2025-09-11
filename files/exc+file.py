# # Exception Handling in Python
# print("------ Exception Handling in Python ------")
# try:
#     number = int(input("Enter a number: "))
# except ValueError:
#     print("Invalid input. Please enter a valid number.")
# except ZeroDivisionError:
#     print("You can't divide by zero!")
# except Exception as e:
#     print(f"An unexpected error occurred: {e}")
# finally:
#     print("Execution completed.")

# File Operations
print("\n------ File Operation ------")
import os

file_path="input.txt"
if os.path.exists(file_path):
    print(f"File '{file_path}' exists.")
    if os.path.isfile(file_path):
        print(f"'{file_path}' is a file.")
    elif os.path.isdir(file_path):
        print(f"'{file_path}' is a directory.")
else:
    print(f"File '{file_path}' does not exist.")

file_path1="D:/OneDrive/Documents/Python/outside.txt"
text="Hello, world!"
try:
    with open(file_path1, 'w') as file:
        file.write(f"{text}\n")
        print(f"File '{file_path1}' written successfully.")
except FileExistsError:
    print(f"File '{file_path1}' doesn't exist.")

file_path2="output.txt"
txt1="Land of the undead"
try:
    with open(file_path2, 'a') as file:
        file.write(f"{txt1}\n")
        print(f"File '{file_path2}' appended successfully.")
except FileExistsError:
    print(f"File '{file_path2}' doesn't exist.")
    
file_path3="output_list.txt"
lines=["Spongebob", "Patrick", "Crabby"]
try:
    with open(file_path3, 'a') as file:
        for line in lines:
            file.write(f"{line} ")
        file.write("\n")
        print(f"File '{file_path3}' written successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
    
file_path4="output.json"
import json
data={"name":"John", 
      "age":30, 
      "city":"New York"}
try:
    with open(file_path4, "w") as file:
        json.dump(data, file, indent=4)
        print(f"File '{file_path4}' written successfully.")
except FileExistsError:
    print(f"File '{file_path4}' doesn't exist.")
    
file_path5="output.csv"
import csv
rows=[["Name", "Age", "City"],
      ["Alice", 28, "Los Angeles"],
      ["Bob", 34, "Chicago"],
      ["Charlie", 22, "Houston"]]
try:
    with open(file_path5, "w", newline="") as file:
        writer=csv.writer(file)
        for row in rows:
            writer.writerow(row)
        print(f"File '{file_path5}' written successfully.")
except FileExistsError:
    print(f"File '{file_path5}' doesn't exist.")
    
try:
    with open("output_list.txt", "r") as file:
        content = file.read()
        print(f"Content of 'output_list.txt':\n{content}")
    with open("output.json", "r") as file:
        content = json.load(file)
        content = json.dumps(content, indent=4)
        print(f"\nContent of 'output.json':\n{content}")
    with open("output.csv", "r") as file:
        reader = csv.reader(file)
        print("\nContent of 'output.csv':")
        for row in reader:
            print(row)
except FileNotFoundError:
    print("File not found.")
except PermissionError:
    print("You don't have permission to read the files.")