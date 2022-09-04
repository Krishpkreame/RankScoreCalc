from kamarapi import *
from filterapi import filter_kamar
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('home.html')


@app.route('/', methods=['POST'])
def my_form_post():
    k = kamar_api(
        request.form['school'],
        request.form['username'],
        request.form['password'])
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

    return "rankscore: " + str(sum)


if __name__ == '__main__':
    app.run()
