$.getScript(`https://maps.googleapis.com/maps/api/js?key=${google_maps_api_key}&libraries=places`) 
.done(function( _script, _textStatus ) {
    google.maps.event.addListener(window, "load", initAutocomplete())
})
.fail(function(_jqxhr, _settings, _exception) {
    console.log("Failed to load Google Maps Places Script!")
});

function initAutocomplete() {
    // get existing input
    let existing = document.getElementById("id_location").value

    // initialize the autocomplete field
    let autocomplete = new google.maps.places.Autocomplete(
        document.getElementById("id_location"),
        {
            componentRestrictions: {
                country: ["US", "CA", "MX", "FR", "DE", "IT", "ES", "GB", "NL", "BE"]
            },
        },
    );

    // restore the existing value back to the input field
    if(existing !== null && existing !== "")
        document.getElementById("id_location").value = existing;

    // listen for the place selection event
    autocomplete.addListener("place_changed", function () {
        var place = autocomplete.getPlace();

        // log the selected place details
        console.log("Place Name:", place.name);
    });
}