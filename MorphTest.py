import unittest
from Morph import Morph

class MorphTest(unittest.TestCase):
    def setUp(self):
        self.morph = Morph("TestMorph", True, "Test Recessive", "Test No Issue", "Test No Issue Desc")
    
    def test_setMorphName(self):
        newName = "NewMorphName"
        self.morph.setMorphName(newName)
        self.assertEqual(newName, self.morph.name)
    
    def test_getMorphName(self):
        getName = self.morph.getMorphName()
        self.assertEqual("TestMorph", getName)

    def test_getMorphIssue(self):
        getIssue = self.morph.getMorphIssue()
        self.assertEqual("Test No Issue", getIssue)
    
    def test_getMorphVisibility(self):
        getVisibility = self.morph.getMorphVisibility()
        self.assertEqual(True, getVisibility)
    
    def test_setMorphVisibility(self):
        self.morph.setMorphVisibility(False)
        self.assertEqual(False, self.morph.isVisible)
        
        with self.assertRaises(TypeError): # Check that non-boolean values raise a TypeError
            self.morph.setMorphVisibility("String")
            
        self.assertEqual(False, self.morph.isVisible) # Check that the above ^ did not overwrite the morph visibility
    
if __name__ == '__main__':
    unittest.main(verbosity=2)