const API = {
    getData: function() {
        console.log("hello?");
        $.ajax({
            url: "http://13.58.61.47:5000/api/v1/items/ranked?emphasized=profit,profit%20percent&history_region_id=Etherium_Reach_10000027",
            type: "GET",
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .done((response)=> {
            console.log(response);
        });

    }
}


API.getData();