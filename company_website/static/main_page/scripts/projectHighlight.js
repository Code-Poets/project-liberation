projectHighlightOverlay = document.getElementsByClassName("project-highlight")[0];
projectBoxes = $(".project-box");
screenMdSize = 991;


projectBoxes.each(function() {
    $(this).click(function() {
        if(isWindowLarge())
            disableScroll();
        $(projectHighlightOverlay).toggle();
        $(projectHighlightOverlay).toggleClass("non-clickable");
        projectBoxes.toggleClass("non-clickable");
        transformBackground();

        let absoluteGridPosition = this.getBoundingClientRect();
        projectHighlightOverlay.appendChild(this);
        changeElementSize(this, absoluteGridPosition.width, absoluteGridPosition.height);
        let absoluteHighlightPosition = this.getBoundingClientRect();
        animateProjectHighlight(this, absoluteGridPosition, absoluteHighlightPosition);
    });
});

$(projectHighlightOverlay).click(function() {
    let originalContainer = findEmptyProjectHolder();
    let absoluteGridPosition = originalContainer.getBoundingClientRect();
    let highlightedProject = projectHighlightOverlay.getElementsByClassName("project-box")[0];

    $(projectHighlightOverlay).toggleClass("non-clickable");
    matchProjectBoxSizeToOtherProjectBoxes(highlightedProject);

    let transitionEndListener = function() {
        let absoluteHighlightPosition = highlightedProject.getBoundingClientRect();
        transformBackground();
        animateProjectReturn(highlightedProject, absoluteGridPosition, absoluteHighlightPosition, originalContainer);
        highlightedProject.removeEventListener('transitionend', transitionEndListener);
    }

    highlightedProject.addEventListener('transitionend', transitionEndListener);
    $(highlightedProject).toggleClass("expanded-project-box");
});

function animateProjectHighlight(projectElement, absoluteGridPosition, absoluteHighlightPosition) {
    let fromParams = {
        x: (isWindowLarge() ? absoluteGridPosition.left - absoluteHighlightPosition.left : 0),
        y: absoluteGridPosition.top - absoluteHighlightPosition.top,
    };
    let toParams = {
        x: 0,
        y: 0,
        duration: 0.5,
        ease: "power3.out",
        onCompleteParams: [projectElement],
        onComplete: expandProjectBoxOnHighlight,
    };
    gsap.fromTo(projectElement, fromParams, toParams);
}

function animateProjectReturn(projectElement, absoluteGridPosition, absoluteHighlightPosition, originalContainer) {
    let fromParams = {
        x: 0,
        y: 0,
    };
    let toParams = {
        x: (isWindowLarge() ? absoluteGridPosition.left - absoluteHighlightPosition.left : 0),
        y: absoluteGridPosition.top - absoluteHighlightPosition.top,
        duration: 0.5,
        ease: "expo.out",
        onCompleteParams: [projectElement, originalContainer],
        onComplete: moveProjectBoxBackToOrigin,
    };
    gsap.fromTo(projectElement, fromParams, toParams);
}

function expandProjectBoxOnHighlight(projectElement) {
    projectElement.removeAttribute("style");
    $(projectElement).toggleClass("expanded-project-box");
    $(projectHighlightOverlay).toggleClass("non-clickable");
}

function moveProjectBoxBackToOrigin(projectElement, originalContainer) {
    $(projectHighlightOverlay).toggle();
    $(projectHighlightOverlay).toggleClass("non-clickable");
    projectBoxes.toggleClass("non-clickable");
    projectElement.removeAttribute("style");
    originalContainer.appendChild(projectElement);
    enableScroll();
}

function transformBackground() {
    $(".project-highlight-background").toggleClass("darkened");
}

function matchProjectBoxSizeToOtherProjectBoxes(projectElement) {
    let originalProjectBoxDimensions = findEmptyProjectHolder().getBoundingClientRect();
    changeElementSize(projectElement, originalProjectBoxDimensions.width, originalProjectBoxDimensions.height);
}

function changeElementSize(element, width, height) {
    element.style.width = width + "px";
    element.style.height = height + "px";
}

function isWindowLarge() {
    return window.innerWidth > screenMdSize;
}

function findEmptyProjectHolder() {
    let projectHolders = document.getElementsByClassName("project-holder");
    let projectHolder;
    for (projectHolder of projectHolders)
        if (projectHolder.children.length === 0)
            return projectHolder;
    return null;
}
