document.addEventListener('DOMContentLoaded', function () {
  const toggles = document.querySelectorAll('.toggle-btn');

  toggles.forEach(btn => {
    btn.addEventListener('click', () => {
      const content = btn.nextElementSibling;
      content.classList.toggle('show');
      btn.classList.toggle('active');
    });
  });
});

const checkboxes = document.querySelectorAll('input[name="rango_precio"]');
checkboxes.forEach(chk => {
  chk.addEventListener('change', () => {
    const seleccionados = Array.from(checkboxes)
      .filter(cb => cb.checked)
      .map(cb => cb.value);
    console.log("Rangos seleccionados:", seleccionados);
  });
});

