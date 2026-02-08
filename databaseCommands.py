import sqlite3, hashlib

def hashed(text):
    """
    Docstring for hashed
    
    :param text: the text that needs to be encoded using hashlib
    """
    encoded = text.encode('utf-8')
    hashedValue = hashlib.sha256(encoded)
    return hashedValue.hexdigest()


def addEntry(unifiedList):
    businessList = unifiedList[0]
    contactList = unifiedList[1]
    operatingTimes = unifiedList[2]
    tags = unifiedList[3]
    
    
    """
    Docstring for addEntry
    This function takes in all the various datapoints and stores them into the database

    :param businessList: list containing attributes in the order 
    [businessName,category,averageRating,priceRange,dateLastUpdated,lattitude,longitude,postCode,addressLineOne,addressLineTwo]
    
    :param contactList: list containing attributes in the order 
    [[contactText,contactType]]

    :param operatingTimes: list containing attributes in the order
    [[openingTime,closingTime,day]]

    :param tags: list containing the different tags belonging to each entry
    """
    connect = sqlite3.connect("businessesDatabase.db")
    cursor = connect.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    print(businessList[0],businessList[5],businessList[6],businessList[7],businessList[8])
    
    hashValue = hashed(businessList[0]+businessList[5]+businessList[6]+businessList[7]+businessList[8])

    try:
        cursor.execute(f"INSERT INTO businessList VALUES ('{hashValue}', '{businessList[0]}', '{businessList[1]}', '{businessList[2]}', '{businessList[3]}', '{businessList[4]}', '{businessList[5]}', '{businessList[6]}', '{businessList[7]}', '{businessList[8]}', '{businessList[9]}')")
    except:
        pass
    for i in contactList:
        try: 
            cursor.execute(f"INSERT INTO contactList VALUES ('{i[0]}', '{i[1]}', '{hashValue}')")
        except:
            pass
    try: # duplicate handling
        for i in operatingTimes:
            cursor.execute(f"INSERT INTO operatingTimes VALUES ('{i[0]}', '{i[1]}', '{i[2]}', '{hashValue}')")
    except:
        pass
    
    for i in tags:
        try:
            cursor.execute(f"INSERT INTO tags VALUES ('{i}')")
        except:
            print(i + " repeated")
    try:
        cursor.execute(f"INSERT INTO tagsCombiner VALUES ('{i}', '{hashValue}')")
    except:
        pass
    

    connect.commit()
    connect.close()

def deleteEntry(businessHash):
    """
    Docstring for deleteEntry
    
    :param businessHash: hash value made using the hashed function, since users will not be expected 
    to delete items this action is reserved for developers, hence only a hash value is required.
    """
    connect = sqlite3.connect("businessesDatabase.db")
    cursor = connect.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute(f"DELETE FROM businessList WHERE hashBusiness = '{businessHash}'")
    print("Deleted")

    connect.commit()
    connect.close()

def readEntry(businessHash):
    """
    Docstring for readEntry
    This function is meant to be used internally, returning exactly one value every time as the hash function is unique


    :param businessHash: hash value belonging to the business we are looking for
    """
    connect = sqlite3.connect("businessesDatabase.db")
    cursor = connect.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    data,dataOne, dataTwo, dataThree, dataFour = [],[],[],[],[]

    cursor.execute(f"SELECT * FROM businessList WHERE hashBusiness = '{businessHash}'")
    dataOne = cursor.fetchone()

    cursor.execute(f"SELECT contactText, contactType FROM contactList WHERE hashBusiness = '{businessHash}'")
    dataTwo = cursor.fetchall()

    cursor.execute(f"SELECT openingTime, closingTime, day FROM operatingTimes WHERE hashBusiness = '{businessHash}'")
    dataThree = cursor.fetchone()

    cursor.execute(f"SELECT tagName FROM tagsCombiner WHERE hashBusiness = '{businessHash}'")
    dataFour = cursor.fetchall()

    data = [dataOne, dataTwo, dataThree, dataFour]

    connect.commit()
    connect.close()




    return data

def readEntryWithName(businessName):
    """
    Docstring for readEntryWithName
    This function takes in a name of a business and outputs a list of all businesses with a similar name.
    
    :param businessName: name of the business, or a name similar ot the business' name
    """
    connect = sqlite3.connect("businessesDatabase.db")
    cursor = connect.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute( f"SELECT hashBusiness FROM businessList " 
                   f"WHERE LOWER(businessName) LIKE LOWER('%{businessName}%')" 
                   )
    data = cursor.fetchall()

    dataFormatted = []

    for i in range(0, len(data)):
        dataFormatted.append("")
        dataFormatted[i] = readEntry(data[i][0]) 

    connect.commit()
    connect.close()
    return dataFormatted
