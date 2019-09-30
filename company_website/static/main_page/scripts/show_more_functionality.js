$(document).ready(function () {
    const more_projects_button = document.querySelector('.more-projects');
    const more_projects_row = document.querySelector('.mobile-hidden-projects');

    const handleClick = () => {
        more_projects_row.classList.toggle('toggle-projects');
        if (more_projects_button.getAttribute("value") === "Show more"){
            more_projects_button.setAttribute("value", "Show less");
        } else {
            more_projects_button.setAttribute("value", "Show more");
        }

    };

    more_projects_button.addEventListener('click', handleClick);

    $(".more-projects").click(function () {
        if (more_projects_row.classList.contains('toggle-projects')) {
            scrollTo = ".more-projects";
        } else {
            scrollTo = ".project-golem-box";
        }

        $('html,body').animate({
                scrollTop: $(scrollTo).offset().top
            },
            2000);
    });
});
