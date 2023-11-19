
// Runs when page is loaded
document.addEventListener("DOMContentLoaded", function() {
    // check if initial event is set
    try {
        if(initialEventID !== undefined && initialEventID !== null) {
            // get initially selected option element
            let elementID = `harvestly-event-option-${initialEventID}`;
            let element = document.getElementById(elementID);
            
            // select event element and update product-event value
            element.classList.add("selected-event")
            document.getElementById("product-event").value = initialEventID;
        }
    }
    catch(error) {
        console.log("Unable to set initial event selection:", error)
    }
});

function selectEvent(element, id) {
    if(element.classList.contains("selected-event")) {
        element.classList.remove("selected-event");

        try{
            document.getElementById("product-event").value = null;
        }
        catch(error) {
            console.log("Unable to update event selection. There must be a 'product-event' field:", error);
        }
    }
    else {
        // deselect all others
        var currentlySelected = document.querySelectorAll('.selected-event');
        currentlySelected.forEach(function(el) {
            el.classList.remove('selected-event');
        });

        element.classList.add("selected-event");

        try{
            document.getElementById("product-event").value = id;
        }
        catch(error) {
            console.log("Unable to update event selection. There must be a 'product-event' field:", error);
        }
    }
}