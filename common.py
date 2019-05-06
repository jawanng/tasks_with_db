import datetime
from os import system, name


class Common:

    @classmethod
    def clear(cls):
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

    @classmethod
    def get_date(cls, intro_message="Date of the task"):
        while 1:
            Common.clear()
            print(intro_message)
            task_date_raw = input("Please use MM/DD/YYYY: ")
            task_date_num = task_date_raw.split("/")
            try:
                task_date = datetime.date(year=int(task_date_num[2]),
                                          month=int(task_date_num[0]),
                                          day=int(task_date_num[1]))
            except (ValueError, IndexError) as e:
                print("\n\n{}".format(e))
                input("Press enter to try again")
            else:
                break
        return task_date

    @classmethod
    def get_minutes(cls):
        while 1:
            Common.clear()
            try:
                minutes = int(input("Time spent (rounded minutes) : "))
            except ValueError as e:
                print("\n\n{}".format(e))
                input("Press enter to try again")
            else:
                if minutes >= 1:
                    return minutes
                else:
                    print("Time spent must be an integer greater than 1\n")
                    input("Press enter to try again")

    @classmethod
    def get_date_option(cls):
        while 1:
            Common.clear()
            response = input("E) Exact date\nR) Range of dates\n> ")
            if response in ['E', 'e', 'R', 'r']:
                return response.upper()
            else:
                print("Your response must be E or R\n")
                input("Press return to continue")

    @classmethod
    def main_message(cls):
        Common.clear()
        while 1:
            option = input('''
            WORK LOG
            What would you like to do?
            a) Add new entry
            b) Search in existing entries
            c) Quit program
            > ''')
            if option in ('a', 'b', 'c'):
                return option
            else:
                Common.clear()
                print("Please enter a, b, or c")

    @classmethod
    def search_menu(cls):
        Common.clear()
        while 1:
            option = input('''
            Do you want to search by:
            a) Employee
            b) Date(s)
            c) Time spent
            d) Search Term
            e) Return to menu
            > ''')
            if option in ('a', 'b', 'c', 'd', 'e'):
                Common.clear()
                return option
            else:
                Common.clear()
                print("Please enter a, b, c, d, or e")

    @classmethod
    def print_result(cls, results, entry, total_num):
        Common.clear()
        print(results[entry])
        print("\nResult {} of {}\n".format(entry+1, total_num))

    @classmethod
    def print_result_array(cls, results, idx=0):
        total = len(results)
        while 1:
            Common.print_result(results, idx, total)
            if idx == 0 and total > 1:
                option = input("[N]ext, [E]dit, [D]elete, [R]eturn to search menu\n> ").upper()
                if option in ["N", "E", "D", "R"]:
                    return option
            elif idx == 0:
                option = input("[E]dit, [D]elete, [R]eturn to search menu\n> ").upper()
                if option in ["E", "D", "R"]:
                    return option
            elif idx == total - 1:
                option = input("[P]revious, [E]dit, [D]elete, [R]eturn to search menu\n> ").upper()
                if option in ["P", "E", "D", "R"]:
                    return option
            else:
                option = input("[P]revious, [N]ext, [E]dit, [D]elete, [R]eturn to search menu\n> ").upper()
                if option in ["P", "N", "E", "D", "R"]:
                    return option
            print("\nInvalid Entry")

