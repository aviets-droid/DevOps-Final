import GeckoModel
import Morph


class GeckoView:
    geckoModel = GeckoModel

    def __init__(self, geckoModel):
        self.geckoModel = geckoModel

    @staticmethod
    def printStartMenu():
        print(
            "\n-- Leopard Gecko Collection Manager --\n\nSelect an action:\n1. Create a collection\n2. Add a gecko to my collection\n3. View my geckos\n4. Delete my collection table (erases all saved geckos!)"
        )
        print("0. Exit\n")
        userinput = int(input("Action: "))
        match (userinput):
            case 0:
                print("\nExiting.\n")
            case 1:
                print("\nCreated a new collection.\n")
            case 2:
                print("\nAdded gecko to your collection.\n")
            case 3:
                print("\nViewing your geckos:\n")
            case 4:
                print("\nCollection deleted.\n")
            case _:
                print("\nInvalid input.\n")
        return userinput

    @staticmethod
    def printGeckoInfo(gecko):
        print(
            "\n" + gecko.name + ", " + gecko.sex + ", " + str(gecko.age) + " years old."
        )
        print("Morphs: " + gecko.getMorphs())
        print("Health-related notes: " + gecko.getHealthInfo())

    @staticmethod
    def newGeckoRoutine():
        newgecko = GeckoModel.GeckoModel

        newgecko.clearHealth(newgecko)
        newgecko.clearMorphs(newgecko)

        print("-- Enter gecko details --\n")
        newgecko.setName(newgecko, input("Name: "))
        newgecko.setSex(newgecko, input("Sex: "))
        newgecko.setAge(newgecko, int(input("Age: ")))
        numMorphs = int(input("Enter the amount of morphs your gecko has: "))
        for i in range(numMorphs):
            newgecko.morphstr.append(str(input(f"Enter morph {i+1}: ")))
            # morph = Morph.Morph(str(input(f"Enter morph {i+1}: ")), True, "", "", "")
            # newgecko.addMorph(newgecko, morph)
        newgecko.healthInfo.append(input("Health-related notes: "))

        return newgecko
