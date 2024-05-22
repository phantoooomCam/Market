document.addEventListener("DOMContentLoaded", function() {
  //Botones de referencia en barra de navegacion
  var btn1 = document.querySelector(".btn_home");
  var btn2 = document.querySelector(".btn_menos");
  var btn3 = document.querySelector(".btn_mas");
  var texto = document.querySelector(".can");
  var cantidad = parseInt(texto.textContent);

  btn1.addEventListener("click", function() {
    // Redireccionar a otro archivo HTML
    window.location.href = "/principal";
  });

  btn2.addEventListener("click", function(){
    if(cantidad>0){
      cantidad--;
      texto.textContent = cantidad;
    }
  });

  btn3.addEventListener("click", function(){
    cantidad++;
    texto.textContent = cantidad;
  });

});