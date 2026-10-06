/**
 * VOZ ESCOLAR - Interactive Core JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
  initModal();
  initSearch();
  initSmoothScroll();
});

// Modal Controller
function initModal() {
  const modal = document.getElementById('codeModal');
  const openBtns = document.querySelectorAll('.open-code-modal');
  const closeBtns = document.querySelectorAll('.close-modal');
  const codeForm = document.getElementById('codeForm');
  const codeInput = document.getElementById('participationCode');
  const codeError = document.getElementById('codeError');

  if (!modal) return;

  openBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      modal.classList.add('active');
      if (codeInput) {
        codeInput.focus();
      }
    });
  });

  closeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      modal.classList.remove('active');
      if (codeError) codeError.textContent = '';
    });
  });

  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.classList.remove('active');
      if (codeError) codeError.textContent = '';
    }
  });

  if (codeForm) {
    codeForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const code = codeInput.value.trim().toUpperCase();

      if (code.length < 5) {
        if (codeError) {
          codeError.textContent = 'Por favor, insira um código válido fornecido pela sua escola.';
          codeError.style.display = 'block';
        }
        return;
      }

      // Store current code in sessionStorage for page transition
      sessionStorage.setItem('voz_escolar_active_code', code);
      sessionStorage.setItem('voz_escolar_school_name', 'Colégio Estadual Modelo');

      // Redirect to evaluation flow
      window.location.href = 'pages/avaliar.html';
    });
  }
}

// Search Filter Simulator
function initSearch() {
  const searchInput = document.getElementById('schoolSearch');
  const cityInput = document.getElementById('citySearch');
  const schoolCards = document.querySelectorAll('.school-card');

  function filterCards() {
    const schoolQuery = (searchInput?.value || '').toLowerCase();
    const cityQuery = (cityInput?.value || '').toLowerCase();

    schoolCards.forEach(card => {
      const name = card.dataset.schoolName?.toLowerCase() || '';
      const city = card.dataset.city?.toLowerCase() || '';

      const matchSchool = name.includes(schoolQuery);
      const matchCity = city.includes(cityQuery);

      if (matchSchool && matchCity) {
        card.style.display = 'flex';
      } else {
        card.style.display = 'none';
      }
    });
  }

  if (searchInput) searchInput.addEventListener('input', filterCards);
  if (cityInput) cityInput.addEventListener('input', filterCards);
}

// Smooth Anchor Scrolling
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      const targetEl = document.querySelector(targetId);
      if (targetEl) {
        e.preventDefault();
        targetEl.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
}
