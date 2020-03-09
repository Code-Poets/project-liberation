window.initMap = function initMap() {
    var position = {lat: 51.1013288, lng: 17.027990499999987};
    var styles = [
        {
            featureType: "all",
            stylers: [{ hue: "#7bb0e7" }, { saturation: 50}]
        },
        {
            featureType: "poi",
            stylers: [{visibility: "off"}]
        }
    ];
    var map_options = {
        zoom: 15,
        center: position,
        backgroundColor: "transparent",
        gestureHandling: "cooperative",
        mapTypeControl: false,
        mobile_drag_control: 1,
        pan_control: false,
        scrollwheel: false,
        streetview_control: 1,
        styles: styles
    };
    var map = new google.maps.Map(document.getElementsByClassName('map')[0], map_options);
    map.setMapTypeId(google.maps.MapTypeId.ROADMAP);
    var marker_options = {
        position: position,
        map: map,
        title: "Józefa Piłsudskiego 49-57",
        optimized: false
    };
    var marker = new google.maps.Marker(marker_options);
    var info_window = new google.maps.InfoWindow({content: "Code Poets sp. z o.o."});
    google.maps.event.addListener(marker, 'click', function() {
        info_window.open(map,marker);
    });
    info_window.open(map, marker);
};

if(screen.width >= 720) {
    document.write(
        '<script src="https://maps.googleapis.com/maps/api/js?key=' + google_api_key +
        '&callback=initMap" async defer></script>'
    );
}
