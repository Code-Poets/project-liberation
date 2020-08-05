function gtagReportConversion(url) {
    var callback = function () {
        if (typeof (url) != 'undefined') {
            window.location = url;
        }
    };
    gtag(
        'event',
        'conversion',
        {
            'send_to': window.GOOGLE_ADS_CONVERSION_TARGET_ADDRESS,
            'event_callback': callback
        }
    );
    return false;
}
