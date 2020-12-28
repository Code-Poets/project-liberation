const colorOfAuthorName = "#03428c"

window.showBio = function(element, authorBio){
    if (authorBio !== "") {
        var currentBioToDisplay = element.children[0];
        currentBioToDisplay.style.display = "block";
    }
}

document.body.addEventListener("click", function(evt) {
    if (evt.target.className === 'close' || evt.target.className === "bio-modal") {
        var bioModals = document.getElementsByClassName('bio-modal');
        for (var elementNumber = 0; elementNumber < bioModals.length; elementNumber++ ) {
            bioModals[elementNumber].style.display = "none";
}
    }
});

document.body.addEventListener("mouseover", function(evt) {
    if (evt.target.className === 'author-name') {
        var targetAuthor = evt.target.children[0];
        var lengthOfAuthorBio = targetAuthor.getElementsByClassName("text")[0].innerText.trim().length;

        if (lengthOfAuthorBio > 0) {
            evt.target.style.cursor = "pointer";
        }
        else {
            evt.target.style.color = colorOfAuthorName
        }
    }
});
