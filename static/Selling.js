document.addEventListener("DOMContentLoaded", function() {
    var btn1 = document.querySelector(".btn_home");
    var btn2 = document.querySelector(".btn_agregar");

    btn1.addEventListener("click", function() {
        // Redireccionar a otro archivo HTML
        window.location.href = "/principal";
    });
    btn2.addEventListener("click", function(){
        window.location.href = "/agregarproducto";
    });
});