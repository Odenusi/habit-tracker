import sqlite3
import datetime


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
    habit)""")

    db.commit()


def add_habit(db, name, description, periodicity, longest_streak):
    """
    Adds habits to the Habits table and commits these changes.
    :param db: An initialized sqlite3 database connection.
    :param name: The name of the habit.
    :param description: The description of the habit.
    :param periodicity: The periodicity of the habit.
    :param longest_streak: The longest streak the has had.
    :return: None
    """
    cur = db.cursor()
    cur.execute("INSERT INTO habits VALUES (?, ?, ?, ?)", (name, description, periodicity, longest_streak))
    db.commit()


def add_adapted_habit(db, habit_name, habit):
    """
    Adds habits to the Habits table and commits these changes.
    :param db: An initialized sqlite3 database connection.
    :param habit: The longest streak the has had.
    :param habit_name: The longest streak the has had.
    :return: None
    """
    cur = db.cursor()
    cur.execute("INSERT INTO longest_streak_table VALUES (?, ?)", (habit_name, habit))
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
    cur.execute("INSERT INTO tracker VALUES (?, ?)", (name, event_date))  # this formatting prevents sql injections
    db.commit()


def custom_data(db, name, event_date):
    """
    function to insert custom data (preferably for testing purposes
    :param db:
    :param name:
    :param event_date:
    :return:
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
    :return: all the rows from the Habit table.
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habits")  # remember to check if the data actually exists in the database
    rows = cur.fetchall()
    habits = []
    habit_names = []
    for row in rows:
        habits.append(row[0])
    for habit in habits:
        habit_names.append(habit)

    return habit_names


def return_adapted_habits(db, habit_name):
    """
    Returns all the rows from the Habit table where the name field matches the name argument.
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
