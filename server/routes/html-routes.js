var path = require("path");

module.exports = function (app) {

    // paged served at root is profit table
    app.get("/", function (req, res) {
        res.render("profit");
    });

    app.get("/charts", function (req, res) {
        res.render("charts");
    });

}