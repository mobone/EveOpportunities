var path = require("path");
const axios = require('axios');

module.exports = function (app) {

    // paged served at root is profit table
    app.get("/", function (req, res) {
        try {
            axios.get("http://73.164.50.141:5000/api/v1/items/ranked?emphasized=profit,profit%20percent&history_region_id=Etherium_Reach_10000027")
            .then((response)=> { 
            res.render("profit", { item: response.data });
            });
        } catch (err) {
            if (err) throw err;
        }   
        
    });


    app.get("/trade-hub", function (req, res) {
        try {
            // change this URL to be the tradehub URL
            axios.get("http://73.164.50.141:5000/api/v1/items/ranked?emphasized=profit,profit%20percent&history_region_id=Etherium_Reach_10000027")
            .then((response)=> { 
            res.render("tradeHub", { item: response.data });
            });
        } catch (err) {
            if (err) throw err;
        }   
        
    });




    app.get("/charts", function (req, res) {
        res.render("charts");
    });

}