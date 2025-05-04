import unittest
from unittest.mock import patch, MagicMock
from GeckoController import GeckoController
from GeckoModel import GeckoModel
from GeckoView import GeckoView
from Morph import Morph

class TestGeckoController(unittest.TestCase):

    def setUp(self):
        # Mocking the GeckoModel and GeckoView classes
        self.mock_gecko_model = MagicMock()
        self.mock_gecko_view = MagicMock()
        self.controller = GeckoController(self.mock_gecko_model, self.mock_gecko_view)

        # Create a mock Gecko object
        self.mock_gecko = MagicMock()
        self.mock_gecko.getName.return_value = "Leo"
        self.mock_gecko.getSex.return_value = "Female"
        self.mock_gecko.getAge.return_value = 2
        self.mock_gecko.getMorphNames.return_value = "Hypo, Tangerine"
        self.mock_gecko.getHealthInfo.return_value = ["Healthy"]

    @patch('psycopg2.connect')
    def test_new_collection(self, mock_connect):
        # Mock database connection and cursor
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        # Call the method
        self.controller.newCollection()
        
        # Assert that the database connection and cursor are being used correctly
        mock_connect.assert_called_once_with("dbname=LeopardGeckos user=postgres password=#2Truckee port=5433")
        mock_cursor.execute.assert_called_with("""CREATE TABLE IF NOT EXISTS usercollection (
            name text PRIMARY KEY,
            sex text,
            age int,
            morphs text,
            healthInfo text);""")
        
        # Check that commit and close were called
        mock_cursor.close.assert_called_once()
        mock_connect.return_value.close.assert_called_once()

    @patch('psycopg2.connect')
    def test_add_gecko(self, mock_connect):
        # Mock the database connection and cursor
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        # Call the addGecko method
        self.controller.addGecko(self.mock_gecko)
        
        # Ensure that the necessary methods were called on the cursor
        mock_cursor.execute.assert_called_with(
            """INSERT INTO usercollection (name, sex, age, morphs, healthInfo) VALUES (%s, %s, %s, %s, %s);""",
            ("Leo", "Female", 2, "Hypo, Tangerine", ["Healthy"])
        )
        mock_cursor.close.assert_called_once()
        mock_connect.return_value.close.assert_called_once()

    @patch('psycopg2.connect')
    def test_clear_collection(self, mock_connect):
        # Mock the database connection and cursor
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        # Call the clearCollection method
        self.controller.clearCollection()
        
        # Ensure the DROP TABLE command was executed
        mock_cursor.execute.assert_called_once_with("""DROP TABLE usercollection;""")
        mock_cursor.close.assert_called_once()
        mock_connect.return_value.close.assert_called_once()

    @patch('psycopg2.connect')
    def test_fetch_all_geckos(self, mock_connect):
        # Mock the database connection and cursor
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        # Simulate a cursor returning rows from the database
        mock_cursor.fetchall.return_value = [
            ("Leo", "Female", 2, "Hypo, Tangerine", "Healthy")
        ]
        
        # Call the fetchAllGeckos method
        self.controller.fetchAllGeckos()
        
        # Verify that the Gecko was added to the geckos list
        self.assertEqual(len(self.controller.geckos), 1)
        self.assertEqual(self.controller.geckos[0].getName(), "Leo")
        mock_cursor.execute.assert_called_once_with(f"""SELECT * FROM usercollection;""")
        mock_cursor.close.assert_called_once()
        mock_connect.return_value.close.assert_called_once()

    @patch('psycopg2.connect')
    def test_convert_morphs(self, mock_connect):
        # Mock the database connection and cursor
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        # Mock the Morph class
        mock_morph = MagicMock()
        mock_morph.getMorphName.return_value = "Hypo"
        mock_morph.getMorphIssue.return_value = "No Issues"
        
        # Simulate the fetchMorph method to return the mock morph object
        self.controller.fetchMorph = MagicMock(return_value=mock_morph)
        
        # Call convertMorphs to simulate morph conversion
        self.controller.convertMorphs(self.mock_gecko)
        
        # Ensure the fetchMorph method was called correctly
        self.controller.fetchMorph.assert_called_with("Hypo", "BaseMorphs")
        
        # Ensure the morph was added to the gecko
        self.mock_gecko.addHealthInfo.assert_called_with(self.mock_gecko, "No Issues")
        self.mock_gecko.addMorph.assert_called_with(self.mock_gecko, mock_morph)

if __name__ == '__main__':
    unittest.main()
