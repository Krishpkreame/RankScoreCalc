import re
import xmltodict
import requests


class kamar_api():
    def getauthkey(school, user, pswd):
        url = "https://kamarportal.{}.school.nz/api/api.php".format(
            school)

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'KAMAR API Demo',
            'Origin': 'file://',
            'X-Requested-With': 'nz.co.KAMAR'
        }

        response = requests.request(
            "POST",
            url,
            headers=headers,
            data='Command=Logon&Key=vtku&Username={0}&Password={1}'.format(user, pswd))

        infodict = xmltodict.parse(response.text)["LogonResults"]

        if "Success" not in infodict:
            return infodict

        if infodict["Success"] == "YES":
            print(infodict)
            return {"AccessLevel": infodict["AccessLevel"], "id": infodict["CurrentStudent"], "key": infodict["Key"]}

    def getresults(school, student_id, authkey):
        url = "https://kamarportal.{}.school.nz/api/api.php".format(
            school)

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'KAMAR API Demo',
            'Origin': 'file://',
            'X-Requested-With': 'nz.co.KAMAR'
        }

        payload = "Command=GetStudentResults" + "&Key=" + \
            authkey + "&StudentID=" + student_id

        response = requests.request(
            "POST", url, headers=headers, data=payload)
        unfilter = xmltodict.parse(response.text)
        results = {}
        for i in unfilter["StudentResultsResults"]["ResultLevels"]["ResultLevel"]:
            if i['NCEALevel'] == "3":
                level3results = i["Results"]["Result"]
                for y in level3results:
                    if y["Grade"] == "Not Achieved":
                        results.update(
                            {y["Number"]: [0, "Not Achieved", 0, y["Title"]]})
                    elif y["Grade"] == "Achieved":
                        results.update(
                            {y["Number"]: [int(y["CreditsPassed"]), "Achieved", int(y["CreditsPassed"]) * 2, y["Title"]]})
                    elif y["Grade"] == "Achieved with Merit":
                        results.update({
                            y["Number"]: [int(y["CreditsPassed"]), "Merit", int(y["CreditsPassed"]) * 3, y["Title"]]})
                    elif y["Grade"] == "Achieved with Excellence":
                        results.update({
                            y["Number"]: [int(y["CreditsPassed"]), "Excellence", int(y["CreditsPassed"]) * 4, y["Title"]]})

        return results
