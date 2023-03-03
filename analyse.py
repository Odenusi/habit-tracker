from db import get_habit_tracker_data
from db import get_db
from db import update_habit_longest_streak
db = get_db("main_test")
db2 = get_db("test_db")
db3 = get_db("test_db3")


def calculate_streak(db, habit):
    """
    Calculate streak of the habit

    :param db: an initialized sqlite3 database connection
    :param habit: name of the habit present in the database
    :return: length of the habit check events (should probably clarify on this)
    """
    data = get_habit_tracker_data(db, habit)  # compute something like number of consecutive check offs
    return len(data)


def print_entries(db, habit):
    """

    :param db: an initialized sqlite3 database connection
    :param habit: name of the habit present in the database
    :return: A list of a habit and check-off dates and times
    """
    data = get_habit_tracker_data(db, habit)  # compute something like number of consecutive check offs
    return data


data = print_entries(db, "read")


def streak_func(db3, habit):

    month_len = {
        '01': 31,
        '02': 28,
        '03': 31,
        '04': 30,
        '05': 31,
        '06': 30,
        '07': 31,
        '08': 31,
        '09': 30,
        '10': 31,
        '11': 30,
        '12': 31

    }

    data = print_entries(db3, habit)
    dates = []
    no_hyphens = []
    streak = 1
    longest_streak = 1
    curr_streak = 1
    for x in data:
        dates.append(x[-1])
    for x in dates:
        no_hyphens.append(x.split("-"))
    for x in no_hyphens:        # flips the contents of the no_hyphens list so it is in the format [d,m,y]
        x.reverse()
    year = []
    month = []
    day = []

    for x in no_hyphens:
        year.append(x[2])
    current_year = year[-1]
    same_year = True

    # Comparing each element with first item
    for item in year:
        if current_year != item:
            same_year = False

    print("same year: " + str(same_year))

    for x in no_hyphens:
        month.append(x[1])
    current_month = month[-1]
    same_month = True

    for item in month:
        if current_month != item:
            same_month = False

    for x in no_hyphens:
        day.append(x[0])
    current_day = int(day[-1])
    same_day = True

    for item in day:
        if current_day != item:
            same_day = False

    day_in_num = []

    for x in day:
        day_in_num.append(x.lstrip("0"))

    x = 1
    y = 1
    z = 0

    if same_year:  # if the year value is the same we can then check if the month is the same
        if same_month:
            if same_day:  # this would mean that the dates are identical
                streak = streak
            else:
                while len(day_in_num) != x:
                    if current_day - x == int(day_in_num[-1-x]):
                        streak = streak + 1
                        x = x + 1
                    else:
                        x = 1
                        break
        else:
            streak = streak
            while len(day_in_num) != x:
                if current_day - x == int(day_in_num[-1 - x]):
                    streak = streak + 1
                    x = x + 1
                else:
                    x = 1
                    break

    else:
        streak = streak
        while len(day_in_num) != x:
            if current_day - x == int(day_in_num[-1 - x]):
                streak = streak + 1
                x = x + 1
            else:
                x = 1
                break

    return streak


def longest_streak_func(db, habit, streak):
    # Given the current streak of a habit each time I will check whether this current streak is greater than the
    # longest streak. if current streak is greater than longest streak then longest streak will be set to the value
    # of current streak
    # instance_of_habit = return_habit_instances(db, name)
    # streak = streak_func(db, name)
    if streak > habit.get_longest_streak():
        update_habit_longest_streak(db, habit.name, streak)
    else:
        habit.set_longest_streak(habit.get_longest_streak())

    return habit.get_longest_streak()


def get_all_habit_table_data(db):
    """
    Returns all the rows from the Habit table where the name field matches the name argument.
    :param db: an initialized sqlite3 database connection
    :return: all the rows from the Habit table where the name field matches the name argument.
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habits")  # remember to check if the data actually exists in the database
    return cur.fetchall()


def same_periodicity(db, period):
    """
    Returns the names of all habits categorized by periodicity.

    :param db: an initialized sqlite3 database connection
    :param period: either the string 'daily' or 'weekly'
    :return: a list of habit's names based on the period parameter value.
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE periodicity = ?", (period,))
    rows = cur.fetchall()
    habits = []
    habit_names = []
    for row in rows:
        habits.append(row[0])
    for habit in habits:
        habit_names.append(habit)

    return habit_names
