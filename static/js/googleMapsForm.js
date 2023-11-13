// called when the HTML content is first loaded
document.addEventListener("DOMContentLoaded", function() {
    console.log(google_maps_api_key)

    // include the Google Maps Places API
    let script = document.createElement("script");
    script.src = `https://maps.googleapis.com/maps/api/js?key=${google_maps_api_key}&libraries=places`;
    script.defer = true;
    script.async = true;

    // function runs once the google maps script has been loaded
    script.onload = function() {
        // initialize the autocomplete field
        var autocomplete = new google.maps.places.Autocomplete(document.getElementById("id_location"));

        // Listen for the place selection event
        autocomplete.addListener("place_changed", function () {
            var place = autocomplete.getPlace();

            // Log the selected place details (you can customize this part)
            console.log("Place Name:", place.name);
            console.log("Address:", place.formatted_address);
            console.log("Latitude:", place.geometry.location.lat());
            console.log("Longitude:", place.geometry.location.lng());
        });
    }

    document.head.appendChild(script);
});