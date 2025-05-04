# Aisling Viets
# GeckoModel.py

import Morph

class GeckoModel:
    name = ""
    age = 0
    morphs = [] # List of Morph objects
    healthInfo = [] # List of strings
    morphstr = []
    
    def __init__(self, name, sex, age, morphs, healthInfo, morphstr):
        self.name = name
        self.sex = sex
        self.age = age
        self.morphs = morphs
        self.healthInfo = healthInfo
        self.morphstr = morphstr
    
    def getName(self):
        return self.name
    
    def setName(self, newName):
        self.name = newName
        
    def getAge(self):
        return self.age
    
    def setAge(self, newAge):
        self.age = newAge
    
    def getSex(self):
        return self.sex
    
    def setSex(self, newSex):
        self.sex = newSex
        
    def getMorphNames(self):
        morphNames = []
        for morph in self.morphs:
            morphNames.append(morph.getMorphName())
        concatMorphs = ", ".join(morphNames)
        return concatMorphs
    
    def getMorphs(self):
        return self.morphs
    
    # Add a morph if it doesn't already exist
    def addMorph(self, morph):
        if morph not in self.morphs:
            self.morphs.append(morph)
            return 0
        else:
            return -1 # Morph requested to be added is already in the list
    
    # Remove a morph at given index
    def removeMorph(self, idx):
        del self.morphs[idx]
    
    def getHealthInfo(self):
        return self.healthInfo
    
    def addHealthInfo(self, info):
        self.healthInfo.append(info)
    
    # Removes a health note at given index
    def removeHealthInfo(self, idx):
        del self.healthInfo[idx]
    
    def clearMorphs(self):
        self.morphs.clear()
        self.morphstr.clear()
    
    def clearHealth(self):
        self.healthInfo.clear()