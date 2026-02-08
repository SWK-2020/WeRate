from bs4 import BeautifulSoup
import requests

from geopy.geocoders import Nominatim
loc = Nominatim(user_agent="Geopy Library")

def searchBusiness(name):
    #get correct url
    print(name)
    url = "https://api.ratings.food.gov.uk/Establishments"
    params = {"name": name}
    headers = {"x-api-version": "2"}
    #search up that term
    response = requests.get(url, headers=headers, params=params)
    
    #filter all results
    data = response.json()
    print(f"data : \n\n" + f"{data}")

    if data == {}:
        return None

    ret = []
    for estab in data["establishments"]: #get stuff from dictionary
        name = estab["BusinessName"]
        address = estab["AddressLine1"]+ ' ' +estab["AddressLine2"]+ ' ' + estab["AddressLine3"]+ ' ' +estab["AddressLine4"]
        postcode = estab["PostCode"]
        category = estab["BusinessType"]
        website = estab["LocalAuthorityWebSite"]
        email = estab["LocalAuthorityEmailAddress"]
        rating = estab["RatingValue"]
        phone = estab["Phone"]
        geocode = estab["geocode"]
        lastDate = estab["RatingDate"]
        ret.append(formatInfo(name,address,postcode,category,website,email,rating,phone,geocode, lastDate))
    return ret

def formatInfo(name, address, postcode, category, website, email, rating, phone, geocode, lastDate): # standards
    first = (name, category, rating, "", lastDate,
             str(geocode["latitude"]), str(geocode["longitude"]), postcode, address, "")
    second = ((website,"WEBSITE"), (email, "EMAIL"), (phone, "PHONE"))
    third = ("", "", "")
    forth = ("")
    return (first,second,third,forth)
