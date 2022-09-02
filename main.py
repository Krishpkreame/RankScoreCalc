import re
from kamarapi import *
from encrypt import local_encryption
from filterapi import filter_kamar
if __name__ == "__main__":
    cryt = local_encryption()
    while True:
        if input("New user? [y/n]") == "y":
            temp1 = input("what school u goto? \n").lower() + "\n"
            for i in range(0, 50):
                print("")
            temp1 += input("username : \n").lower() + "\n"
            for i in range(0, 50):
                print("")
            temp1 += input("password : \n")
            for i in range(0, 50):
                print("")
            cryt.encrypt(temp1.encode("utf-8"))
            break
        else:
            with open("secret.dll", "wb") as file:
                file.write(
                    b"gAAAAABjD9uqq5hAe6_bgLyH7j-GZ-h6rcw8aRmhaXpGWKVLg-vAn-p8gTOdP-dOcgMsVyHkENnUqzF2CY2g7ZcHTZYejUrEYG579TgegzKroBOHjWMXU9Y=")
            break

    cred_details = cryt.decryptlogins()
    k = kamar_api(cred_details[0], cred_details[1], cred_details[2])
    results = k.getresults()
    print("-----------\n", results, "\n-------------")
    print(k.student_id, " :\n", len(results))

    filterObj = filter_kamar(open("uestandards.json").read())
    sortedKamar = filterObj.filter_results(results)
    # print(sortedKamar)
    sum = 0
    for i in sortedKamar.values():
        print(i, "\n\n")
        for x in i.keys():
            if x == "subject_credits_earned":
                continue
            sum += i[x][2]
    print("rankscore: ", sum)
