from db import get_habit_tracker_data
from datetime import datetime, timedelta


def calculate_current_streak(dates):
    """

    :param dates: The dates the habit was checked off
    :return: The current streak as an int
    """
    # Convert date strings to datetime objects
    dates = [datetime.strptime(date, "%Y%m%d") for date in dates]

    # Sort the dates in descending order
    dates.sort(reverse=True)

    # Initialize variables
    current_streak = 1

    # Loop through the sorted dates
    for i in range(len(dates) - 1):
        # Check if the difference between consecutive dates is one day
        if (dates[i] - dates[i + 1]) == timedelta(days=1):
            # If so, increment the current streak
            current_streak += 1
        else:
            # If not, break out of the loop
            break

    # Return the current streak of consecutive days as an integer
    return current_streak


def longest_streak_func(dates):
    """

    :param dates: The dates the habit was checked off
    :return: The longest streak as an int
    """
    from datetime import datetime, timedelta
    date_objs = [datetime.strptime(date, '%Y%m%d') for date in dates]
    sorted_dates = sorted(date_objs)
    streak = 1
    longest_streak = 1
    for i in range(1, len(sorted_dates)):
        if (sorted_dates[i] - sorted_dates[i - 1]) == timedelta(days=1):
            streak += 1
        else:
            if streak > longest_streak:
                longest_streak = streak
            streak = 1
    if streak > longest_streak:
        longest_streak = streak
    return longest_streak


def current_weekly_streak(dates):
    """

    :param dates: The dates the habit was checked off
    :return: The current weekly streak as an int
    """
    streak = 1
    current_date = datetime.strptime(dates[0], '%Y%m%d')

    for i in range(1, len(dates)):
        next_date = datetime.strptime(dates[i], '%Y%m%d')
        if (next_date - current_date).days == 7:
            streak = streak + 1
            current_date = next_date
        elif (next_date - current_date).days < 7:
            continue
        elif (next_date - current_date).days >= 8:
            if (next_date - current_date).days % 7 == 0:
                streak = 1
                current_date = next_date
            else:
                streak = 1
                current_date = next_date

        else:
            pass
    return streak


def longest_weekly_streak(dates):
    """

    :param dates: The dates the habit was checked off
    :return: The longest weekly streak as an int
    """
    streak = 1
    current_date = datetime.strptime(dates[0], '%Y%m%d')
    longest_streak = 1
    for i in range(1, len(dates)):
        next_date = datetime.strptime(dates[i], '%Y%m%d')
        if (next_date - current_date).days == 7:
            streak = streak + 1
            current_date = next_date
        elif (next_date - current_date).days < 7:
            pass
        elif (next_date - current_date).days >= 8:
            if (next_date - current_date).days % 7 == 0:
                streak = 1
                current_date = next_date
            else:
                streak = 1
                current_date = next_date

        else:
            pass
        if streak > longest_streak:
            longest_streak = streak
    return longest_streak


def print_entries(db, habit):
    """

    :param db: an initialized sqlite3 database connection
    :param habit: name of the habit present in the database
    :return: A list of a habit and check-off dates
    """
    data = get_habit_tracker_data(db, habit)  # compute something like number of consecutive check offs

    return data


def get_all_habit_table_data(db):
    """
    Returns all the rows from the Habit table where the name field matches the name argument.
    :param db: an initialized sqlite3 database connection
    :return: all the rows from the Habit table.
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habits")
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
