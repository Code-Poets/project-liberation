nameField = document.getElementById("id_name");
emailField = document.getElementById("id_email");
descriptionField = document.getElementById("id_idea_description");
policyCheckboxField = document.getElementById("id_privacy_policy_accepted");

inputFieldName = document.getElementsByClassName("input-field")[0];
inputFieldEmail = document.getElementsByClassName("input-field")[1];
descriptionBox = document.getElementsByClassName("describe-idea-box-input")[0];

const borderErrorColor = "#ff0000"
const borderCorrectColor = "#d7d7d7"
const borderErrorShadow = "0px 0px 16px #ff0000"


$(nameField).on("invalid", function() {
    $(inputFieldName).css({"border-color": borderErrorColor, "box-shadow": borderErrorShadow});
});

$(emailField).on("invalid", function() {
    $(inputFieldEmail).css({"border-color": borderErrorColor, "box-shadow": borderErrorShadow});
});

$(descriptionField).on("invalid", function() {
    $(descriptionBox).css({"border-color": borderErrorColor, "box-shadow": borderErrorShadow});
});

$(policyCheckboxField).on("invalid", function() {
    $("input[type=checkbox]").css({"border-color": borderErrorColor, "box-shadow": borderErrorShadow});
});

$(nameField).on("valid", function() {
    $(inputFieldName).css({"border-color": borderCorrectColor, "box-shadow": "none"});
});

$(emailField).on("valid", function() {
     $(inputFieldEmail).css({"border-color": borderCorrectColor, "box-shadow": "none"});
});

$(descriptionField).on("valid", function() {
    $(descriptionBox).css({"border-color": borderCorrectColor, "box-shadow": "none"});
});

$(nameField).on("change", function() {
    $(inputFieldName).css({"border-color": borderCorrectColor, "box-shadow": "none"});
});

$(emailField).on("change", function() {
    $(inputFieldEmail).css({"border-color": borderCorrectColor, "box-shadow": "none"});
});

$(descriptionField).on("change", function() {
    $(descriptionBox).css({"border-color": borderCorrectColor, "box-shadow": "none"});
});

$(policyCheckboxField).on("change", function() {
    $("input[type=checkbox]").css({"border-color": borderCorrectColor, "box-shadow": "none"})
});

document.addEventListener("invalid", (function () {
    return function (event) {
        event.preventDefault();
    };
})(), true);

$(function () {
    if (typeof document.createElement("input").checkValidity === "function") {
        $("#estimate-project-form").submit(function (event) {
            if (!this.checkValidity()) {
                event.preventDefault();
            }
        });
    }
});
