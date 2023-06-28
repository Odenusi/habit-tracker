from db import add_habit, check_habit
# import sqlite3


class Habit:
    def __init__(self, name: str, description: str, periodicity: str, longest_streak: int):
        """Habit class to track habit streaks/events

        :param name: name of the habit
        :param description: description of the habit
        :param periodicity: how often the habit should be done (days/weeks)
        :param longest_streak: the longest streak of the habit
        """
        self.name = name  # name of the habit
        self.description = description  # short description of the habit
        self.periodicity = periodicity  # the habit's periodicity
        self.longest_streak = longest_streak  # the longest streak the habit has had
        self.is_checked = False  # habit is not complete by default   This line might be unnecessary

    def set_name(self, name):
        """
        Sets/resets the name of the habit
        :param name: (New) name of the habit
        :return: None
        """
        self.name = name

    def get_name(self):
        """
        Returns the name of the habit
        :return: the name of the habit
        """
        return self.name

    def set_periodicity(self, periodicity):
        """
        Sets or resets the periodicity of the habit.
        :param periodicity:
        :return: None
        """
        # set periodicity might be used to reset or change a habit's periodicity.
        self.periodicity = periodicity

    def get_periodicity(self):
        """
        Returns the periodicity of the habit.
        :return: the periodicity of the habit.
        """
        return self.periodicity

    def set_longest_streak(self, longest_streak):
        """
        Sets or resets the periodicity of the habit.
        :param longest_streak:
        :return: None
        """

        self.longest_streak = longest_streak

    def get_longest_streak(self):
        """
        Returns the periodicity of the habit.
        :return: the periodicity of the habit.
        """
        return self.longest_streak

    def update_longest_streak(self, streak):
        if streak > self.longest_streak:
            self.longest_streak = streak
            return True
        else:
            self.longest_streak = self.longest_streak
            return False

    def store_habit(self, db):
        """
        Stores the habit in our database by adding it to our habits table.
        :param db: an initialized sqlite3 database connection
        :return: None
        """
        add_habit(db, self.name, self.description, self.periodicity, self.longest_streak)

    def add_event(self, db, date: str = None):
        """
        Checks off our habit by adding it to the tracker table.
        :param db: an initialized sqlite3 database connection
        :param date: The date our habit is checked off.
        :return: None
        """
        check_habit(db, self.name, date)

        self.is_checked = True

    def test_event(self, db, date):
        """
        check off function with custom date
        :param db:
        :param date:
        :return:
        """
        check_habit(db, self.name, date)
        self.is_checked = True
