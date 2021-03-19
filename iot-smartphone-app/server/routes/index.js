let express = require("express");
let router = express.Router();
let fs = require('fs')

// fetch the url of the service to call when generating text
var LOCALIP = process.env.LOCALIP
var BROKER_SERVICE = process.env.BROKER_SERVICE

// Main Route
router.get("/", function(req, res){
    res.render("register_device.ejs", {LOCALIP: LOCALIP, BROKER_SERVICE: BROKER_SERVICE});
});

// register logic
router.post("/register", function(req,res){
  var username = req.body.username
  console.log(username)
  req.flash("success", "Willkommen " + username + ", deine Registrierung war erfolgreich")
  res.redirect("/train?user=" + username);
});

// Main Route
router.get("/train", function(req, res){
  var username = req.query.user
  res.render("gen_train_data.ejs", {LOCALIP: LOCALIP, BROKER_SERVICE: BROKER_SERVICE, USER: username});
});

// Main Route
router.get("/test", function(req, res){
  var username = req.query.user
  res.render("gen_test_data.ejs", {LOCALIP: LOCALIP, BROKER_SERVICE: BROKER_SERVICE, USER: username});
});

router.get("/about", function(req, res){
  var username = req.query.user
  res.render("about.ejs", {LOCALIP: LOCALIP, BROKER_SERVICE: BROKER_SERVICE, USER: username});
});


module.exports = router;