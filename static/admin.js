document.addEventListener('DOMContentLoaded', function(){
    var btn = document.querySelector(".btn_agregar_admin");

    btn.addEventListener("click", function(){
        window.location.href = '/agregar_admin';
    });
});