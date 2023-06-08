# Note that data is saved inside of a text file!
# hours to select from you know?
hours = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
         "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24"]

file_name = "data.txt"

# Helper functions

# Convert list into dictionary.

def convert_list(lst):
    if len(lst) > 0:
        new_dict = {}

        for key, val in enumerate(lst):
            new_dict[key] = lst[key]

        return new_dict
    else:
        return  False


# Check for numeric answers.

def verify_numeric(input):
    input = input.replace(" ", "")
    if input.isnumeric():
        return  input
    else:
        print(number_error)
        return  False

# Check for yes or no answers.

def verify_answer(input):
    input = input.replace(" ", "")
    if "y" in input:
        return  True
    elif "n" in input:
        return  False
    print(input_error)


# Error functions
input_error = "Input error! Answer was not formatted with yes or no. Please use yes or no!"
number_error = "Number error! Answer was not a number or not found! Please put in a number next time!"
time_error = "There is no time such as this time, reselect time ranging from 1-24 in military."



# Option One : Create a new task.
# Ask what time does this task begin.
# Ask what time does this task end.
# Ask for the name of this task as well.

def new_task():
    print("Please remember to use military time!")

    name = name_task()
    start = start_time()
    end = end_time()


    verify_task(start, end, name)
    main_menu()

# Ask for a name.

def name_task():
    name = input("What is the name to your task?")
    return name

def end_time():
    time = verify_numeric(input("What is the end time?"))
    if time in hours:
        return time
    else:
        print(time_error)
        end_time()



def start_time():
    temp_list = hours.copy()
    with open(file_name, "r") as file:
        for line in file:
            for x in temp_list:
                if "Start: " + x in line:
                    temp_list.remove(x)

    print("Avaible times! You don't have to choose from these of course.")
    print(temp_list)
    time = verify_numeric(input("What is the starting time?"))

    if time in hours:
        return time
    else:
        print(time_error)
        start_time()

# Write the task
def write_task(start, end, name):
    with open(file_name, "a") as file:
        file.seek(0, 2)
        file.write("Name: " + name + " Start: " + start + " End: " + end + "\n")

# Ask for verification towards making this task.

def verify_task(start, end, name):
    times = check_times(start, end)
    if times == False:
        main_menu()
        return
    overlap = check_overlap(start)
    if type(overlap) is dict:
        update_overlap(overlap)
        write_task(start, end, name)
    elif overlap == True:
        main_menu()
    elif overlap == False:
        write_task(start, end, name)


# If times are weird, or one task has a starting time pass it's end time >
# Ask whether to delete this task or not.
# If yes, just go back to main menu.
# If no, create the task.

def check_times(start, end):
    ein = hours.index(end)
    if ein+1>24:
        ein = hours[1]
    else:
        ein = hours.index(end)+1

    sin = hours.index(start)
    if sin+1>24:
        sin = hours[1]
    else:
        sin = hours.index(start)+1


    if sin > ein:
        answer = verify_answer(input("Are you sure these times works? Starting from " + start + " to " + end))
        if answer == True:
            return  True
        else:
            # Just don't make the task.
            return  False


# If it overlaps.
# Check if this task overlaps with another.
# If it does, ask if they'd like to go through.
# If they say yes, make it.

def check_overlap(start):
    temp_list = []
    # Code taken from stackexchange.
    # https://stackoverflow.com/questions/42508768/how-to-retrieve-specific-value-from-file-using-python
    # Starting here.
    with open(file_name, 'r') as file:
        new_list = list(file)
        # Check all items in the list
        for row in new_list:
            if row.find("Start: " + start) != -1:
                # Ending here.
                # create a dictionary out of this
                temp_list.append(row)

    found_lines = convert_list(temp_list)
    if found_lines == False:
        return  False

    print(found_lines)
    answer = verify_answer(input("This task overlap with this new task, procede?"))
    if answer == True:
        return found_lines
    else:
        return True

# If yes, make it and send back to main menu.

def update_overlap(lines):
    answer = verify_answer(input("Would you like delete this overlapped task?"))
    if answer == True:
        delete_task(lines)
        return  True
    else:
        return  False

# Read all lines and store it.
# Truncate the file, deleting everything.
# Loop through the read lines, loop through the lines we do not want to save using the saved table.
# Write the lines we want to save and ignore the ones we don't.
# Finish.

def delete_task(ig_lines):
    # Taken from stack exchange.
    # https://stackoverflow.com/questions/4710067/how-to-delete-a-specific-line-in-a-text-file-using-python
    # Starting from here.
    with open(file_name, 'r') as file:
        body = file.readlines()
    with open(file_name, 'w') as file:
        file.truncate()
        for line in body:
            for key in ig_lines:
                # Ending here.
                if line != ig_lines[key]:
                    file.write(line)

# Option two:
# Read lines and print them out!
def view_task():
    with open(file_name, 'r') as f:
        print("\n"*15)
        print("These are your task:")
        all_lines = convert_list(list(f))
        if not all_lines:
            print("File is empty!")
            main_menu()
            return
        else:
            for key in all_lines:
                line = all_lines[key].strip("\n")
                print(line)
            any = input("Press anything to return to main menu!")
            if any or not any:
                print("\n" * 15)
                main_menu()


# Option three:
def choose_delete():
    tab = {}
    with open(file_name, "r") as file:
        all_lines = convert_list(list(file))

    if not all_lines:
        print("No task to delete!")
        main_menu()
        return

    print(all_lines)
    answer = verify_numeric(input("Which task would you delete?"))
    answer = int(answer)

    # If we have a number that is in the delete then go forward
    if answer in all_lines:
        tab[answer] = all_lines[answer]
        delete_task(tab)

    main_menu()



# Have a main menu function that holds potential things we can do
def main_menu():
    # List out the potential things we can do.
    print("Hello, and welcome to text to task. What would you like to do? \n")
    print("[1]:View tasks.")
    print("[2]:Create task.")
    print("[3]:Delete task.")
    print("[4]:Quit planner.")
    print("\n")

    answer = verify_numeric(input("Select using numbers:"))

    if "1" in answer:
        view_task()
    if "2" in answer:
        new_task()
    if "3" in answer:
        choose_delete()
    if "4" in answer:
        quit()


# So clean so awesome, so cool!
# God is good!
main_menu()

