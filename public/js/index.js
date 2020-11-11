const API = {
    getData = function() {
        
        return $.ajax({
            url: "/api/table",
            type: "GET"
        });

    }
}


API.getData();