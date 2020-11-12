const API = {
    getData: function() {
        console.log("hello?");
       return $.ajax({
            url: "/api/profit-table",
            type: "GET",
            headers: {
                'Content-Type': 'application/json'
            }
        })
    }
}


API.getData();