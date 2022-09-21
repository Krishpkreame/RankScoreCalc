const express = require("express");
const cors = require("cors");
const axios = require("axios");

const PORT = 8080;

const app = express();

const kamarheaders = {
  "Content-Type": "application/x-www-form-urlencoded",
  "User-Agent": "KAMAR API Demo",
  Origin: "file://",
  "X-Requested-With": "nz.co.KAMAR",
};

app.use(express.json());

// GET methods API
app.get("/api/v2/auth", (req, res) => {
  res.json({ error: "Auth Not implemented yet - Krish" });
});

app.get("/api/v2/results", (req, res) => {
  res.json({ error: "Results Not implemented yet - Krish" });
});

// POST methods API
app.post("/api/v2/auth", async (req, res) => {
  const req_data = req.body;
  console.log(req_data);

  if (!req_data.schoolurl || !req_data.username || !req_data.password) {
    return res.sendStatus(400);
  }

  var authconfig = {
    method: "post",
    url: req_data.schoolurl,
    headers: kamarheaders,
    data: `Command=Logon&Key=vtku&Username=${req_data.username}&Password=${req_data.password}`,
  };

  await axios(authconfig)
    .then(function (response) {
      console.log(response.data);
      res.sendStatus(200);
    })
    .catch(function (error) {
      console.log(error);
      res.sendStatus(400);
    });

  //{ error: "WIP, returning values back", ...res });
});

app.listen(PORT, () => {
  console.log(`Server is running http://localhost:${PORT}`);
});
