import questionary  # Imports the questionary module used to create the sleek user interface

from analyse import get_all_habit_table_data, print_entries, same_periodicity
from db import get_db, return_habits, update_longest_streak, add_streaks, return_streaks
from habit import Habit  # Imports the Habit class from the habit module
from analyse import calculate_current_streak, longest_streak_func, current_weekly_streak, \
    longest_weekly_streak

habits = []


def cli(habits):
    """
    A wrapper for our command line interface.
    :return: None
    """
    db = get_db("main_db")

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
            period = "daily"
        else:
            period = "weekly"
        habit = Habit(name, description, period, longest_streak)
        habits.append(habit)
        habit.store_habit(db)
        update_longest_streak(db, habit.name, longest_streak)
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
                period = "daily"
            else:
                period = "weekly"
            longest_streak = 0
            habit = Habit(name, desc, period, longest_streak)
            habit.store_habit(db)
            habits.append(habit)
            update_longest_streak(db, habit.name, longest_streak)
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
                streak_date = int(year+month+day)
                # add_streaks(db, name, str(streak_date)) # streaks were added in check habit
                streak_info = return_streaks(db, name)
                streak_dates = []
                streak_dates.append(str(streak_date))
                for x in streak_info:
                    streak_dates.append(x[1])
                if name in same_periodicity(db, "daily"):
                    habit = Habit(name, "no description", "daily", 0)  # this line may be unnecessary
                    habit.add_event(db, date)
                    calculated_streak = calculate_current_streak(streak_dates)
                    # print(streak_dates)
                    # print("Your current streak is: " + str(calculated_streak) + " day(s)")

                else:
                    habit = Habit(name, "no description", "weekly", 0)  # this line may be unnecessary
                    habit.add_event(db, date)
                    # streak = streak_func(db, name)
                    calculated_streak = current_weekly_streak(streak_dates)
                    # print(streak_dates)
                    # print(f"Your current streak for {name} is: {str(calculated_streak)} week(s)")
            else:
                habit = Habit(name, "no description", "no periodicity", 0)
                habit.add_event(db)
                streak_info = return_streaks(db, name)
                streak_dates = []
                for x in streak_info:
                    streak_dates.append(x[1])

            print("updating")

        elif choice == "Analyse":  # If the 'analyse' action is chosen they will be able to take action accordingly
            analysis_choice = questionary.select(
                "What analysis do you want for this habit?",
                choices=["Current Streak", "Check Entries", "List Habits", "Same Periodicity", "Longest streak for All Habits",
                         "Longest Streak for a Habit"]
            ).ask()
            if analysis_choice == "Current Streak":
                name = questionary.select(
                    "which habit do you want to see the current streak for?",
                    choices=return_habits(db)
                ).ask()
                streak_info = return_streaks(db, name)
                streak_dates = []
                for x in streak_info:
                    streak_dates.append(x[1])
                if name in same_periodicity(db, "daily"):
                    current_streak_value = calculate_current_streak(streak_dates)
                    print(f"your current streak for {name} is {current_streak_value} day(s)")
                else:
                    current_streak_value = current_weekly_streak(streak_dates)
                    print(f"your longest streak for {name} is {current_streak_value} week(s)")

            elif analysis_choice == "Check Entries":
                name = questionary.select(
                    "which habit do you want to Check entries for?"
                    ' *Shows the name of habit and when the habit was "checked off" in the format YYYY-MM-DD',
                    choices=return_habits(db)
                ).ask()
                entries = print_entries(db, name)
                if not entries:
                    print("You have never checked off this habit. Check it off to begin a streak")
                else:
                    print(entries)
            elif analysis_choice == "List Habits":
                print("Your habits are: ")
                for habit in return_habits(db):
                    print(habit)
            elif analysis_choice == "Same Periodicity":
                daily_habits = []
                weekly_habits = []
                for habit in same_periodicity(db, "daily"):
                    daily_habits.append(habit)
                for habit in same_periodicity(db, "weekly"):
                    weekly_habits.append(habit)
                if daily_habits:
                    print("Your daily habits are: ")
                    for habit in daily_habits:
                        print(habit)
                else:
                    print("You have no daily habits")
                if weekly_habits:
                    print("Your weekly habits are: ")
                    for habit in weekly_habits:
                        print(habit)
                    print()
                else:
                    print("You have no weekly habits")
                    print()
            elif analysis_choice == "Longest streak for All Habits":
                habit_list = []
                for habit in return_habits(db):
                    habit_list.append(habit)
                for name in habit_list:
                    streak_info = return_streaks(db, name)
                    streak_dates = []
                    for record in streak_info:
                        streak_dates.append(record[1])
                    if name in same_periodicity(db, "daily"):
                        longest_streak_value = longest_streak_func(streak_dates)
                        print(f"your longest streak for {name} is {longest_streak_value} day(s)")
                    else:
                        longest_streak_value = longest_weekly_streak(streak_dates)
                        print(f"your longest streak for {name} is {longest_streak_value} week(s)")
            else:

                name = questionary.select(
                    "which habit do you want to see the longest streak for?",
                    choices=return_habits(db)
                ).ask()

                # longest_streak_value = 0
                streak_info = return_streaks(db, name)
                streak_dates = []
                for x in streak_info:
                    streak_dates.append(x[1])
                if name in same_periodicity(db, "daily"):
                    longest_streak_value = longest_streak_func(streak_dates)
                    print(f"your longest streak for {name} is {longest_streak_value} day(s)")
                else:
                    longest_streak_value = longest_weekly_streak(streak_dates)
                    print(f"your longest streak for {name} is {longest_streak_value} week(s)")

        else:  # If the user chooses the 'exit' action, a goodbye message is shown and the program execution will end
            print("See You Later!!")
            stop = True


if __name__ == '__main__':
    cli(habits)
