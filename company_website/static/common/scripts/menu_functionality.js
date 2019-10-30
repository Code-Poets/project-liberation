function navScroll() {
    var scroll = $(window).scrollTop();
    if (scroll >= 100) {
        $(".cp-navi").addClass("visible");
        $(".cp-navi").removeClass("hidden");
        $(".logo1").addClass("visible");
        $(".logo1").removeClass("hidden");
        $(".logo2").addClass("hidden");
        $(".logo2").removeClass("visible");
        $(".navbar").addClass("nb-visible");
        $(".navbar").removeClass("nb-hidden");

    } else {
        $(".cp-navi").addClass("hidden");
        $(".cp-navi").removeClass("visible");
        $(".logo1").addClass("hidden");
        $(".logo1").removeClass("visible");
        $(".logo2").addClass("visible");
        $(".logo2").removeClass("hidden");
        $(".navbar").removeClass("nb-visible");
        $(".navbar").addClass("nb-hidden");
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
    var toggled_menu_width = 991;
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
