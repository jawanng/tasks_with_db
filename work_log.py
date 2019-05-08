from common import Common
from peewee import *

db = SqliteDatabase('tasks.db')


class Task(Model):
    """Task model with name, date, title, task_time, and notes."""
    date = DateField()
    name = CharField(max_length=70)
    title = CharField(max_length=255)
    task_time = IntegerField(null=False, unique=False)
    notes = TextField(null=True)

    class Meta:
        database = db

    def __str__(self):
        """Formatting for the Task"""
        return "Name: {}\nDate: {}\nTitle: {}\nTime Spent: {}\nNotes: {}\n".format(self.name,
                                                                                   self.date.strftime('%m/%d/%Y'),
                                                                                   self.title, self.task_time,
                                                                                   self.notes)

    def __eq__(self, other):
        if (self.name == other.name and self.task_time == other.task_time and
                self.date == other.date and self.notes == other.notes):
            return True
        return False


def search_results():
    """
    Provides the search results.

    This takes the option the user selected and calls the appropriate search.

    Returns:
    list: A list of the search results or None if the user wants to return to the main menu

    """
    new_option = Common.search_menu()
    if new_option == 'a':
        list_employees()
        results = search_employee(input("Name of employee: "))
    elif new_option == 'b':
        results = search_date()
    elif new_option == 'c':
        results = search_duration(Common.get_minutes())
    elif new_option == 'd':
        results = text_search(input("What text to search for: "))
    else:
        results = None
    return results


def search_sequence():
    """
    Gives a message if it receives and empty results array.
    Calls Common.print_result_array with the current index starting with zero
    Based on the user input, either call again with a different index number, edit, or delete the task.
    """
    idx = 0
    results = search_results()
    if not results:
        Common.clear()
        print("No results were found for the criteria specified")
        input("Press enter to return to menu")
        return

    while 1:
        option = Common.print_result_array(results, idx)
        if option == "P":
            idx -= 1
        elif option == "N":
            idx += 1
        elif option == "R":
            break
        elif option == "D":
            delete_task(results[idx])
            break
        elif option == "E":
            edit_task(results[idx])
            break


def initialize():
    """Initialize the database."""
    db.connect()
    db.create_tables([Task], safe=True)


def add_task_menu():
    """Sequence for adding a task."""
    name = input("Name of who worked on the task: ")
    Common.clear()
    date = Common.get_date()
    Common.clear()
    title = input("Title of the task: ")
    task_time = Common.get_minutes()
    Common.clear()
    notes = input("Notes (Optional, you can leave this empty) : ")
    add_task([date, name, title, task_time, notes])
    Common.clear()
    input("The entry has been add.  Press enter to return to the menu")
    Common.clear()


def add_task(task_entry):
    """Call to the datebase to create a task."""
    Task.create(date=task_entry[0], name=task_entry[1], title=task_entry[2], task_time=task_entry[3],
                notes=task_entry[4])


def edit_task(task):
    """Takes a task to edit, queries the user or what to edit, perform the edit requested,
    and save the task to the database."""
    while 1:
        Common.clear()
        print("What would you like to edit?")
        option = input("Name, Title, Date, Time, Notes :  ")
        if option.lower() == "name":
            task.name = input("Name of who worked on the task: ")
            break
        elif option.lower() == "title":
            task.title = input("What is the title of the task: ")
            break
        elif option.lower() == "date":
            task.date = Common.get_date()
            break
        elif option.lower() == "time":
            task.task_time = Common.get_minutes()
            break
        elif option.lower() == "notes":
            task.notes = input("Notes (Optional, you can leave this empty) : ")
            break
        else:
            print("You entered an invalid option")
    task.save()


def list_employees():
    """When search by name, this provides a list of names available."""
    Common.clear()
    results = Task.select(Task.name).distinct()
    print("Employee(s)\n-----------")
    for result in results:
        print(result.name)
    print()


def list_dates():
    """When searching by date, this provides a list of dates available"""
    Common.clear()
    results = Task.select(Task.date).distinct()
    print("Date(s)\n-------")
    for result in results:
        print(result.date.strftime('%m/%d/%Y'))
    print()
    input("Press enter to pick the date")


def delete_task(task):
    """Tasks a task as input and deletes it"""
    task.delete_instance()


def search_employee(text):
    """Takes a name or part of a name and return any hits."""
    return Task.select().where(Task.name.contains(text))


def search_date():
    """If the user wants an exact date, query the database for that date and return the results.
    Otherwise, query the database for the range of dates specified and return the results."""
    option = Common.get_date_option()
    if option == 'E':
        list_dates()
        main_date = Common.get_date()
        return Task.select().where(Task.date == main_date.isoformat())
    else:
        begin_date = Common.get_date("What is the date to start with?")
        end_date = Common.get_date("What is the ending date of the search?")
        return Task.select().where(Task.date.between(begin_date, end_date))


def search_duration(duration):
    """Takes a number as input and returns any entries whose task_duration matches that number."""
    return Task.select().where(Task.task_time == duration)


def text_search(text):
    """Takes text as input and returns any records where the title or notes contains the text."""
    return Task.select().where(Task.title.contains(text) | Task.notes.contains(text))


if __name__ == "__main__":
    """Starts the task sequence."""
    initialize()

    while 1:
        option = Common.main_message()
        if option == 'c':
            Common.clear()
            print("Thanks for using the Work Log program!\nHave a great day\n")
            exit()
        elif option == 'a':
            add_task_menu()
        elif option == 'b':
            search_sequence()
