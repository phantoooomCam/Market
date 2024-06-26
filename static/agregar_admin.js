document.addEventListener('DOMContentLoaded', function(){
    var btn = document.querySelector(".btn_back");

    btn.addEventListener("click", function(){
        window.location.href = "/admin";
    })
})