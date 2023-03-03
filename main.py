import questionary  # Imports the questionary module used to create the sleek user interface
from db import get_db  # Imports our database from the database module
from db import return_habits  # Imports a function that returns a list of every habit's name
from db import return_adapted_habits
from db import add_adapted_habit
from analyse import get_all_habit_table_data  # Imports a function that returns all the rows from our habit table
from analyse import print_entries  # Imports the function used to list a habits' check-off dates and times
from analyse import same_periodicity  # Imports a function that lists all habits grouped by periodicity
from analyse import streak_func
from habit import Habit  # Imports the Habit class from the habit module
from habit import adapt_habit
import sqlite3

sqlite3.register_adapter(Habit, adapt_habit)
habits = []


def cli(habits):
    """
    A wrapper for our command line interface.
    :return: None
    """
    db = get_db("test_db3")

    questionary.confirm("are you ready?").ask()  # Asks the user if they are ready to use the program
    if not get_all_habit_table_data(db):  # If no habits are found the user will be prompted to create their first habit
        print("You do not have any habits.")
        name = questionary.text("What is the name of your first habit?").ask()
        description = questionary.text("What is the description of your first habit?").ask()
        longest_streak = 0
        period_choice = questionary.select(
            "How often do you want to do this habit?",
            choices=["Daily", "Weekly"]
        ).ask()
        if period_choice == "Daily":
            period = "d"
        else:
            period = "w"
        habit = Habit(name, description, period, longest_streak)
        habits.append(habit)
        habit.store_habit(db)
        add_adapted_habit(db, habit.name, habit)
    stop = False
    while not stop:  # Loops the program's execution until stop is set to true, which is done when the user chooses Exit
        choice = questionary.select(
            "What do you want to do?",
            choices=["Create", "Check", "Analyse", "Exit"]
        ).ask()
        if choice == "Create":  # If the user chooses the 'create' action they will be able to take action accordingly
            name = questionary.text("What is the name of your habit?").ask()
            desc = questionary.text("What is the description of your habit?").ask()
            period_choice = questionary.select(
                "How often do you want to do this habit?",
                choices=["Daily", "Weekly"]
            ).ask()
            if period_choice == "Daily":
                period = "d"
            else:
                period = "w"
            longest_streak = 0
            habit = Habit(name, desc, period, longest_streak)
            habit.store_habit(db)
            habits.append(habit)
            add_adapted_habit(db, habit.name, habit)
        elif choice == "Check":  # If the user chooses the 'check' action they will be able to take action accordingly
            name = questionary.select(
                "which habit do you want to check-off?",
                choices=return_habits(db)
            ).ask()

            check_choice = questionary.select(
                "How would you like to check off this habit?",
                choices=["Manually add the date in the format YYYY-MM-DD", "Automatically fill in today's date"]
            ).ask()
            if check_choice == "Manually add the date in the format YYYY-MM-DD":
                year_validity = "invalid"
                month_validity = "invalid"
                day_validity = "invalid"
                while year_validity == "invalid":
                    year = questionary.text("What year did you do this habit?").ask()
                    if len(year) == 4:
                        try:
                            year_in_num = int(year)
                            year_validity = "valid"
                        except:
                            print("this should be in digits")
                            year_validity = "invalid"
                    else:
                        print("year should be four digits long")
                        year_validity = "invalid"
                while month_validity == "invalid":
                    month = questionary.text("What month did you do this habit?").ask()
                    if len(month) == 2:
                        try:
                            month_in_num = int(month)
                            month_validity = "valid"
                        except:
                            print("this should be in digits")
                            month_validity = "invalid"
                    else:
                        print("month should be 2 digits long (prefix with a zero if the month is before October) ")
                        month_validity = "invalid"
                while day_validity == "invalid":
                    day = questionary.text("What day did you do this habit?").ask()
                    if len(day) == 2:
                        try:
                            day_in_num = int(day)
                            day_validity = "valid"
                        except:
                            print("this should be in digits")
                            day_validity = "invalid"
                    else:
                        print("day should be 2 digits long (prefix with a zero if the day is before the 10th")
                        day_validity = "invalid"

                date = str(year + "-" + month + "-" + day)
                habit = Habit(name, "no description", "no periodicity", 0)  # this line may be unnecessary
                habit.test_event(db, date)
                streak = streak_func(db, name)

                rows = return_adapted_habits(db, name)
                for x in rows:
                    if int(x[1][-1]) < streak:
                        habit.set_longest_streak(streak)
                        add_adapted_habit(db, habit.name, habit)
                        print(streak)
                        print(habit.longest_streak)
                        print("adding")
                    else:
                        print(streak)
                        print(habit.longest_streak)
            else:
                habit = Habit(name, "no description", "no periodicity", 0)
                habit.add_event(db)
                streak = streak_func(db, name)
                rows = return_adapted_habits(db, name)
                for x in rows:
                    if int(x[1][-1]) < streak:
                        habit.set_longest_streak(streak)
                        add_adapted_habit(db, habit.name, habit)
                        print(streak)
                        print(habit.longest_streak)
                        print("adding")
                    else:
                        print(streak)
                        print(habit.longest_streak)

        elif choice == "Analyse":  # If the 'analyse' action is chosen they will be able to take action accordingly
            analysis_choice = questionary.select(
                "What analysis do you want for this habit?",
                choices=["Current Streak", "Check Entries", "List Habits", "Same Periodicity",
                         "Longest Streak for All Habits"]
            ).ask()
            if analysis_choice == "Current Streak":
                name = questionary.select(
                    "which habit do you want to see the current streak for?",
                    choices=return_habits(db)
                ).ask()
                streak = streak_func(db, name)
                print(f"your current streak for {name} is {streak} day(s)")
            elif analysis_choice == "Check Entries":
                name = questionary.select(
                    "which habit do you want to Check entries for?"
                    ' *Shows the name of habit and when the habit was "checked off" in the format YYYY-MM-DD',
                    choices=return_habits(db)
                ).ask()
                print(print_entries(db, name))
            elif analysis_choice == "List Habits":
                print("Your habits are: ")
                for habit in return_habits(db):
                    print(habit)
            elif analysis_choice == "Same Periodicity":
                daily_habits = []
                weekly_habits = []
                for habit in same_periodicity(db, "d"):
                    daily_habits.append(habit)
                for habit in same_periodicity(db, "w"):
                    weekly_habits.append(habit)
                print("Your daily habits are: ")
                for habit in daily_habits:
                    print(habit)
                print("Your weekly habits are: ")
                for habit in weekly_habits:
                    print(habit)
            else:

                name = questionary.select(
                    "which habit do you want to see the longest streak for?",
                    choices=return_habits(db)
                ).ask()
                for habit in return_habits(db):
                    print(return_adapted_habits(db, habit))

        else:  # If the user chooses the 'exit' action, a goodbye message is shown and the program execution will end
            print("See You Later!!")
            stop = True


if __name__ == '__main__':
    cli(habits)
