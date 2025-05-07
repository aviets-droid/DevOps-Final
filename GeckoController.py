# Aisling Viets
# GeckoController.py

import psycopg2
import Morph
from GeckoModel import GeckoModel
import GeckoView


class GeckoController:
    geckoModel = GeckoModel
    geckoView = GeckoView
    geckos = []

    def __init__(self, geckoModel, geckoView):
        self.geckoModel = geckoModel
        self.geckoView = geckoView

    def startView(self):
        while True:
            startinput = self.geckoView.printStartMenu()

            if startinput == 0:
                break
            elif startinput == 1:
                self.newCollection()
            elif startinput == 2:
                newgecko = self.geckoView.newGeckoRoutine()
                self.convertMorphs(newgecko)  # Populate morph list from DB
                self.addGecko(newgecko)
            elif startinput == 3:
                self.fetchAllGeckos()
                for gecko in self.geckos:
                    self.geckoView.printGeckoInfo(gecko)
            elif startinput == 4:
                self.clearCollection()
            else:
                break

    def setGecko(self, gecko):
        self.geckoModel = gecko

    def getGecko(self):
        return self.geckoModel

    def convertMorphs(self, gecko):
        for morph in gecko.morphstr:
            morphobj = self.fetchMorph(morph, "BaseMorphs")
            if morphobj == -1:
                morphobj = self.fetchMorph(morph, "MorphCombos")
            if morphobj == -1:
                morphobj = self.fetchMorph(morph, "PolygenicTraits")
            gecko.addHealthInfo(gecko, morphobj.getMorphIssue())
            gecko.addMorph(gecko, morphobj)

    def newCollection(self):
        try:
            conn = psycopg2.connect(
                "dbname=LeopardGeckos user=postgres password=#2Truckee port=5433"
            )
        except:
            print("Database failed to connect.\n")

        cur = conn.cursor()
        try:
            cur.execute(
                """CREATE TABLE IF NOT EXISTS usercollection (
                name text PRIMARY KEY,
                sex text,
                age int,
                morphs text,
                healthInfo text);"""
            )
        except:
            return -1
        conn.commit()
        cur.close()
        conn.close()

    def clearCollection(self):
        try:
            conn = psycopg2.connect(
                "dbname=LeopardGeckos user=postgres password=#2Truckee port=5433"
            )
        except:
            print("Database failed to connect.\n")

        cur = conn.cursor()
        cur.execute("""DROP TABLE usercollection;""")
        conn.commit()
        cur.close()
        conn.close()

    def addGecko(self, gecko):
        self.newCollection()  # Ensure that the user table exists
        try:
            conn = psycopg2.connect(
                "dbname=LeopardGeckos user=postgres password=#2Truckee port=5433"
            )
        except:
            print("Database failed to connect.\n")

        cur = conn.cursor()
        cur.execute(
            """INSERT INTO usercollection (name, sex, age, morphs, healthInfo) VALUES (%s, %s, %s, %s, %s);""",
            (
                gecko.getName(gecko),
                gecko.getSex(gecko),
                gecko.getAge(gecko),
                gecko.getMorphNames(gecko),
                gecko.getHealthInfo(gecko),
            ),
        )

        conn.commit()
        # cur.close()
        # conn.close()

    # Fill geckos list with geckos from the database
    def fetchAllGeckos(self):
        try:
            conn = psycopg2.connect(
                "dbname=LeopardGeckos user=postgres password=#2Truckee port=5433"
            )
        except:
            print("Database failed to connect.\n")

        cur = conn.cursor()
        cur.execute(f"""SELECT * FROM usercollection;""")
        for record in cur:
            gecko = GeckoModel(
                record[0], record[1], record[2], record[3], record[4], ""
            )
            if gecko not in self.geckos:
                self.geckos.append(gecko)

        conn.commit()

        cur.close()
        conn.close()

    # Fetches the morph of a given name and from a given table, returns morph object with retrieved info
    def fetchMorph(self, morphName, tablename):
        # Connect and fetch information from the database
        try:
            conn = psycopg2.connect(
                "dbname=LeopardGeckos user=postgres password=#2Truckee port=5433"
            )
        except:
            print("Database failed to connect.\n")

        # print(morphName) # DEBUG PRINT

        cur = conn.cursor()

        try:
            cur.execute(
                f"""SELECT name, type, issue, description FROM "{tablename}" LEFT JOIN "HealthInfo" ON "{tablename}".name = "HealthInfo".morph WHERE name = '{morphName}';"""
            )
        except:
            return -1

        data = cur.fetchone()
        # print(data) # DEBUG PRINT
        conn.commit()

        # New morph object
        try:
            morph = Morph.Morph(data[0], True, data[1], data[2], data[3])
        except TypeError:
            return -1

        # Disconnect the database
        cur.close()
        conn.close()

        # Return a morph object with the data retrieved from the DB
        return morph
