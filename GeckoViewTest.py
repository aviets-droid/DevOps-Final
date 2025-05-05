import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

from GeckoView import GeckoView
from GeckoModel import GeckoModel

class TestGeckoView(unittest.TestCase):

    def setUp(self):
        self.mockGeckoModel = MagicMock()
        self.mockGeckoInstance = MagicMock()
        self.mockGeckoModel.GeckoModel.return_value = self.mockGeckoInstance
        self.view = GeckoView(self.mockGeckoModel)

    @patch('builtins.input', return_value='1')
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_start_menu_create_collection(self, mock_stdout, mock_input):
        result = self.view.printStartMenu()
        self.assertEqual(result, 1)
        self.assertIn("Created a new collection.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['Leo', 'Female', '12', '1', 'Tangerine', 'Healthy'])
    def test_new_gecko_routine(self, mock_input):
        new_gecko = self.view.newGeckoRoutine()

        self.assertEqual(new_gecko.name, 'Leo')
        self.assertEqual(new_gecko.sex, 'Female')
        self.assertEqual(new_gecko.age, 12)
        self.assertEqual(new_gecko.morphstr, ['Tangerine'])
        self.assertEqual(new_gecko.healthInfo, ['Healthy'])

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_gecko_info(self, mock_stdout):
        gecko = MagicMock()
        gecko.name = "Spike"
        gecko.sex = "Male"
        gecko.age = 3
        gecko.getMorphs.return_value = "Albino"
        gecko.getHealthInfo.return_value = "Perfect health"

        self.view.printGeckoInfo(gecko)
        output = mock_stdout.getvalue()
        self.assertIn("Spike, Male, 3 years old.", output)
        self.assertIn("Morphs: Albino", output)
        self.assertIn("Health-related notes: Perfect health", output)

if __name__ == '__main__':
    unittest.main()
