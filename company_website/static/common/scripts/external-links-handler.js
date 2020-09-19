$('a').each(function() {
   let local_link_expression = new RegExp('/' + window.location.host + '/');
   if(!local_link_expression.test(this.href)) {
       $(this).click(function(event) {
           event.preventDefault();
           event.stopPropagation();
           window.open(this.href, '_blank');
       });
   }
});
