import os
from datetime import date

# module contains miscellaneous functions

class helper():
    # function parses a string and converts to appropriate type
    @staticmethod # staticmethod makes it so do not have to put self in each python class method definition
    def convert(value):
        types = [int,float,str] # order needs to be this way
        if value == '':
            return None
        for t in types:
            try:
                return t(value)
            except:
                pass

    # function reads file path to clean up data file
    @staticmethod
    def data_cleaner(path):
        with open(path,"r",encoding="utf-8") as f:
            data = f.readlines()

        data = [i.strip().split(",") for i in data]
        data_cleaned = []
        for row in data[:]:
            row = [helper.convert(i) for i in row]
            data_cleaned.append(tuple(row))
        return data_cleaned

    # function checks for user input given a list of choices
    @staticmethod
    def get_choice(lst):
        choice = input("Enter choice number: ")
        while choice.isdigit() == False:
            print("Incorrect option. Try again")
            choice = input("Enter choice number: ")

        while int(choice) not in lst:
            print("Incorrect option. Try again")
            choice = input("Enter choice number: ")
        return int(choice)

    # reusable function for getting a string value from user input
    @staticmethod
    def get_str(msg):
        res = ""
        while True:
            res = input(msg)
            if res == "":
                print("Invalid input, nothing was entered.")
                continue
            else:
                break
        return res

    @staticmethod
    def get_file_path():
        path = ""
        while True:
            path = input("--Enter the file path.\n--NOTE: Default path is ./songs_update.csv simply press ENTER if wish to use the default path\nPath: ")
            # default case
            if path == "":
                path = "./songs_update.csv"
                break
            
            # split file into name and ext
            split_path = os.path.os.path.splitext(path)
            file_name = split_path[0]
            file_ext = split_path[1]
            # ensure a csv file is being passed
            if file_ext != ".csv":
                print("ERROR: Invalid file type. Received {} but expected a .csv file.".format(file_ext))
                continue
            # checking user inputted path
            try:
                open(path, "r")
                break
            except:
                print("ERROR: Invalid file path, please enter a valid path.")
                continue
        return path
            


    # function prints a list of strings nicely
    @staticmethod
    def pretty_print(lst):
        print("Results..")
        for i in lst:
            print(i)
        print("")

    # function prints a list of strings nicely with the attributes
    @staticmethod
    def pretty_print_attr(attr_list, results_list):
        print("Results..")
        results_dict = {}
        for index, attr in enumerate(attr_list):
            results_dict[attr] = results_list[index]
        index = 0
        for key, value in results_dict.items():
            print(f'{index} {key} : {value}')
            index += 1

    @staticmethod
    def get_update_value(msg, data_type, original_value):
        isValid = False
        value = None
        while isValid == False:
            value = input(msg)
            if len(value) == 0:
                print("Error: Input cannot be empty")
                continue
            if value == original_value:
                print(f"Error: Value - {value} - is the same, please enter a new value.")
                continue
            if data_type == str:
                # get length of str input
                input_len = len(value)
                # make sure it is not more than 20 chars long
                if input_len > 20:
                    print("Error: Input cannot exceed 20 characters.")
                    continue
            elif data_type == date:
                date_err_msg = "Error: Date input must be in the form of YYYY-MM-DD \n*YYYY is year, MM is month, DD is day."
                input_len = len(value)
                # check length
                if input_len != 10:
                    print(date_err_msg)
                    print("Potential Cause: Incorrect Length")
                    continue
                # check dash indexes
                if value[4] != "-" or value[7] != "-":
                    print(date_err_msg)
                    print("Potential Cause: Missing dash(s).")
                    continue
                date_nums = [char for index, char in enumerate(value) if index != 4 and index != 7]
                for num in date_nums:
                    try:
                        int(num)
                    except Exception as e:
                        print(date_err_msg)
                        print(f"Potential Cause: Incorrect data type.\n{e}")
                        continue
            elif data_type == bool:
                valid_options = ["0", "1", "True", "False"]    
                if value not in valid_options:
                    print(f"Error: Incorrect data type, expected bool value.\nValid inputs are: {valid_options}")
                    continue
                if value == "1":
                    value = "True"
                if value == "0":
                    value = "False"
            isValid = True
        return value


