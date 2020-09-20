$('.table-of-contents a').click(function () {
    let targetID = $.attr(this, 'href');
    let scrollTo = $(targetID).offset().top
    $root.animate({scrollTop: scrollTo}, 500);
});
