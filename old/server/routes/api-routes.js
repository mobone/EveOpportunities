const { default: Axios } = require("axios");

const axios = require('axios');

module.exports = function(app) {

    app.get("/api/profit-table", function(req, res){
        
        try {
            axios.get("http://73.164.50.141:5000/api/v1/items/ranked?emphasized=profit,profit%20percent&history_region_id=Etherium_Reach_10000027")
            .then((response)=> {
            console.log(response.data);
            res.json(response.data);
            });
        } catch (err) {
            if (err) throw err;
        }
        
    });


//end of export bracket 
}
