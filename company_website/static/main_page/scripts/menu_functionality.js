$(window).scroll(function () {

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
});

$(document).ready(function () {
    $("button").click(function (event) {
        var event_target = $(event.target).attr('id');
        if (event_target === "menuButton") {
            if ($('.navbar-toggler').attr('aria-expanded') === "false") {
                $(".content-page").addClass("disable-fields");
            } else {
                $(".content-page").removeClass("disable-fields");
            }
        }
    });

    $("div").click(function (event) {
        if ($(event.target).hasClass('disable-fields')) {
            $(".navbar-toggler").click();
            $(".content-page").removeClass("disable-fields");
        }
    });

    $("a").click(function (event) {
        var is_estimate_project = $(event.target).hasClass('estimate-project');
        if ($(event.target).hasClass('nav-link') || is_estimate_project) {
            $(".navbar-toggler").click();
            $(".content-page").removeClass("disable-fields");
        }
    });
});

$(document).ready(function () {
    var $window = $(window);
    var toggled_menu_width = 991;

    function checkWidth() {
        var window_size = $window.width();
        if ($('.navbar-toggler').attr('aria-expanded') === "true" && toggled_menu_width < window_size) {
            $(".content-page").removeClass("disable-fields");
            $(".navbar-toggler").click();
        }
    }

    checkWidth();
    $(window).resize(checkWidth);
});
