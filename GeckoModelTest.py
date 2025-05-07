import unittest
from unittest.mock import MagicMock
from GeckoModel import GeckoModel


class TestGeckoModel(unittest.TestCase):

    def setUp(self):
        self.mock_morph1 = MagicMock()
        self.mock_morph1.getMorphName.return_value = "Hypo"
        self.mock_morph2 = MagicMock()
        self.mock_morph2.getMorphName.return_value = "Tangerine"

        self.gecko = GeckoModel(
            name="Leo",
            sex="Female",
            age=2,
            morphs=[self.mock_morph1],
            healthInfo=["Healthy"],
            morphstr=["Hypo"],
        )

    def test_get_and_set_name(self):
        self.assertEqual(self.gecko.getName(), "Leo")
        self.gecko.setName("Nova")
        self.assertEqual(self.gecko.getName(), "Nova")

    def test_get_and_set_age(self):
        self.assertEqual(self.gecko.getAge(), 2)
        self.gecko.setAge(3)
        self.assertEqual(self.gecko.getAge(), 3)

    def test_get_and_set_sex(self):
        self.assertEqual(self.gecko.getSex(), "Female")
        self.gecko.setSex("Male")
        self.assertEqual(self.gecko.getSex(), "Male")

    def test_get_morph_names(self):
        morph_names = self.gecko.getMorphNames()
        self.assertEqual(morph_names, "Hypo")

    def test_add_morph_success(self):
        result = self.gecko.addMorph(self.mock_morph2)
        self.assertEqual(result, 0)
        self.assertIn(self.mock_morph2, self.gecko.getMorphs())

    def test_add_morph_duplicate(self):
        result = self.gecko.addMorph(self.mock_morph1)
        self.assertEqual(result, -1)

    def test_remove_morph(self):
        self.gecko.addMorph(self.mock_morph2)
        self.assertEqual(len(self.gecko.getMorphs()), 2)
        self.gecko.removeMorph(0)
        self.assertNotIn(self.mock_morph1, self.gecko.getMorphs())

    def test_add_health_info(self):
        self.gecko.addHealthInfo("Needs more calcium")
        self.assertIn("Needs more calcium", self.gecko.getHealthInfo())

    def test_remove_health_info(self):
        self.gecko.removeHealthInfo(0)
        self.assertEqual(self.gecko.getHealthInfo(), [])

    def test_clear_morphs(self):
        self.gecko.clearMorphs()
        self.assertEqual(self.gecko.getMorphs(), [])
        self.assertEqual(self.gecko.morphstr, [])

    def test_clear_health(self):
        self.gecko.clearHealth()
        self.assertEqual(self.gecko.getHealthInfo(), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
