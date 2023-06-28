from analyse import longest_streak_func, calculate_current_streak, same_periodicity, current_weekly_streak, longest_weekly_streak
from db import get_db, add_habit, check_habit, return_streaks, return_habits
from habit import Habit


class TestHabit:

    def setup_method(self):
        self.db = get_db(':memory:')
        add_habit(self.db, "read", "read everyday", "daily", 0)
        add_habit(self.db, "write", "write daily", "daily", 0)
        add_habit(self.db, "study", "study daily", "daily", 0)
        add_habit(self.db, "draw", "draw weekly", "weekly", 0)
        add_habit(self.db, "sauna", "sauna weekly", "weekly", 0)

        # read data
        check_habit(self.db, "read", "2023-04-01")
        check_habit(self.db, "read", "2023-04-02")
        check_habit(self.db, "read", "2023-04-03")
        check_habit(self.db, "read", "2023-04-04")
        check_habit(self.db, "read", "2023-04-05")
        check_habit(self.db, "read", "2023-04-06")

        check_habit(self.db, "read", "2023-04-08")
        check_habit(self.db, "read", "2023-04-09")

        check_habit(self.db, "read", "2023-04-11")
        check_habit(self.db, "read", "2023-04-12")
        check_habit(self.db, "read", "2023-04-13")

        check_habit(self.db, "read", "2023-04-21")
        check_habit(self.db, "read", "2023-04-22")

        check_habit(self.db, "read", "2023-06-10")
        check_habit(self.db, "read", "2023-06-11")
        check_habit(self.db, "read", "2023-06-12")
        check_habit(self.db, "read", "2023-06-13")

        check_habit(self.db, "read", "2023-06-15")
        check_habit(self.db, "read", "2023-06-16")
        check_habit(self.db, "read", "2023-06-17")

        # write data
        check_habit(self.db, "write", "2023-05-01")
        check_habit(self.db, "write", "2023-05-02")
        check_habit(self.db, "write", "2023-05-03")
        check_habit(self.db, "write", "2023-05-04")
        check_habit(self.db, "write", "2023-05-05")
        check_habit(self.db, "write", "2023-05-06")

        check_habit(self.db, "write", "2023-05-08")
        check_habit(self.db, "write", "2023-05-09")
        check_habit(self.db, "write", "2023-05-10")
        check_habit(self.db, "write", "2023-05-11")
        check_habit(self.db, "write", "2023-05-12")
        check_habit(self.db, "write", "2023-05-13")
        check_habit(self.db, "write", "2023-05-14")
        check_habit(self.db, "write", "2023-05-15")
        check_habit(self.db, "write", "2023-05-16")

        check_habit(self.db, "write", "2023-05-18")
        check_habit(self.db, "write", "2023-05-19")
        check_habit(self.db, "write", "2023-05-20")
        check_habit(self.db, "write", "2023-05-21")

        check_habit(self.db, "write", "2023-05-27")
        check_habit(self.db, "write", "2023-05-28")
        check_habit(self.db, "write", "2023-05-29")
        check_habit(self.db, "write", "2023-05-30")

        # study data
        check_habit(self.db, "study", "2023-06-01")
        check_habit(self.db, "study", "2023-06-02")
        check_habit(self.db, "study", "2023-06-03")
        check_habit(self.db, "study", "2023-06-04")
        check_habit(self.db, "study", "2023-06-05")
        check_habit(self.db, "study", "2023-06-06")
        check_habit(self.db, "study", "2023-06-07")
        check_habit(self.db, "study", "2023-06-08")
        check_habit(self.db, "study", "2023-06-09")
        check_habit(self.db, "study", "2023-06-10")
        check_habit(self.db, "study", "2023-06-11")
        check_habit(self.db, "study", "2023-06-12")
        check_habit(self.db, "study", "2023-06-13")

        check_habit(self.db, "study", "2023-06-15")
        check_habit(self.db, "study", "2023-06-16")
        check_habit(self.db, "study", "2023-06-17")
        check_habit(self.db, "study", "2023-06-18")
        check_habit(self.db, "study", "2023-06-19")

        check_habit(self.db, "study", "2023-06-21")
        check_habit(self.db, "study", "2023-06-22")

        check_habit(self.db, "study", "2023-06-25")
        check_habit(self.db, "study", "2023-06-26")

        # draw data
        check_habit(self.db, "draw", "2023-06-01")

        check_habit(self.db, "draw", "2023-06-07")
        check_habit(self.db, "draw", "2023-06-08")
        check_habit(self.db, "draw", "2023-06-09")

        check_habit(self.db, "draw", "2023-06-14")

        check_habit(self.db, "draw", "2023-06-22")

        check_habit(self.db, "draw", "2023-06-25")
        check_habit(self.db, "draw", "2023-06-26")

        # sauna data
        check_habit(self.db, "sauna", "2023-05-31")

        check_habit(self.db, "sauna", "2023-06-07")
        check_habit(self.db, "sauna", "2023-06-08")
        check_habit(self.db, "sauna", "2023-06-09")

        check_habit(self.db, "sauna", "2023-06-14")
        check_habit(self.db, "sauna", "2023-06-15")

        check_habit(self.db, "sauna", "2023-06-21")

        check_habit(self.db, "sauna", "2023-06-28")

    def test_habit(self):
        habit = Habit("test_habit", "test_description", "test_periodicity", 0)

        habit.get_name()
        habit.store_habit(self.db)
        habit.set_name("code")
        habit.get_periodicity()
        habit.set_periodicity("d")
        habit.add_event(self.db)

    def test_read(self):
        streak_info = return_streaks(self.db, "read")
        streak_dates = []
        for x in streak_info:
            streak_dates.append(x[1])
            # print(streak_dates)
        longest_streak = longest_streak_func(streak_dates)
        assert longest_streak == 6
        current_streak = calculate_current_streak(streak_dates)
        assert current_streak == 3

    def test_write(self):
        streak_info = return_streaks(self.db, "write")
        streak_dates = []
        for x in streak_info:
            streak_dates.append(x[1])
            # print(streak_dates)
        longest_streak = longest_streak_func(streak_dates)
        assert longest_streak == 9
        current_streak = calculate_current_streak(streak_dates)
        assert current_streak == 4

    def test_study(self):
        streak_info = return_streaks(self.db, "study")
        streak_dates = []
        for x in streak_info:
            streak_dates.append(x[1])
            # print(streak_dates)
        longest_streak = longest_streak_func(streak_dates)
        assert longest_streak == 13
        current_streak = calculate_current_streak(streak_dates)
        assert current_streak == 2

    def test_draw(self):
        streak_info = return_streaks(self.db, "draw")
        streak_dates = []
        for x in streak_info:
            streak_dates.append(x[1])
            # print(streak_dates)
        longest_streak = longest_weekly_streak(streak_dates)
        assert longest_streak == 2
        current_streak = current_weekly_streak(streak_dates)
        assert current_streak == 1

    def test_sauna(self):
        streak_info = return_streaks(self.db, "sauna")
        streak_dates = []
        for x in streak_info:
            streak_dates.append(x[1])
            # print(streak_dates)
        longest_streak = longest_weekly_streak(streak_dates)
        assert longest_streak == 5
        current_streak = current_weekly_streak(streak_dates)
        assert current_streak == 5

    def test_same_periodicity(self):
        daily_habits = []
        weekly_habits = []
        for habit in same_periodicity(self.db, "daily"):
            daily_habits.append(habit)
        for habit in same_periodicity(self.db, "weekly"):
            weekly_habits.append(habit)
        assert "write" in daily_habits
        assert "read" in daily_habits
        assert "study" in daily_habits
        assert "draw" in weekly_habits
        assert "sauna" in weekly_habits

    def test_list_habits(self):
        habits_list = return_habits(self.db)
        assert "write" in habits_list
        assert "read" in habits_list
        assert "study" in habits_list
        assert "draw" in habits_list
        assert "sauna" in habits_list



