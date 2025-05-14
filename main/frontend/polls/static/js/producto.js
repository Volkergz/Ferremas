function validar() {
  const input = document.getElementById('cantidad');
  const mensajeError = document.getElementById('mensajeError');
  const valor = input.value.trim();

  const soloEnteros = /^[1-9][0-9]*$/;

  if (soloEnteros.test(valor)) {
    mensajeError.style.display = 'none';
    addCarrito(valor); 
  } else {
    mensajeError.style.display = 'block';
  }
}

// Arreglar con BBDD
function addCarrito(cantidad) {
  console.log("Cantidad válida añadida al carrito:", cantidad);
}

function cambiarCantidad(n) {
  const input = document.getElementById('cantidad');
  let valorActual = input.value.trim();

  const soloEnteros = /^[0-9]+$/;

  if (!soloEnteros.test(valorActual)) {
    input.value = 0;
    return;
  }

  let nuevoValor = parseInt(valorActual) + n;
  if (nuevoValor < 0) nuevoValor = 0;

  input.value = nuevoValor;
}