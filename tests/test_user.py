import unittest

from user import User


class UserTest(unittest.TestCase):
    def test_level_up_across_several_levels(self):
        user = User(1, "Тарас")
        self.assertEqual(user.exp_handler(35), "level_up")  # 10 + 20 spent, 5 left
        self.assertEqual((user.level, user.exp, user.total_xp), (3, 5, 35))

    def test_big_loss_drops_several_levels_without_negative_xp(self):
        user = User(1, "Тарас")
        user.exp_handler(35)
        self.assertEqual(user.exp_handler(-30), "level_down")
        self.assertEqual((user.level, user.exp, user.total_xp), (1, 5, 5))

    def test_xp_never_below_zero(self):
        user = User(1, "Тарас")
        user.exp_handler(-4)
        self.assertEqual((user.level, user.exp), (1, 0))

    def test_titles(self):
        user = User(1, "Тарас")
        self.assertEqual(user.title, "Джура")
        user.level = 30
        self.assertEqual(user.title, "Гетьман")


if __name__ == "__main__":
    unittest.main()
