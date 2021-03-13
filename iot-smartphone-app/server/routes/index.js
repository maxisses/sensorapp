var express = require("express");
var router = express.Router();
const fs = require('fs')

// fetch the url of the service to call when generating text
var LOCALIP = process.env.LOCALIP
var BROKER_SERVICE = process.env.BROKER_SERVICE

fs.readFile('public/certs/ca.crt', 'utf8' , (err, data) => {
    if (err) {
      console.log(fs.readdirSync('.'))
      console.error(err)
      return
    }
    console.log(data)
  })

var CRT = "proces.env.CRT"

// Main Route
router.get("/", function(req, res){
    res.render("gen_train_data.ejs", {LOCALIP: LOCALIP, BROKER_SERVICE: BROKER_SERVICE, CRT: CRT});
});


module.exports = router;