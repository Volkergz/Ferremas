function scrollProductos(direction) {
    const container = document.getElementById('destacados');
    const cardWidth = document.querySelector('.producto-card').offsetWidth + 24; // 24px por el gap
    const cardsToMove = 5; // Número de tarjetas que se deben mover a la vez
    const scrollMax = container.scrollWidth - container.clientWidth;
  
    if (direction === 1) {
      if (container.scrollLeft >= scrollMax - 10) {
        // Si está casi al final, vuelve al inicio
        container.scrollLeft = 0;
      } else {
        container.scrollLeft += cardWidth * cardsToMove; // Mueve 5 tarjetas
;
      }
    } else {
      if (container.scrollLeft <= 0) {
        // Si está al inicio, ve al final
        container.scrollLeft = scrollMax;
      } else {
        container.scrollLeft -= cardWidth * cardsToMove; // Mueve 5 tarjetas hacia la izquierda
    }
    }
  }
  