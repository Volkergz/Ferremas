// Este archivo contiene la lógica para manejar el carrito de compras y la validación de formularios

// Función para agregar un producto al carrito
function cambiarCantidad(n) {
  event.preventDefault();
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

function validar() {
    const cantidadInput = document.getElementById('cantidad');
    const mensajeError = document.getElementById('mensajeError');
    const cantidad = cantidadInput.value.trim();

    // Validar que sea un número entero positivo
    const esValido = /^[1-9][0-9]*$/.test(cantidad);

    if (!esValido) {
        mensajeError.style.display = 'block'; // Mostrar el mensaje de error
        cantidadInput.classList.add('is-invalid'); // Bootstrap puede usar esto
        return false; // Detiene el envío del formulario
    }

    mensajeError.style.display = 'none'; // Ocultar mensaje si todo está bien
    cantidadInput.classList.remove('is-invalid');
    return true; // Permite el envío del formulario
}