(function(_window, _document, script, layer, id){
    _window[layer] = _window[layer] || [];
    _window[layer].push({'gtm.start': new Date().getTime(), event: 'gtm.js'});
    var f = _document.getElementsByTagName(script)[0],
    j = _document.createElement(script), dl = layer != 'dataLayer' ? '&l=' + layer : '';
    j.async = true;
    j.src = 'https://www.googletagmanager.com/gtm.js?id=' + id + dl;
    f.parentNode.insertBefore(j, f);
})
(window, document, 'script', 'dataLayer', window.GOOGLE_TAG_MANAGER_ID);
