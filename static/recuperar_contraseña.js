document.addEventListener("DOMContentLoaded", function(){
    var btn = document.querySelector(".regresar");

    btn.addEventListener("click", function(){
        window.location.href = "/iniciar_sesion";
    });
});