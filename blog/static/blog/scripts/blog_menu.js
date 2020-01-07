window.onload = function(){

    function handleMenuToggling() {
        let categories = document.querySelector(".categories");
        let blogButton = document.querySelector(".blog-menu-button");

        const handleClick = () => {
            document.querySelector(".navbar-mobile-blog").classList.toggle('navbar-mobile-open');
            document.querySelector(".blog-menu-mobile").classList.toggle('blog-menu-mobile-open');
            document.querySelector(".overlay").classList.toggle("disable-fields");
            if (blogButton.classList.contains("down-arrow")) {
                blogButton.classList.remove("down-arrow");
                blogButton.classList.add("close-sign");
            } else {
                blogButton.classList.add("down-arrow");
                blogButton.classList.remove("close-sign");
            }
        };

        categories.addEventListener('click', handleClick);
    }
    handleMenuToggling();
};
