var timer_display = document.getElementById("timer");

var seconds = 5;

timer_display.innerText = seconds;

var timer_interval = window.setInterval(function() {
    if (seconds > 0) {
        seconds -= 1;
        timer_display.innerText = seconds;
    }
    else {
        window.clearInterval(timer_interval);
        window.location.href = "/";
    }
}, 1000);
