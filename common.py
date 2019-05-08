import datetime
from os import system, name


class Common:
    """
    Helper functions for the Task class.

    All are class methods

    """

    @classmethod
    def clear(cls):
        """Needed because some people still use Windows :)"""
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

    @classmethod
    def get_date(cls, intro_message="Date of the task"):
        """
        This prompts the user for a date and properly formats it

        Parameters:
        arg1 (text): Optional message to display to the user

        Returns:
        DateTime: Date entered by the user
        """
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
        """Method to validate the input for length of task.  Returns (int) minutes"""
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
        """Method to ask user if they want to use exact date or range of dates.  Returns (E or R)"""
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
        """Gives the option of adding a new entry or searching existing entries. Returns (a, b, or c)"""
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
        """Menu of search options. Returns (a, b, c, d, or e)"""
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
        """
        Formats and prints the results of the various searches

        This clears the screen. Prints the entry. Then let's the user know that this is x of y entries.

        Parameters:
        arg1 (list): A list of search results
        arg2 (int): The index of the current entry to display
        arg3 (int): The total number of entries in the results array

        Returns:
        N/A

        """
        Common.clear()
        print(results[entry])
        print("\nResult {} of {}\n".format(entry+1, total_num))

    @classmethod
    def print_result_array(cls, results, idx=0):
        """
        Prints the results along with a navigation menu.

        The navigation menu has options to go forward, backward, edit or delete and entry.

        Parameters:
        arg1 (list): A list of search results
        arg2 (int): An index of the current result.

        Returns:
        String: The users choice of action (Previous, Next, Delete, Edit, Return to Main Menu)

        """
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

