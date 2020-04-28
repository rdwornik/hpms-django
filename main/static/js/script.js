var API_URL = document
                    .querySelector("div [url-endpoint]")
                    .attributes
                    .getNamedItem("url-endpoint")
                    .value;

var displayJSON = function(query) {
    d3.json(API_URL + query, function(error, data){

        if(error){
            return console.warn(error);
        }

        d3.select('#query pre').html(query);
    })
}