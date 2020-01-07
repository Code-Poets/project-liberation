function navScroll() {
    var scroll = $(window).scrollTop();
    if (scroll >= 100) {
        $(".logo").addClass("scrolled");
        $(".navbar").addClass("nb-visible");
        $(".navbar").removeClass("nb-hidden");
        $(".navbar-collapse").addClass("background-change");

    } else {
        $(".logo").removeClass("scrolled");
        $(".navbar").removeClass("nb-visible");
        $(".navbar").addClass("nb-hidden");
        $(".navbar-collapse").removeClass("background-change");
    }
}

$(document).ready(function () {
    var current_path_name = window.location.pathname;
    if (current_path_name === "/") {
        $(window).scroll(function () {
            navScroll();
        });
    }
});

$(document).ready(function () {
    var current_path_name = window.location.pathname;
    if (current_path_name === "/") {
        navScroll();
    }
});

$(document).ready(function () {
    const hamburger = document.querySelector('.hamburger');
    const navigation = document.querySelector('.navigation');

    const handleClick = () => {
        hamburger.classList.toggle('hamburger-active');
        if (hamburger.classList.contains('hamburger-active')) {
            hamburger.setAttribute('aria-expanded', 'true');
        } else {
            hamburger.setAttribute('aria-expanded', 'false');
        }

        navigation.classList.toggle('navigation-active');
    };

    hamburger.addEventListener('click', handleClick);
});

$(document).ready(function () {

    $("button").click(function (event) {
        if ($(".hamburger").attr("aria-expanded") === "true") {
            $(".overlay").addClass("disable-fields");
        } else {
            $(".overlay").removeClass("disable-fields");
        }
    });

    $("div").click(function (event) {
        if ($(event.target).hasClass('disable-fields')) {
            $(".hamburger").click();
            $(".overlay").removeClass("disable-fields");
        }
    });

    $("a, .mobile.estimate-project span").click(function (event) {
        if ($(event.target).hasClass('mobile-link') || $(event.target).hasClass('estimate-project')) {
            $(".hamburger").click();
            $(".overlay").removeClass("disable-fields");
        }
    });
});

$(document).ready(function () {
    var toggled_menu_width = 1175;
    const hamburger = document.querySelector('.hamburger');

    function checkWidth() {
        var window_size = window.innerWidth;
        var is_aria_expanded = hamburger.getAttribute('aria-expanded');

        if (is_aria_expanded === "true" && toggled_menu_width < window_size) {
            hamburger.click();
        }
    }

    checkWidth();
    $(window).resize(checkWidth);
});

var $root = $('html, body');
$('a.nav-link').click(function () {
    var str = $.attr(this, 'href');
    var scrollTo;
    if (window.location.pathname == "/" ){
        if (str.indexOf("#") == 1) {
            if (window.innerWidth > 1175){
                scrollTo = ($(str.substring(1)).offset().top - 50)
            } else {
                scrollTo = ($(str.substring(1)).offset().top - 94);
            }
            $root.animate({
                scrollTop: scrollTo
            }, 500);
        }
    }
});
