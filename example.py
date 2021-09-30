import requests

try:
	res = requests.get("https://r6kvds.deta.dev/api/generator/orang", timeout=120)
	print(res.content)
except (requests.ConnectionError, requests.Timeout) as exception:
	print("Changed")
