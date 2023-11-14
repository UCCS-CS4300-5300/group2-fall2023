$.getScript(`https://maps.googleapis.com/maps/api/js?key=${google_maps_api_key}`) 
.done(function( _script, _textStatus ) {
    initMap()
})
.fail(function(_jqxhr, _settings, _exception) {
    console.log("Failed to load Google Maps Script!")
});


function initMap() {
    let map = new google.maps.Map(document.getElementById("harvestly-map"), {
        center: { lat: latitude, lng: longitude },
        zoom: 15
    });

    var marker = new google.maps.Marker({
        map: map,
        position: {
            lat: latitude,
            lng: longitude
        },
        title: "Farmers Market Location"
    });
}