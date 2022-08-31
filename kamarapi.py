import xmltodict
import requests


class kamar_api():
    def __init__(self, school, user, pswd):
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
                for y in i["Results"]["Result"]:
                    # print(y, "\n--------------------------------\n")
                    crntsub = y["Title"].split("3")[0].strip()
                    subfield = y["SubField"]
                    if crntsub not in self.list_of_subs.keys():
                        self.list_of_subs.update({crntsub: subfield})
                    else:
                        print(crntsub, subfield, "is already in the list")
                        if subfield not in self.list_of_subs.values():
                            self.list_of_subs.update({subfield: crntsub})
                    if y["Grade"] == "Not Achieved":
                        self.rank_score += int(y["CreditsPassed"])*1
                    elif y["Grade"] == "Achieved":
                        self.rank_score += int(y["CreditsPassed"])*2
                    elif y["Grade"] == "Achieved with Merit":
                        self.rank_score += int(y["CreditsPassed"])*3
                    elif y["Grade"] == "Achieved with Excellence":
                        self.rank_score += int(y["CreditsPassed"])*4
        print(self.list_of_subs)
        return self.rank_score
