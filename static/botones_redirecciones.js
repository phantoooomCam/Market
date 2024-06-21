document.addEventListener("DOMContentLoaded", function() {
    //Botones de referencia en barra de navegacion
    var btn1 = document.querySelector(".btn_home");
    var btn2 = document.querySelector(".btn_sell");
    var btn7 = document.querySelector(".btn_car");

    // Obtener referencia a los botones de submenus
    var btn3 = document.querySelector(".btn__material");
    var btn4 = document.querySelector(".btn__comida");
    var btn5 = document.querySelector(".btn__snack");
    var btn6 = document.querySelector(".btn__otros");

    // Agregar event listener a btn1
    btn1.addEventListener("click", function() {
        // Redireccionar a otro archivo HTML
        window.location.href = "/principal";
    });
    
    // Agregar event listener a btn2
    btn2.addEventListener("click", function() {
        // Redireccionar a otro archivo HTML
        window.location.href = "/iniciarvendedor";
    });

    // Agregar event listener a btn2
    btn3.addEventListener("click", function() {
        // Redireccionar a otro archivo HTML
        window.location.href = "/material";
    });

    // Agregar event listener a btn2
    btn4.addEventListener("click", function() {
        // Redireccionar a otro archivo HTML
        window.location.href = "/comidas";
    });

    btn5.addEventListener("click", function() {
        // Redireccionar a otro archivo HTML
        window.location.href = "/snacks";
    });

    btn6.addEventListener("click", function() {
        // Redireccionar a otro archivo HTML
        window.location.href = "/otros";
    });
    
    btn7.addEventListener("click", function(){
        window.location.href= "/shopping";
    })

});
document.addEventListener('DOMContentLoaded', function() {
    var Texto = "¡ El website compra-venta de Upiita !";
    var velocidadEscritura = 90; // Velocidad de escritura en milisegundos
    var contenedorTexto = document.querySelector(".slogan");
    var i = 0;

    function escribirPrimerTexto() {
        var i = 0;
        cursorInterval = setInterval(function() {
            if (i < Texto.length) {
                contenedorTexto.textContent += Texto.charAt(i);
                i++;
            } else {
                clearInterval(cursorInterval);
            }
        }, velocidadEscritura);
        moverCursor();
    }

    escribirPrimerTexto();
});