# Import necessary libraries
import requests
import time
import random
import string
import hashlib
import pandas as pd
import json


# Inputvärden som skall skickas med i API-frågan
callerId = "Rikard Fahlström"
time = str(time.time())
unique = str(''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16)))
key = "vOl0qzQAp1tKtsFvzHXDPpA27ga9ZE5AdJaGiIIX"
hashstr = hashlib.sha1((callerId+time+key+unique).encode('utf-8')).hexdigest()

query_type = 'listings'  # Enter 'listings', 'sold' eller 'areas'
query_city = 'vasastan'  # Enter city of interest
offset = '0'
limit = str(10)  # Max results = 500
object_type = 'lägenhet'
#living_area =

# Själva API-frågan
r = requests.get("https://api.booli.se/"+query_type+"?q="+query_city+"&callerId="+callerId+"&time="+time+"&unique="+unique+"&hash="+str(hashstr)+"&limit="+limit+"&offset="+offset+"&objectType="+object_type)

print("Status code from API request = " + str(r.status_code))

if r.status_code != 200:
    print('fail')
    exit()

test = json.loads(r.text)

print("Number of listings returned in API = " + str(len(test['listings'])))
print(test['listings'])
print("Below is output from code: " + "\n")
#_________________________________________________-

for item in test['listings']:
    try:
        print(item['location']['address']['streetAddress'] + ", " + item['location']['region']['countyName'])
        print("Utgångspris: " + str(item['listPrice']))
        print(item['objectType'])
        print("Antal rum: " + str(item['rooms']))
        print(item['url'])
        print("\n")

    except KeyError:
        print(str(item['location']['address']['streetAddress']) + " is missing some data.")
        print('\n')

listing_fields = ['listPrice','published','url']
listings = pd.DataFrame(test['listings'], columns=listing_fields)
#print(listings)


# range av kvadratmeter
# range av rum