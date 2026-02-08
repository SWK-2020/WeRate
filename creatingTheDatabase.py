import sqlite3


if __name__ == "__main__":

    connect = sqlite3.connect("businessesDatabase.db")
    cursor = connect.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS businessList(
                    hashBusiness TEXT PRIMARY KEY,
                    businessName TEXT,
                    category TEXT,
                    averageRating INTEGER,
                    priceRange INTEGER,
                    dateLastUpdated TEXT,
                    lattitude REAL,
                    longitude REAL,
                    postCode TEXT,
                    addressLineOne TEXT,
                    addressLineTwo TEXT
                )
                """)

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS contactList(
                    contactText TEXT,
                    contactType TEXT,
                    hashBusiness TEXT,
                    FOREIGN KEY (hashBusiness) REFERENCES businessList(hashBusiness)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE,
                    PRIMARY KEY (contactText, hashBusiness)
                )
                """)

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS operatingTimes(
                    openingTime TEXT,
                    closingTime TEXT,
                    day TEXT,
                    hashBusiness TEXT,
                    FOREIGN KEY (hashBusiness) REFERENCES businessList(hashBusiness)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE,
                    PRIMARY KEY (hashBusiness,openingTime,day)

                )
                """)

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS tags(
                    tagName TEXT PRIMARY KEY
                )
                """)

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS tagsCombiner(
                    tagName TEXT,
                    hashBusiness TEXT,
                    FOREIGN KEY (hashBusiness) REFERENCES businessList(hashBusiness)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE,
                    FOREIGN KEY (tagName) REFERENCES tags(tagName)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE,
                    PRIMARY KEY (hashBusiness,tagName)

                )
                """)

    connect.commit()
    connect.close()
