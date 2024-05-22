document.addEventListener("DOMContentLoaded", function() {
    
    //Botones de referencia en barra de navegacion
    var btn1 = document.querySelector(".btn_home");
    var btn2 = document.querySelector(".btn_power");
    var btn3 = document.querySelector(".btn_pizza");
    var btn4 = document.querySelector(".btn_otros");
    var btn5 = document.querySelector(".btn_car");

    // Agregar event listener a btn1
    btn1.addEventListener("click", function() {
        // Redireccionar a otro archivo HTML
        window.location.href = "/principal";
    });
    
    // Agregar event listener a btn2
    btn2.addEventListener("click", function() {
        // Redireccionar a otro archivo HTML
        window.location.href = "/material";
    });

    // Agregar event listener a btn2
    btn3.addEventListener("click", function() {
        // Redireccionar a otro archivo HTML
        window.location.href = "/comidas";
    });

    // Agregar event listener a btn2
    btn4.addEventListener("click", function() {
        // Redireccionar a otro archivo HTML
        window.location.href = "/otros";
    });

    btn5.addEventListener("click", function(){
        window.location.href="/shopping";
    })
});
document.addEventListener("DOMContentLoaded", function() {
    var imagenes = document.querySelectorAll('.img_prod');
    var index = 0;

    // Función para mostrar la imagen en el índice actual
    function mostrarImagenActual() {
        // Oculta todas las imágenes
        imagenes.forEach(function(imagen) {
            imagen.style.display = 'none';
        });
        // Muestra la imagen en el índice actual
        imagenes[index].style.display = 'block';
    }

    // Muestra la primera imagen inicialmente
    mostrarImagenActual();

    // Función para mostrar la siguiente imagen
    function mostrarSiguienteImagen() {
        index = (index + 1) % imagenes.length; // Incrementa el índice
        mostrarImagenActual();
    }

    // Función para mostrar la imagen anterior
    function mostrarImagenAnterior() {
        index = (index - 1 + imagenes.length) % imagenes.length; // Decrementa el índice
        mostrarImagenActual();
    }

    // Agrega un evento de clic al botón de siguiente
    document.getElementById('siguiente').addEventListener('click', mostrarSiguienteImagen);

    // Agrega un evento de clic al botón de anterior
    document.getElementById('anterior').addEventListener('click', mostrarImagenAnterior);
});
//Efecto de escritura de texto
document.addEventListener('DOMContentLoaded', function() {
    var segundoTexto = "¡El website compra-venta de Upiita!";
    var primerTexto = "Upii-Market";
    var velocidadEscritura = 70; // Velocidad de escritura en milisegundos
    var contenedorTexto = document.querySelector(".slogan");
    var i = 0;

    function escribirPrimerTexto() {
        var i = 0;
        cursorInterval = setInterval(function() {
            if (i < primerTexto.length) {
                contenedorTexto.textContent += primerTexto.charAt(i);
                i++;
            } else {
                clearInterval(cursorInterval);
                setTimeout(borrarTexto, 1000); // Espera 1 segundo antes de borrar el texto
            }
        }, velocidadEscritura);
        moverCursor();
    }

    function borrarTexto() {
        cursorInterval = setInterval(function() {
            var contenido = contenedorTexto.textContent;
            if (contenido.length > 0) {
                contenedorTexto.textContent = contenido.slice(0, -1);
            } else {
                clearInterval(cursorInterval);
                escribirSegundoTexto(); // Llama a la función para escribir el segundo texto después de borrar el primero
            }
        }, velocidadEscritura / 2); // Reduce la velocidad de borrado
    }

    function escribirSegundoTexto() {
        var i = 0;
        cursorInterval = setInterval(function() {
            if (i < segundoTexto.length) {
                contenedorTexto.textContent += segundoTexto.charAt(i);
                i++;
            } else {
                clearInterval(cursorInterval);
            }
        }, velocidadEscritura);
        moverCursor();
    }

    escribirPrimerTexto();
});
