function searchNearby() {
    const query =
        document.getElementById("search-query").value;

    alert("Searching for: " + query);
}
/////////////////////////////////////////////////////////////////////////////
function setSearch(value) {
        document.getElementById("search-input").value = value;
}
function setSearchLocal(value) {
        document.getElementById("search-input-local").value = value;
}
////////////////////////////////////////////////////////////////////////
function getLocation() {
    navigator.geolocation.getCurrentPosition(
        function(position) {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;

            document.getElementById("latitude").value = lat;
            document.getElementById("longitude").value = lng;
        },
        function() {
            alert("Unable to get your location.");
        }
    );
}
function getLocation() {
    navigator.geolocation.getCurrentPosition(
        function(position) {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;

            document.getElementById("latitude-bottom").value = lat;
            document.getElementById("longitude-bottom").value = lng;
        },
        function() {
            alert("Unable to get your location.");
        }
    );
}
///////////////////////////////////////////////////////////////////////////////////////
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
        function(position) {

            const lat = position.coords.latitude;
            const lng = position.coords.longitude;

            document.getElementById("latitude").value = lat;
            document.getElementById("longitude").value = lng;

            fetch(`/location?lat=${lat}&lng=${lng}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById("current-location").textContent =
                        data.address;
                });
        },
        function(error) {
            document.getElementById("current-location").textContent =
                "Location unavailable";
        }
    );
}
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
        function(position) {

            const lat = position.coords.latitude;
            const lng = position.coords.longitude;

            document.getElementById("latitude-bottom").value = lat;
            document.getElementById("longitude-bottom").value = lng;

            loadBusinessCount(lat, lng);

            fetch(`/location?lat=${lat}&lng=${lng}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById("current-location-bottom").textContent =
                        data.address;
                });
        },
        function(error) {
            document.getElementById("current-location-bottom").textContent =
                "Location unavailable";
        }
    );
}
///////////////////////////////////////////////////////////////////////////////////////////
document.querySelector(".search-box").addEventListener("submit", () => {
    document.getElementById("search-btn").innerText = "Searching...";
});
document.querySelector(".search-card").addEventListener("submit", () => {
    document.getElementById("search-btn-bottom").innerText = "Searching...";
});
/////////////////////////////////////////////////////////////////////////////////////////
window.open(
    `https://www.google.com/maps/search/${query}`,
    "_blank"
);
