document.addEventListener("DOMContentLoaded", function() {
    // Obtener referencia a los botones
    var btn1 = document.querySelector(".btn_is");
    var btn2 = document.querySelector(".btn_reg");
    
    // Agregar event listener a btn1
    btn1.addEventListener("click", function() {
        // Redireccionar a otro archivo HTML
        window.location.href = "Iniciar Sesion.html";
    });
    
    // Agregar event listener a btn2
    btn2.addEventListener("click", function() {
        // Redireccionar a otro archivo HTML
        window.location.href = "Registrarse.html";
    });
});
