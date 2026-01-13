import json
f = open('data.json')
data = json.load(f)
f.close()
print(data)
print(data["features"])
print(data["features"][0]["geometry"])
for i in data["features"]:
    print(i["geometry"]["coordinates"][0])