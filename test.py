import requests

# This is the Overpass API website
URL = "https://overpass-api.de/api/interpreter"

# This is the question we ask it:
# "Give me cafés in a small area"
QUERY = """
[out:json];
node["amenity"="cafe"](52.52,13.40,52.53,13.41);
out;
"""

# Send the question to Overpass
response = requests.post(URL, data=QUERY)

# If something went wrong, crash loudly
response.raise_for_status()

# Turn the answer into Python data
data = response.json()

# Print the raw answer so we can see it
print(data)
print(data['elements'])
