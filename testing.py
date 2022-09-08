import requests
import xmltodict
url = "https://kamarportal.mags.school.nz/api/api.php"

payload = 'Command=Logon&Key=vtku&Username=kpatel6&Password=celm2Si'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'KAMAR API Demo',
    'Origin': 'file://',
    'X-Requested-With': 'nz.co.KAMAR'
}

response = requests.request("POST", url, headers=headers, data=payload)

infodict = xmltodict.parse(response.text)["LogonResults"]

print(infodict)
