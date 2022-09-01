import json

data = json.loads(open("18036.json").read())

sorted = {}

orglist = []
for i in data.keys():
    orglist.append(data[i]["totalcreds"])


for i in data.keys():
    highest = 0
    for i in orglist:
        if i >= highest:
            highest = i

    sorted.update({list(data.keys())[orglist.index(
        highest)]: data[list(data.keys())[orglist.index(highest)]]})
    orglist[orglist.index(highest)] = -1

for i in sorted.keys():
    sorted[i]["results"].sort(key=lambda x: x[3], reverse=True)

with open("18036.json", "w") as f:
    f.write(json.dumps(sorted))
