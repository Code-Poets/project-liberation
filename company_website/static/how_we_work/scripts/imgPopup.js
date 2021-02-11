var modal = document.getElementsByClassName("imgModal")[0];
var leftImg = document.getElementById("image-left-popup");
var rightImg = document.getElementById("image-right-popup");
var imgInPopup = document.getElementById("popup-img");


$(leftImg).add(rightImg).on("click", function (){
    modal.style.display = "block";
    imgInPopup.src = this.src;
    imgInPopup.alt = this.alt;
});

var span = document.getElementsByClassName("close")[0];
span.onclick = function () {
    modal.style.display = "none";
}
