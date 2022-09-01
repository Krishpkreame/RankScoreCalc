import xmltodict
import requests
import json


class kamar_api():
    def __init__(self, school, user, pswd):
        self.testsubdic = {}
        self.url = "https://kamarportal.{}.school.nz/api/api.php".format(
            school)

        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'KAMAR API Demo',
            'Origin': 'file://',
            'X-Requested-With': 'nz.co.KAMAR'
        }

        self.response = requests.request(
            "POST",
            self.url,
            headers=self.headers,
            data='Command=Logon&Key=vtku&Username={0}&Password={1}'.format(user, pswd))

        self.infodict = xmltodict.parse(self.response.text)["LogonResults"]

        self.key = self.infodict["Key"]
        self.student_id = self.infodict["CurrentStudent"]

        print(self.infodict)  # ! Remove

    def get_rank_score(self, grade, creds):
        if grade == "Achieved":
            return creds * 2
        elif grade == "Achieved with Merit":
            return creds * 3
        elif grade == "Achieved with Excellence":
            return creds * 4
        else:
            return 0

    def getresults(self):
        self.rank_score = 0
        self.payload = "Command=GetStudentResults" + "&Key=" + \
            self.key + "&StudentID=" + self.student_id

        self.response = requests.request(
            "POST", self.url, headers=self.headers, data=self.payload)
        with open("test.xml", "w") as f:
            f.write(self.response.text)
        self.results = xmltodict.parse(self.response.text)

        self.list_of_subs = {}
        for i in self.results["StudentResultsResults"]["ResultLevels"]["ResultLevel"]:
            if i['NCEALevel'] == "3":
                self.level3results = i["Results"]["Result"]
                for y in self.level3results:
                    print(y, "\n--------------------------------\n")
                    crntsub = y["Title"].split("3")[0].strip()
                    subfield = y["SubField"]
                    if crntsub not in self.list_of_subs.keys():
                        self.list_of_subs.update({crntsub: subfield})
                    else:
                        print(crntsub, subfield, "is already in the list")
                        if subfield not in self.list_of_subs.values():
                            self.list_of_subs.update({subfield: crntsub})
        print(self.list_of_subs.keys())
        for n in self.list_of_subs.keys():
            self.testsubdic.update({n: {"totalcreds": 0, "results": []}})
        print("self.testsubdic", self.testsubdic)
        for y in self.level3results:
            tempnotfound = True
            for x in self.list_of_subs.keys():
                if(y["SubField"] == x):
                    add_rank_score = self.get_rank_score(
                        y["Grade"], int(y["CreditsPassed"]))
                    self.testsubdic[x]["totalcreds"] += int(y["CreditsPassed"])
                    self.testsubdic[x]["results"].append(
                        [y["Number"],
                         y["Grade"],
                         int(y["CreditsPassed"]),
                         add_rank_score])

                    print(y["Number"], x, "----",
                          y["Grade"], add_rank_score, "\n")
                    tempnotfound = False
                    self.rank_score += add_rank_score
                    break
            if tempnotfound:
                for x in self.list_of_subs.keys():
                    if(y["Title"].split("3")[0].strip() == x):
                        add_rank_score = self.get_rank_score(
                            y["Grade"], int(y["CreditsPassed"]))
                        self.testsubdic[x]["totalcreds"] += int(
                            y["CreditsPassed"])

                        self.testsubdic[x]["results"].append([
                            y["Number"],
                            y["Grade"],
                            int(y["CreditsPassed"]),
                            add_rank_score])

                        print(y["Number"], x, "----",
                              y["Grade"], add_rank_score, "\n")
                        self.rank_score += add_rank_score
                        break
        with open(self.student_id+".json", "w") as f:
            f.write(json.dumps(self.testsubdic))
        return self.rank_score
