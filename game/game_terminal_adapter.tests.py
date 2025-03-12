import io
import unittest
import unittest.mock
from game_terminal_adapter import GameTerminalAdapter


class GameTerminalAdapterTests(unittest.TestCase):

    def test_getActionTaken(self):
        gt = GameTerminalAdapter()

        actualResult = gt.getActionTaken("Grab! the, sword?", {"inventory", "N", "S"}, {"grab", "talk", "attack"}, {"azazel", "chair", "sword"})
        expectedResult = ['grab', 'sword']
        self.assertEqual(actualResult, expectedResult)

        actualResult = gt.getActionTaken("Talk to the merchant Azazel and attack the zombie", {"inventory", "N", "S"}, {"grab", "talk", "attack"}, {"azazel", "chair", "sword"})
        expectedResult = ['talk', 'azazel']
        self.assertEqual(actualResult, expectedResult)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_println1(self, mock_stdout):
        gt = GameTerminalAdapter(5)

        gt.println("")
        actualResult = mock_stdout.getvalue()
        expectedResult = ""
        self.assertEqual(actualResult, expectedResult)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_println2(self, mock_stdout):
        gt = GameTerminalAdapter(5)
        gt.println(" ")
        actualResult = mock_stdout.getvalue()
        expectedResult = " \n\n"
        self.assertEqual(actualResult, expectedResult)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_println3(self, mock_stdout):
        gt = GameTerminalAdapter(5)
        gt.println("12345")
        actualResult = mock_stdout.getvalue()
        expectedResult = "12345\n\n"
        self.assertEqual(actualResult, expectedResult)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_println4(self, mock_stdout):
        gt = GameTerminalAdapter(5)
        gt.println("123456")
        actualResult = mock_stdout.getvalue()
        expectedResult = "123456\n\n"
        self.assertEqual(actualResult, expectedResult)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_println5(self, mock_stdout):
        gt = GameTerminalAdapter(5)
        gt.println("12345 12345")
        actualResult = mock_stdout.getvalue()
        expectedResult = "12345\n \n12345\n\n"
        self.assertEqual(actualResult, expectedResult)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_println6(self, mock_stdout):
        gt = GameTerminalAdapter(5)
        gt.println("12345 123 12345 1234")
        actualResult = mock_stdout.getvalue()
        expectedResult = "12345\n 123 \n12345\n 1234\n\n"
        self.assertEqual(actualResult, expectedResult)


if __name__ == '__main__':
    unittest.main()
