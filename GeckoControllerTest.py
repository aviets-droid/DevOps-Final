import unittest
from unittest.mock import patch, MagicMock
from GeckoController import GeckoController
from GeckoModel import GeckoModel
from GeckoView import GeckoView
from Morph import Morph

class TestGeckoController(unittest.TestCase):

    def setUp(self):

        self.mock_gecko_model = MagicMock()
        self.mock_gecko_view = MagicMock()
        self.controller = GeckoController(self.mock_gecko_model, self.mock_gecko_view)

        self.mock_gecko = MagicMock()
        self.mock_gecko.getName.return_value = "Leo"
        self.mock_gecko.getSex.return_value = "Female"
        self.mock_gecko.getAge.return_value = 12
        self.mock_gecko.getMorphNames.return_value = "Tangerine"
        self.mock_gecko.getHealthInfo.return_value = ["Healthy"]

    @patch('psycopg2.connect')
    def test_new_collection(self, mock_connect): # Test new collection, using mocked cursor
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        self.controller.newCollection()
        
        # Connect and check that the commands were executed (using assertIn multiple times to avoid issues with Python text formatting)
        mock_connect.assert_called_once_with("dbname=LeopardGeckos user=postgres password=#2Truckee port=5433")
        called_args = mock_cursor.execute.call_args[0][0]
        self.assertIn("CREATE TABLE IF NOT EXISTS usercollection", called_args)
        self.assertIn("name text PRIMARY KEY", called_args)
        self.assertIn("sex text", called_args)
        self.assertIn("age int", called_args)
        self.assertIn("morphs text", called_args)
        self.assertIn("healthInfo text", called_args)
        
        mock_cursor.close.assert_called_once()
        mock_connect.return_value.close.assert_called_once()

    @patch('psycopg2.connect')
    def test_add_gecko(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        self.controller.addGecko(self.mock_gecko)
        
        mock_cursor.execute.assert_called_with(
            """INSERT INTO usercollection (name, sex, age, morphs, healthInfo) VALUES (%s, %s, %s, %s, %s);""",
            ("Leo", "Female", 12, "Tangerine", ["Healthy"])
        )
        mock_cursor.close.assert_called_once()
        mock_connect.return_value.close.assert_called_once()

    @patch('psycopg2.connect')
    def test_clear_collection(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        self.controller.clearCollection()
        
        mock_cursor.execute.assert_called_once_with("""DROP TABLE usercollection;""")
        mock_cursor.close.assert_called_once()
        mock_connect.return_value.close.assert_called_once()

    @patch('psycopg2.connect')
    def test_fetch_all_geckos(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        mock_cursor.__iter__.return_value = iter([
            ("Leo", "Female", 12, "Tangerine", "Healthy")
        ])

        self.controller.fetchAllGeckos()

        self.assertEqual(len(self.controller.geckos), 1)
        self.assertEqual(self.controller.geckos[0].getName(), "Leo")
        mock_cursor.execute.assert_called_once_with("SELECT * FROM usercollection;")
        mock_cursor.close.assert_called_once()
        mock_connect.return_value.close.assert_called_once()

    @patch('psycopg2.connect')
    def test_convert_morphs(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        mock_morph = MagicMock()
        self.mock_gecko.morphstr = ["Tangerine"]
        mock_morph.getMorphName.return_value = "Tangerine"
        mock_morph.getMorphIssue.return_value = "No Issues"
        
        self.controller.fetchMorph = MagicMock(return_value=mock_morph)
        
        self.controller.convertMorphs(self.mock_gecko)
        
        self.controller.fetchMorph.assert_called_with("Tangerine", "BaseMorphs")
        
        self.mock_gecko.addHealthInfo.assert_called_with(self.mock_gecko, "No Issues")
        self.mock_gecko.addMorph.assert_called_with(self.mock_gecko, mock_morph)
    
    @patch("psycopg2.connect")
    def test_new_collection_creates_table(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        self.controller.newCollection()

        mock_cursor.execute.assert_called_with("""CREATE TABLE IF NOT EXISTS usercollection (
                name text PRIMARY KEY,
                sex text,
                age int,
                morphs text,
                healthInfo text);""")
        mock_cursor.close.assert_called_once()
        mock_connect.return_value.close.assert_called_once()

    @patch("psycopg2.connect")
    def test_convert_morphs_fetches_morphs_and_updates_gecko(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = ("Tangerine", "Base", "No Issues", "Orange colored morph")

        mock_gecko = MagicMock()
        mock_gecko.morphstr = ["Tangerine"]
        mock_gecko.addHealthInfo = MagicMock()
        mock_gecko.addMorph = MagicMock()

        self.controller.convertMorphs(mock_gecko)

        mock_cursor.execute.assert_called_with(
            """SELECT name, type, issue, description FROM "BaseMorphs" LEFT JOIN "HealthInfo" ON "BaseMorphs".name = "HealthInfo".morph WHERE name = 'Tangerine';"""
        )
        mock_gecko.addHealthInfo.assert_called_with(mock_gecko, "No Issues")
        self.assertTrue(mock_gecko.addMorph.called)

    @patch("psycopg2.connect")
    def test_clear_collection_drops_table(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        self.controller.clearCollection()

        mock_cursor.execute.assert_called_with("DROP TABLE usercollection;")
        mock_cursor.close.assert_called_once()
        mock_connect.return_value.close.assert_called_once()

if __name__ == '__main__':
    unittest.main(verbosity=2)
