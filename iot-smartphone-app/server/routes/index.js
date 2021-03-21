let express = require("express");
let router = express.Router();
let fs = require('fs')

// fetch the url of the service to call when generating text
var BROKER_URL = process.env.BROKER_URL
var BROKER_PORT = process.env.BROKER_PORT

// Main Route
router.get("/", function(req, res){
    res.render("register_device.ejs", {BROKER_URL: BROKER_URL, BROKER_PORT: BROKER_PORT});
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
  res.render("gen_train_data.ejs", {BROKER_URL: BROKER_URL, BROKER_PORT: BROKER_PORT, USER: username});
});

// Main Route
router.get("/test", function(req, res){
  var username = req.query.user
  res.render("gen_test_data.ejs", {BROKER_URL: BROKER_URL, BROKER_PORT: BROKER_PORT, USER: username});
});

router.get("/about", function(req, res){
  var username = req.query.user
  res.render("about.ejs", {BROKER_URL: BROKER_URL, BROKER_PORT: BROKER_PORT, USER: username});
});


module.exports = router;