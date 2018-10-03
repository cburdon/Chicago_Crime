function heatmapdata() {

    var myMap = L.map('map', {
        center: [30.2672, -97.7431],
        zoom: 13
    });
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.streets',
        accessToken: "pk.eyJ1Ijoia3VsaW5pIiwiYSI6ImNpeWN6bjJ0NjAwcGYzMnJzOWdoNXNqbnEifQ.jEzGgLAwQnZCv9rA6UTfxQ"
    }).addTo(myMap);
    
    var data = "https://raw.githubusercontent.com/mattmurphey25/data_trafficers_project/master/Real-Time_Traffic_Incident_Reports_Cleaned.csv"

    // data = "https://data.austintexas.gov/resource/r3af-2r8x.json"

    d3.csv(data).then(successHandle, errorHandle);
    function errorHandle(error) {
        console.log(error)
    }

    function successHandle(response) {
        console.log(response);
        var heatArray = [];
        
        for (var i = 0; i < response.length; i++) {
            var lat = +response[i].Latitude;
            var lng = +response[i].Longitude;
            if (location) {
                heatArray.push(L.latLng(lat, lng))
            }
        }
        // console.log(heatArray)
        var heat = L.heatLayer(heatArray, {
        radius: 20,
        blur: 35
        }).addTo(myMap)
    // console.log(heat)
    }
}

heatmapdata();
