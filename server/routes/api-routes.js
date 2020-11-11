module.exports = function(app) {
    app.get("/api/table", function(req, res){
        let apiInfo = {
            url: "", //URL to external API for data
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
