module.exports = function(app) {
    app.get("/api/table", function(req, res){
        let apiInfo = {
		url: "http://13.58.61.47:5000/api/v1/items/ranked?emphasized=profit,profit%20percent&history_region_id=Etherium_Reach_10000027", //URL to external API for data
            method: "GET"
            // headers: {
        }

        $.ajax(apiInfo)
        .done((response)=> {
            console.log(response);
            // populate table here
        });
    });


//end of export bracket 
}
