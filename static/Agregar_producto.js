document.addEventListener('DOMContentLoaded', function () {
    var btn1 = document.querySelector(".btn_back");

    btn1.addEventListener("click", function() {
        // Redireccionar a otro archivo HTML
        window.location.href = "/selling";
    });

    document.querySelector(".btn_confirmacion").addEventListener("click", function() {
        var campo1 = document.querySelector(".producto").value;
        var campo2 = document.querySelector(".precio").value;
        var campo3 = document.querySelector(".clasificacion").value;
        var campo4 = document.querySelector(".disponibilidad").value;
        var campo5 = document.querySelector(".entrada").value;
        var texto = "¡Se ha agregado correctamente tu producto!";
        
        if (campo1.trim() !== '' && campo2.trim() !== '' && campo3.trim() !== '' && campo4.trim() !== '' && campo5.trim() !== '') {
            // Obtener la etiqueta <p>
            var mensajeElement = document.querySelector(".msj_confirmacion");
          
            // Establecer el mensaje que deseas mostrar
            var mensaje = texto;
          
            // Actualizar el contenido de la etiqueta <p> con el mensaje
            mensajeElement.textContent = mensaje;
          } else {
            alert("No ha llenado todos los campos");
          }
      });
      
});