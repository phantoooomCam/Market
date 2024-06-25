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
document.addEventListener("DOMContentLoaded", function() {
    var buttons = document.querySelectorAll('.btn');
    setTimeout(function() {
      buttons.forEach(function(button, index) {
        button.classList.add('slide-in');
      });
    }, 500); // Delay de 500 milisegundos (0.5 segundos)
  });
document.addEventListener("DOMContentLoaded", function(){
    var btn2 = document.querySelector(".btn-home");
    var btn4 = document.querySelector(".btn-adding");
    var btn5 = document.querySelector(".btn-deleting");
    var btn6 = document.querySelector(".btn-updating");

    btn2.addEventListener("click", function(){
        window.location.href = "/vendedor"
    })
    btn4.addEventListener("click", function(){
        window.location.href = "/agregarproducto"
    })
    btn5.addEventListener("click", function(){
        window.location.href = "/selling"
    })
    btn6.addEventListener("click", function(){
        window.location.href = "/selling"
    })
});