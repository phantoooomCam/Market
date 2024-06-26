document.addEventListener('DOMContentLoaded', function() {
    var images = document.querySelector('.img');
    for (var i = 0; i < images.length; i++) {
        var img = images[i];
        if (img.naturalWidth > 800) { // Ejemplo de ancho máximo
            img.style.width = '100%'; // Ajusta el ancho al máximo permitido
            img.style.height = 'auto'; // Mantiene la proporción de aspecto
        }
    }
});
