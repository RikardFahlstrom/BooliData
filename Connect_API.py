import requests
import time
import random
import string
import hashlib

# Inputvärden som skall skickas med i API-frågan
callerId = "ENTER_CALLERID"
time = str(time.time())
unique = str(''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16)))
key = "ENTER_KEY"
hashstr = hashlib.sha1((callerId+time+key+unique).encode('utf-8')).hexdigest()

query_type = 'listings'  # Enter 'listings', 'sold' eller 'areas'
query_city = 'falun'  # Enter city of interest
offset = '0'
limit = str(100)  # Max results = 500

# Själva API-frågan
r = requests.get("https://api.booli.se/"+query_type+"?q="+query_city+"&callerId="+callerId+"&time="+time+"&unique="+unique+"&hash="+str(hashstr)+"&limit="+limit+"&offset="+offset)

print(r.status_code)

if r.status_code != 200:
    print('fail')
    exit()

# Spara datan i en variabel
response_dict = r.json()

# Kollar vilka keys som finns
print(response_dict.keys())
