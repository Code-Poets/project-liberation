var disqus_config = function () {
    this.page.url = document.getElementById("blog_page_url").innerHTML;
    };
    (function() {
        var d = document, s = d.createElement('script');
        s.src = 'https://code-poets.disqus.com/embed.js';
        s.setAttribute('data-timestamp', +new Date());
        (d.head || d.body).appendChild(s);
    })();
