import requests 
import json
#resp = requests.get('https://s3.amazonaws.com/dolartoday/data.json')
#a = json.loads(resp.content)
resp = requests.get('https://s3.amazonaws.com/dolartoday/data.json')
a = json.loads(resp.text)
usd = a['USD']
dolar = usd['transferencia']

print("Marico el precio del dolar es:","$"+str(dolar))

