import json

data = json.loads(open("18036.json").read())

longresults = []

while len(data.keys()) > 5:
    print("\n\n\n\nOnly 5 subjects allow")
    for i in range(len(data.keys())):
        print(i + 1, list(data.keys())[i])
    delete = input("Select one to delete or m to merge")
    if delete == "m":
        print("Merge")
        for i in range(len(data.keys())):
            print(i + 1, list(data.keys())[i])
        merge1 = int(input("Select first subject to merge")) - 1
        merge2 = int(input("Select second to merge")) - 1
        data[list(data.keys())[merge1]
             ]["totalcreds"] += data[list(data.keys())[merge2]]["totalcreds"]
        data[list(data.keys())[merge1]
             ]["results"] += data[list(data.keys())[merge2]]["results"]
        del data[list(data.keys())[merge2]]
    else:
        del data[list(data.keys())[int(delete) - 1]]

for i in data.keys():
    if data[i]["totalcreds"] > 24:
        sum = 0
        while sum < 24:
            sum += data[i]["results"][0][2]
            longresults.append(data[i]["results"].pop(0))
    else:
        longresults += data[i]["results"]
print(longresults)
totalrank = 0
for i in longresults:
    totalrank += i[3]
print(totalrank)
