if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) {
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}

window.previous_height =  window.innerHeight

function stick_footer_to_bottom(){
    footer = $('.socket');
    var space_taken = footer.offset()['top'] + footer.height();

    if(space_taken <= window.innerHeight){
        var filler = window.innerHeight - space_taken;
        var margin = $('.footer').css('margin-top')
        $('.footer').css('margin-top', 'calc({0} + {1}px)'.format(margin, filler));
    }
    else{
        $('.footer').css('margin-top', '0px');
        if(window.innerHeight < window.previous_height){
            space_taken = footer.offset()['top'] + footer.height();
            var filler = window.innerHeight - space_taken;
            if(filler > 0){
                $('.footer').css('margin-top', filler+'px');
            }
        }
    };
    window.previous_height =  window.innerHeight;
};

stick_footer_to_bottom()

$(window).resize(function(){stick_footer_to_bottom()});