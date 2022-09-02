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
        self.payload = "Command=GetStudentResults" + "&Key=" + \
            self.key + "&StudentID=" + self.student_id

        self.response = requests.request(
            "POST", self.url, headers=self.headers, data=self.payload)
        self.unfilter = xmltodict.parse(self.response.text)
        self.results = {}
        for i in self.unfilter["StudentResultsResults"]["ResultLevels"]["ResultLevel"]:
            if i['NCEALevel'] == "3":
                self.level3results = i["Results"]["Result"]
                for y in self.level3results:
                    if y["Grade"] == "Not Achieved":
                        self.results.update(
                            {y["Number"]: [0, "Not Achieved", 0, y["Title"]]})
                    elif y["Grade"] == "Achieved":
                        self.results.update(
                            {y["Number"]: [int(y["CreditsPassed"]), "Achieved", int(y["CreditsPassed"]) * 2, y["Title"]]})
                    elif y["Grade"] == "Achieved with Merit":
                        self.results.update({
                            y["Number"]: [int(y["CreditsPassed"]), "Merit", int(y["CreditsPassed"]) * 3, y["Title"]]})
                    elif y["Grade"] == "Achieved with Excellence":
                        self.results.update({
                            y["Number"]: [int(y["CreditsPassed"]), "Excellence", int(y["CreditsPassed"]) * 4, y["Title"]]})

        return self.results
