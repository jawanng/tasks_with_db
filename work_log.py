from common import Common
from peewee import *

db = SqliteDatabase('tasks.db')


class Task(Model):
    date = DateField()
    name = CharField(max_length=70)
    title = CharField(max_length=255)
    task_time = IntegerField(null=False, unique=False)
    notes = TextField(null=True)

    class Meta:
        database = db

    def __str__(self):
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
    db.connect()
    db.create_tables([Task], safe=True)


def add_task_menu():
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
    Task.create(date=task_entry[0], name=task_entry[1], title=task_entry[2], task_time=task_entry[3],
                notes=task_entry[4])


def edit_task(task):
    while 1:
        Common.clear()
        print("What would you like to edit?")
        option = input("Name, Title, Date, Time, Notes :  ")
        if option.lower() == "name":
            task.name = input("Name of who worked on the task: ")
            break
        elif option.lower() == "title":
            task.name = input("What is the title of the task: ")
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
    Common.clear()
    results = Task.select(Task.name).distinct()
    print("Employee(s)\n-----------")
    for result in results:
        print(result.name)
    print()


def list_dates():
    Common.clear()
    results = Task.select(Task.date).distinct()
    print("Date(s)\n-------")
    for result in results:
        print(result.date.strftime('%m/%d/%Y'))
    print()
    input("Press enter to pick the date")


def delete_task(task):
    task.delete_instance()


def search_employee(text):
    return Task.select().where(Task.name.contains(text))


def search_date():
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
    return Task.select().where(Task.task_time == duration)


def text_search(text):
    return Task.select().where(Task.title.contains(text) | Task.notes.contains(text))


if __name__ == "__main__":
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
