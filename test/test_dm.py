
import unittest


class Test(unittest.TestCase):


    def test_off_topic(self):
        self.assertEqual("What can I call you?", dialogManager.off_topic({"off_topic":"Hi"}))


if __name__ == "__main__":
    import sys
    sys.path.append("../dm")
    from dm import dialogManager
    unittest.main()