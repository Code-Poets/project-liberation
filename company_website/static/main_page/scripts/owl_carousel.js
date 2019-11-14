var owl_carousel = $('.owl-carousel')

owl_carousel.owlCarousel({
    items: 1,
    lazyLoad: true,
    loop: true,
    autoplay: true,
    autoplayTimeout: 3000,
    autoplayHoverPause: true,
    margin: 20,
    nav: false,
    dotsContainer: ".custom-dots-bar",
    smartSpeed: 1000,
})

function flashOnClick(element) {
    $(element).removeClass("flash");
    setTimeout(function() {
        $(element).addClass("flash")
    }, 10);
}

$(".nav-button-next").click(function() {
    owl_carousel.trigger("next.owl.carousel");
    flashOnClick(this);
});

$(".nav-button-prev").click(function() {
    owl_carousel.trigger("prev.owl.carousel");
    flashOnClick(this);
});

$(".custom-dots-bar").on("click", "li", function(e) {
    owl_carousel.trigger("to.owl.carousel", [$(this).index(), 300]);
});