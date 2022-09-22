const fs = require("fs");
const express = require("express");
const axios = require("axios");
const cors = require("cors");
const X2JS = require("x2js");

const ue_approved_subjects = JSON.parse(fs.readFileSync("ue_approved.json"));
const PORT = 8080;
const dict_school_urls = {
  mags: "https://kamarportal.mags.school.nz/api/api.php",
  mrgs: "https://kamarportal.mrgs.school.nz/api/api.php",
  lynf: "https://lynfield.mystudent.school.nz/api/api.php",
};

const app = express();
const x2js = new X2JS();

const kamarheaders = {
  "Content-Type": "application/x-www-form-urlencoded",
  "User-Agent": "KAMAR API Demo",
  Origin: "file://",
  "X-Requested-With": "nz.co.KAMAR",
};

app.use(express.json());

// ------------------ GET methods API ------------------
app.get("/api/v2/auth", (req, res) => {
  res.json({ error: "unable to Auth with GET, use POST" });
});

app.get("/api/v2/results", (req, res) => {
  res.json({ error: "unable to GET results, use POST" });
});

// ------------------ POST methods API ------------------
app.post("/api/v2/auth", async (req, res) => {
  const req_data = req.body;

  if (!req_data.school || !req_data.username || !req_data.password) {
    return res.status(400).send({ error: "KAMAR LOGINS : `school`, `username` and `password` is required" });
  }
  if (!(req_data.school in dict_school_urls)) {
    return res
      .status(400)
      .send({ error: `'${req_data.school}' is not valid. Valid schools are [${Object.keys(dict_school_urls)}]` });
  }
  var authconfig = {
    method: "post",
    url: dict_school_urls[req_data.school.toLowerCase()],
    headers: kamarheaders,
    data: `Command=Logon&Key=vtku&Username=${req_data.username}&Password=${req_data.password}`,
  };

  await axios(authconfig)
    .then(function (response) {
      var responseObj = x2js.xml2js(response.data).LogonResults;
      if (responseObj.Error) {
        return res.status(401).send({ error: responseObj.Error });
      }
      res.status(200).send({
        authkey: responseObj.Key,
        student_id: responseObj.CurrentStudent,
      });
    })
    .catch(function (error) {
      console.log(error);
      res.status(500).send({ error: "Server might be down, sorry :/ - from auth" });
    });
});

app.post("/api/v2/results", async (req, res) => {
  const req_data = req.body;
  if (!req_data.school || !req_data.student_id || !req_data.authkey) {
    return res.status(400).send({ error: "KAMAR LOGINS : `school`, `student_id` and `authkey` is required" });
  }
  if (!(req_data.school in dict_school_urls)) {
    return res
      .status(400)
      .send({ error: `'${req_data.school}' is not valid. Valid schools are [${Object.keys(dict_school_urls)}]` });
  }
  var authconfig = {
    method: "post",
    url: dict_school_urls[req_data.school.toLowerCase()],
    headers: kamarheaders,
    data: `Command=GetStudentResults&Key=${req_data.authkey}&StudentID=${req_data.student_id}`,
  };

  await axios(authconfig)
    .then(function (response) {
      var responseObj = x2js.xml2js(response.data).StudentResultsResults;
      var student_subjects = {};

      if (responseObj.Error) {
        return res.status(401).send({ error: responseObj.Error });
      }

      // Including not ue approved
      let all_lvl3_results = responseObj.ResultLevels.ResultLevel.filter((r) => r.NCEALevel == 3)[0].Results.Result;

      //Rankscore return
      rankscorecalc = (g, c) => {
        switch (g) {
          case "Achieved with Excellence":
            return 4 * parseInt(c);
          case "Achieved with Merit":
            return 3 * parseInt(c);
          case "Achieved":
            return 2 * parseInt(c);
          default:
            return 0;
        }
      };

      // Only ue approved and correct subject added (unsorted)
      unsorted_final_results = {};
      all_lvl3_results.forEach((e) => {
        let rs = rankscorecalc(e.Grade, e.Credits);
        if (ue_approved_subjects[e.Number] in student_subjects) {
          student_subjects[ue_approved_subjects[e.Number]][0] += rs;
          student_subjects[ue_approved_subjects[e.Number]][1] += parseInt(e.CreditsPassed);
        } else {
          student_subjects[ue_approved_subjects[e.Number]] = [rs, parseInt(e.CreditsPassed)];
        }
        if (student_subjects[ue_approved_subjects[e.Number]][1] <= 24) {
          unsorted_final_results[e.Number] = {
            subject: ue_approved_subjects[e.Number],
            rs_contribution: rs,
            grade: e.Grade,
            credits: e.CreditsPassed,
            as_name: e.Title,
            publish_date: e.ResultPublished,
          };
        }
      });

      res.status(200).send(unsorted_final_results);

      //TODO 24 max, top 5, 80 best
    })
    .catch(function (error) {
      console.log(error);
      res.status(500).send({ error: "Server might be down, sorry :/ - from results" });
    });
});

app.listen(PORT, () => {
  console.log(`Server is running http://localhost:${PORT}`);
});
