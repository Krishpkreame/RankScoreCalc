import xmltodict
import requests


class kamar_api():
    global __uestandards
    __uestandards = {
        "Accounting": [91404, 91405, 91406, 91407, 91408, 91409],
        "Agriculture & Horticulture": [91528, 91529, 91530, 91531, 91532],
        "Biology": [91601, 91602, 91603, 91604, 91605, 91606, 91607, 91818, 91819],
        "Business Studies": [
            91380, 91382, 91384, 91379, 91381, 91383, 91385, 91869, 91870, 91871
        ],
        "Calculus": [91573, 91574, 91575, 91576, 91577, 91578, 91579, 91587],
        "Chemistry": [91387, 91388, 91389, 91390, 91391, 91392, 91393],
        "Chinese": [91533, 91534, 91535, 91536, 91537],
        "Classical Studies": [91394, 91395, 91396, 91397, 91398],
        "Construction and Mechanical Technologies": [
            91620, 91621, 91622, 91623, 91624, 91625, 91626
        ],
        "Cook Islands Maori": [91538, 91539, 91540, 91541, 91542],
        "Dance": [91588, 91589, 91590, 91591, 91592, 91593, 91594, 91595],
        "Design (Practical Art)": [91440, 91445, 91450, 91455, 91460],
        "Design and Visual Communication": [91627, 91628, 91629, 91630, 91631],
        "Digital Technologies and Hangarau Matihiko": [
            91900, 91901, 91902, 91903, 91904, 91905, 91906, 91907, 91908, 91909
        ],
        "Drama": [91512, 91513, 91514, 91515, 91516, 91517, 91518, 91519, 91520],
        "Earth and Space Science": [91410, 91411, 91412, 91413, 91414, 91415],
        "Economics": [91399, 91400, 91401, 91402, 91403],
        "Education for Sustainability": [90828, 90831, 90832, 91735, 91736, 91820],
        "English": [91472, 91473, 91474, 91475, 91476, 91477, 91478, 91479, 91480],
        "French": [91543, 91544, 91545, 91546, 91547],
        "Generic Technology": [
            91608, 91609, 91610, 91611, 91612, 91613, 91614, 91615, 91616, 91617, 91618,
            91619
        ],
        "Geography": [91426, 91427, 91428, 91429, 91430, 91431, 91432, 91433],
        "German": [91548, 91549, 91550, 91551, 91552],
        "Hauora": [91811, 91812, 91813, 91814, 91815, 91816],
        "Health Education": [91461, 91462, 91463, 91464, 91465],
        "History": [91434, 91435, 91436, 91437, 91438, 91439],
        "History of Art": [91482, 91483, 91484, 91485, 91488, 91486, 91487, 91489],
        "Home Economics": [91466, 91467, 91468, 91469, 91470, 91471],
        "Indonesian": [91645, 91646, 91647, 91648, 91649],
        "Japanese": [91553, 91554, 91555, 91556, 91557],
        "Korean": [91558, 91559, 91560, 91561, 91562],
        "Latin": [91506, 91507, 91508, 91509, 91510, 91511],
        "Media Studies": [91490, 91491, 91492, 91493, 91494, 91495, 91496, 91497],
        "Music Studies": [
            91417, 91418, 91419, 91421, 91424, 91416, 91420, 91422, 91423, 91425, 91849
        ],
        "New Zealand Sign Language": [91822, 91823, 91824, 91825],
        "Ngā Mahi a te Rēhia": [91850, 91851, 91852, 91853, 91854],
        "Ngā Toi": [91855, 91856, 91857, 91858, 91859],
        "Ngā Toi Puoro": [91860, 91861, 91862, 91863, 91864],
        "Painting (Practical Art)": [91441, 91446, 91451, 91456],
        "Photography (Practical Art)": [91442, 91447, 91452, 91457],
        "Physical Education": [
            91498, 91499, 91500, 91501, 91502, 91503, 91504, 91505, 91789
        ],
        "Physics": [91521, 91522, 91523, 91524, 91525, 91526, 91527],
        "Printmaking (Practical Art)": [91443, 91448, 91453, 91458],
        "Processing Technologies": [91643, 91644],
        "Psychology": [91872, 91873, 91874, 91875, 91876],
        "Religious Studies": [90825, 90826, 90827, 91725],
        "Samoan": [91563, 91564, 91565, 91566, 91567],
        "Sculpture (Practical Art)": [91444, 91449, 91454, 91459],
        "Social Studies": [91596, 91597, 91598, 91599, 91600],
        "Spanish": [91568, 91569, 91570, 91571, 91572],
        "Statistics": [91580, 91581, 91582, 91583, 91584, 91585, 91586],
        "Te Ao Haka": [91984, 91985, 91986, 91987],
        "Te Reo Māori": [91650, 91651, 91652, 91653, 91654],
        "Te Reo Rangatira": [
            91803, 91804, 91805, 91806, 91807, 91808, 91809, 91810, 91817
        ],
        "Tikanga ā-Iwi": [
            91826, 91827, 91828, 91829, 91830, 91831, 91832, 91833, 91834, 91835
        ],
        "Tongan": [91679, 91680, 91681, 91682, 91683]
    }

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
            return {"AccessLevel": 1, "id": infodict["CurrentStudent"], "key": infodict["Key"]}

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

        def rankpergrade(grade, credit):
            if grade == "Achieved":
                return int(credit) * 2
            if grade == "Achieved with Merit":
                return int(credit) * 3
            if grade == "Achieved with Excellence":
                return int(credit) * 4
            else:
                return 0

        for i in unfilter["StudentResultsResults"]["ResultLevels"]["ResultLevel"]:
            if i['NCEALevel'] == "3":
                level3results = i["Results"]["Result"]
                for y in level3results:
                    for x in __uestandards:
                        if(int(y["Number"]) in __uestandards[x]):
                            if x not in results:
                                results.update({x: {}})
                            results[x].update({
                                y["Number"]: [
                                    int(y["CreditsPassed"]),
                                    y["Grade"],
                                    rankpergrade(
                                        y["Grade"], y["CreditsPassed"]),
                                    y["Title"]]})
        return results
