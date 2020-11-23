let talkWithAdrianButtonId = "#talk-with-adrian"

$('a').each(function() {
    if(!$(this).is(talkWithAdrianButtonId)) {
        let localLinkExpression = new RegExp('/' + window.location.host + '/');

        if (!localLinkExpression.test(this.href)) {
            $(this).click(function (event) {
                event.preventDefault();
                event.stopPropagation();
                window.open(this.href, '_blank');
            });
        }
    }
});
