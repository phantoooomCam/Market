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
    var btn1 = document.querySelector(".btn_upii-market");
    var btn2 = document.querySelector(".btn-home");
    //var btn3 = document.querySelector('.btn-account');
    var btn4 = document.querySelector(".btn_adding");
    var btn4 = document.querySelector(".btn_deleting");
    var btn4 = document.querySelector(".btn_updating");

    btn1.addEventListener("click", function(){
        window.location.href = "/principal"
    })
    btn2.addEventListener("click", function(){
        window.location.href = "/vendedor"
    })
    /*btn3.addEventListener("click", function(){
        window.location.href = "/vendedor_principal"
    })*/
    btn4.addEventListener("click", function(){
        window.location.href = "/vendedor_principal"
    })
    btn5.addEventListener("click", function(){
        window.location.href = "/vendedor_principal"
    })
});