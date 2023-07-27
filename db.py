import sqlite3
import datetime
from date_reformatter import format_date


def get_db(name='main.db'):
    """
    Initializes a sqlite3 database connection.

    :param name: The name of the connected database. Defaults to 'main.db' if not overwritten.
    :return: The connected database.
    """
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    """
    Creates the Habit table and the Tracker table in our database and commits these changes.
    :param db: an initialized sqlite3 database connection
    :return: None
    """

    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS habits (
        name TEXT,
        description TEXT,
        periodicity TEXT,
        longest_streak INTEGER)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS tracker (
    habitName TEXT,
    date TEXT,
    FOREIGN KEY (habitName)REFERENCES habits(name))""")

    cur.execute("""CREATE TABLE IF NOT EXISTS longest_streak_table (
    habitName,
    streak INT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS streak_table (
    habitName,
    streakDates)""")

    db.commit()


def add_habit(db, name, description, periodicity, longest_streak):
    """
    Adds habits to the Habits table and commits these changes.
    :param db: An initialized sqlite3 database connection.
    :param name: The name of the habit.
    :param description: The description of the habit.
    :param periodicity: The periodicity of the habit.
    :param longest_streak: The longest streak the habit has had.
    :return: None
    """
    cur = db.cursor()
    cur.execute("INSERT INTO habits VALUES (?, ?, ?, ?)", (name, description, periodicity, longest_streak))
    db.commit()


def add_streaks(db, habit, streak_date):
    """
    Adds streaks to the streak table
    :param db: An initialized sqlite3 database connection.
    :param habit: The created habit that's been checked off
    :param streak_date: streak date for the streak table
    :return:
    """
    cur = db.cursor()
    cur.execute("INSERT INTO streak_table VALUES (?, ?)", (habit, streak_date))
    db.commit()


def return_streaks(db, habit):
    """
    Returns streaks from the streak table
    :param db: An initialized sqlite3 database connection.
    :param habit: The created habit that's been checked off
    :return: All rows from the streak table for the corresponding habit
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM streak_table WHERE habitName=?", (habit,))
    return cur.fetchall()


def longest_streak_max_value(db, habit_name):
    """
    Returns the longest streak value
    :param db: An initialized sqlite3 database connection.
    :param habit_name: The name of the corresponding habit
    :return: The row with the largest value from the longest_streak_table according to the corresponding habit
    """
    cur = db.cursor()
    cur.execute("SELECT MAX(streak) FROM longest_streak_table WHERE habitName=?", (habit_name,))
    max_value = cur.fetchone()[0]

    return max_value


def update_longest_streak(db, habit_name, streak):
    """
    Updates the longest streak value
    Adds habits to the Habits table and commits these changes.
    :param db: An initialized sqlite3 database connection.
    :param streak: The longest streak the has had.
    :param habit_name: The longest streak the has had.
    :return: None
    """
    cur = db.cursor()
    cur.execute("INSERT OR IGNORE INTO longest_streak_table VALUES (?, ?)", (habit_name, streak))
    db.commit()


def check_habit(db, name, event_date=None):
    """
    Checks off habits by adding them to the Tracker table and commits these changes.
    :param db: an initialized sqlite3 database connection
    :param name: The name of the habit to be checked off
    :param event_date: The date the habit was checked off. Defaults to None if not overwritten
    :return: None
    """
    cur = db.cursor()
    if not event_date:
        event_date = str(datetime.date.today())
        event_date_reformatted = format_date(event_date)
    else:
        event_date_reformatted = format_date(event_date)
    cur.execute("INSERT INTO tracker VALUES (?, ?)", (name, event_date_reformatted))  # format prevents sql injections
    add_streaks(db, name, event_date_reformatted)
    db.commit()


def custom_data(db, name, event_date):
    """
    function to insert custom data (preferably for testing purposes)
    :param db: An initialized sqlite3 database connection.
    :param name: The name of the custom habit
    :param event_date: The custom date
    :return: None
    """
    cur = db.cursor()
    cur.execute("INSERT INTO tracker VALUES (?, ?)", (name, event_date))  # this formatting prevents sql injections
    db.commit()


def get_habit_tracker_data(db, name):
    """
    Returns all the rows in the tracker table where the habitName field matches the name argument.
    :param db: an initialized sqlite3 database connection
    :param name: The name of the habit whose data we want to work with
    :return: All the rows in the tracker table where the habitName field matches the name argument.
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM tracker WHERE habitName=?", (name,))  # remember to check if the data actually exists
    # in the database
    return cur.fetchall()


def get_habit_table_data(db, name):
    """
    Returns all the rows from the Habit table where the name field matches the name argument.
    :param db: an initialized sqlite3 database connection
    :param name: The name of the habit whose data we want to work with
    :return: all the rows from the Habit table where the name field matches the name argument.
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE name=?", (name,))  # remember to check if the data actually exists in the
    # database
    return cur.fetchall()


def update_habit_periodicity(db, name, periodicity):
    """
    Function to chenge the habits periodicity
    :param db: an initialized sqlite3 database connection
    :param name: Habit's name as a string
    :param periodicity: habit's new periodicity, either 'weekly' or 'daily'
    :return: None
    """
    cur = db.cursor()
    cur.execute("UPDATE habits SET periodicity = ? WHERE name = ?", (periodicity, name))
    db.commit()


def update_habit_longest_streak(db, name, longest_streak):
    """
    Updates the habit's longest streak
    :param db: an initialized sqlite3 database connection
    :param name: Habit's name as a string
    :param longest_streak: habit's new longest streak value
    :return: None
    """
    cur = db.cursor()
    cur.execute("UPDATE habits SET longest_streak = ? WHERE name = ?", (longest_streak, name))
    db.commit()


def remove_habit(db, name):
    """
    Deletes habit from the habits list
    :param db: an initialized sqlite3 database connection
    :param name: Habit's name as a string
    :return: None
    """
    cur = db.cursor()
    cur.execute("DELETE from habits WHERE name = ?", (name,))
    db.commit()


def return_habits(db):
    """
    Returns all the rows from the Habit table where the name field matches the name argument.
    :param db: an initialized sqlite3 database connection.
    :return: the names of the habits in the Habit table.
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habits")  # remember to check if the data actually exists in the database
    rows = cur.fetchall()  # Every row in the habit table is now in the row variable
    habits = []  # List ot store the habits from the habit table
    habit_names = []  # List to store just the name of the habit from the habit list
    for row in rows:
        habits.append(row[0])
    for habit in habits:
        habit_names.append(habit)

    return habit_names  # returns a list of the habit names


def return_adapted_habits(db, habit_name):
    """
    Returns all the rows from the Habit table where the name field matches the name argument.
    Adapted in the sense that these habits are form the longest_streak_table and are in descending order??
    And that they are purely the rows from said table. So technically "unadapted".
    :param db: an initialized sqlite3 database connection.
    :param habit_name: the name of the habit
    :return: all the rows from the Habit table.
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM longest_streak_table WHERE habitName = ? ORDER BY rowid DESC", (habit_name,))
    rows = cur.fetchall()
    return rows


def return_habit_instances(db, habit_name):
    """
    Returns all the rows from the Habit table where the name field matches the name argument.
    :param db: an initialized sqlite3 database connection.
    :param habit_name: the name of the habit
    :return: all the rows from the Habit table.
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE name = ?", (habit_name,))
    rows = cur.fetchall()
    habit_instances = []
    for row in rows:
        habit_instances.append(row)

    return habit_instances
