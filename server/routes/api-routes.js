const { default: Axios } = require("axios");

const axios = require('axios');

module.exports = function(app) {

    app.get("/api/profit-table", function(req, res){
        let apiInfo = {
            url: "http://13.58.61.47:5000/api/v1/items/ranked?emphasized=profit,profit%20percent&history_region_id=Etherium_Reach_10000027", //URL to external API for data
            method: "GET"
        }

        axios.get(apiInfo.url)
        .then((response)=> {
            console.log(response);
            res.json(response);
        });
    });


//end of export bracket 
}
