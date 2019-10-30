$(".inner-info").click(function (event) {
    let mobile_window = 991;
    window.innerWidth
    if (window.innerWidth <= mobile_window)
        var clicked_hotspot = event.target.classList[1];
    $(document.body).animate({
        'scrollTop': $('img.hotspot-mobile.' + clicked_hotspot).offset().top - 125
    }, 2000);
});
