from habit import Habit
from db import get_db, add_habit, check_habit, get_habit_tracker_data
from analyse import calculate_streak


class TestHabit:

    def setup_method(self):
        self.db = get_db(':memory:')
        add_habit(self.db, "test_habit", "test_description", "test_periodicity")
        check_habit(self.db, "test_habit", "2022-07-08")
        check_habit(self.db, "test_habit", "2022-07-09")

        check_habit(self.db, "test_habit", "2022-07-11")
        check_habit(self.db, "test_habit", "2022-07-12")

    def test_habit(self):
        habit = Habit("test_habit_1", "test_description_1", "test_periodicity_1")

        habit.get_name()
        habit.store_habit(self.db)
        habit.set_name("code")
        habit.get_periodicity()
        habit.set_periodicity("1")
        habit.add_event(self.db)

    def test_db_habit(self):
        streak = calculate_streak(self.db, "test_habit")
        assert streak == 4

        data = get_habit_tracker_data(self.db, "test_habit")
        assert len(data) == 4

    # def teardown_method(self):
    #     import os
    #     os.remove('test.db')  # figure out a better way to test a database
    #     # This could be done using a database in memory
