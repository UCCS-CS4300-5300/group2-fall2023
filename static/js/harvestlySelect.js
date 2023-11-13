function selectEvent(element, id) {
    if(element.classList.contains("selected-event")) {
        element.classList.remove("selected-event");
        document.getElementById("product-event").value = null;
    }
    else {
        // deselect all others
        var currentlySelected = document.querySelectorAll('.selected-event');
        currentlySelected.forEach(function(el) {
            el.classList.remove('selected-event');
        });

        element.classList.add("selected-event");
        document.getElementById("product-event").value = id;
    }
}