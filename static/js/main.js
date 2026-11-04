/* =========================================================
   WALLAWALLA MAIN.JS
========================================================= */


/* =========================================================
   GOOGLE SEARCH
========================================================= */

function searchNearby() {

    const searchQuery =
        document.getElementById(
            "search-query"
        );

    if (!searchQuery) {
        return;
    }

    const query =
        searchQuery.value.trim();

    if (!query) {
        return;
    }

    window.open(
        `https://www.google.com/maps/search/${encodeURIComponent(query)}`,
        "_blank"
    );
}


/* =========================================================
   SET GOOGLE SEARCH VALUE
========================================================= */

function setSearch(value) {

    const searchInput =
        document.getElementById(
            "search-input"
        );

    if (!searchInput) {
        return;
    }

    searchInput.value =
        value;
}


/* =========================================================
   SET LOCAL SEARCH VALUE
========================================================= */

function setSearchLocal(value) {

    const searchInput =
        document.getElementById(
            "search-input-local"
        );

    if (!searchInput) {
        return;
    }

    searchInput.value =
        value;
}


/* =========================================================
   SEARCH FORM LOADING STATE
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        /*
         * Main Google search form
         */

        const googleSearchForm =
            document.getElementById(
                "google-search-form"
            );

        const searchButton =
            document.getElementById(
                "search-btn"
            );

        if (
            googleSearchForm
            && searchButton
        ) {

            googleSearchForm.addEventListener(
                "submit",
                function () {

                    /*
                     * Do not change selectedLatitude or
                     * selectedLongitude here.
                     *
                     * Location is controlled by the
                     * location system in frontend.html.
                     */

                    searchButton.classList.add(
                        "searching"
                    );

                }
            );

        }


        /*
         * Legacy search-box support
         *
         * Kept safe in case another Wallawalla page
         * still uses .search-box.
         */

        const searchBox =
            document.querySelector(
                ".search-box"
            );

        if (searchBox) {

            searchBox.addEventListener(
                "submit",
                function () {

                    const button =
                        document.getElementById(
                            "search-btn"
                        );

                    if (button) {

                        button.classList.add(
                            "searching"
                        );

                    }

                }
            );

        }


        /*
         * Legacy bottom search card support.
         */

        const searchCard =
            document.querySelector(
                ".search-card"
            );

        if (searchCard) {

            searchCard.addEventListener(
                "submit",
                function () {

                    const button =
                        document.getElementById(
                            "search-btn-bottom"
                        );

                    if (button) {

                        button.classList.add(
                            "searching"
                        );

                    }

                }
            );

        }

    }
);


/* =========================================================
   IMPORTANT

   DO NOT request navigator.geolocation here.

   Location is managed entirely by the location system
   inside frontend.html:

       initializeLocationSearch()
       useCurrentLocation()
       reverseGeocodeLocation()
       setSelectedLocation()
       applyTypedLocation()

   This prevents main.js from overwriting a location
   selected by the visitor.
========================================================= */