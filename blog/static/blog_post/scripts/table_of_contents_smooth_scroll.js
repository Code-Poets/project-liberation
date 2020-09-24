$('.table-of-contents a').click(function () {
    let targetID = $.attr(this, 'href');
    let scrollTo = $(targetID).offset().top
    let pxOffset = window.getComputedStyle($(targetID)[0], ':before')["height"]
    $root.animate({scrollTop: scrollTo - parseInt(pxOffset, 10)}, 500);
});
