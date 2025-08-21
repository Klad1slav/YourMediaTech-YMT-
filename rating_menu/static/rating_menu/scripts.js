function showForm() {
    document.getElementById('modal-overlay').style.display = 'flex';
}
function hideForm() {
    document.getElementById('modal-overlay').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.btn.btn-success').onclick = showForm;
});

// Star rating logic for 0.5 increments, 1-10 scale
document.addEventListener('DOMContentLoaded', function() {
    
    const starContainer = document.getElementById('star-rating');
    if (!starContainer) return;

    let rating = 0; // 0 to 10, increments of 1
    let hoverRating = 0;

    function renderStars() {
        starContainer.innerHTML = '';
        for (let i = 1; i <= 5; i++) {
            // Each star represents 2 points
            let starValue = i * 2;
            let fill = (hoverRating ? hoverRating : rating);

            let starClass = '';
            if (fill >= starValue) {
                starClass = 'full';
            } else if (fill >= starValue - 1) {
                starClass = 'half';
            }

            let star = document.createElement('span');
            star.className = `star ${starClass}`;
            star.dataset.value = starValue;

            // SVG star
            star.innerHTML = `
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                  <defs>
                    <linearGradient id="half-grad-${i}">
                      <stop offset="50%" stop-color="#FFD700"/>
                      <stop offset="50%" stop-color="#ccc"/>
                    </linearGradient>
                  </defs>
                  <polygon 
                    points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"
                    fill="${starClass === 'full' ? '#FFD700' : starClass === 'half' ? 'url(#half-grad-'+i+')' : '#ccc'}"
                  />
                </svg>
            `;
            

            // Mouse events for half-star detection
            star.addEventListener('mousemove', function(e) {
                const rect = star.getBoundingClientRect();
                const x = e.clientX - rect.left;
                if (x < rect.width / 2) {
                    hoverRating = starValue - 1;
                } else {
                    hoverRating = starValue;
                }
                renderStars();
            });
            star.addEventListener('mouseleave', function() {
                hoverRating = 0;
                renderStars();
            });
            star.addEventListener('click', function(e) {
                const rect = star.getBoundingClientRect();
                const x = e.clientX - rect.left;
                if (x < rect.width / 2) {
                    rating = starValue - 1;
                } else {
                    rating = starValue;
                }
                // Store rating in a hidden input for form submission
                let input = document.getElementById('star-rating-input');
                if (!input) {
                    input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = 'star_rating';
                    input.id = 'star-rating-input';
                    starContainer.parentNode.appendChild(input);
                }
                input.value = rating;
                renderStars();
            });

            starContainer.appendChild(star);
        }
    }
    renderStars();
});


document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.star-display').forEach(function (container) {
    const rating = parseFloat(container.dataset.rating);

    for (let i = 1; i <= 5; i++) {
      const starValue = i * 2;
      let starClass = '';
      if (rating >= starValue) {
        starClass = 'full';
      } else if (rating >= starValue - 1) {
        starClass = 'half';
      }

      const star = document.createElement('span');
      star.innerHTML = `
        <svg width="75" height="75" viewBox="0 0 50 50" fill="none" stroke="currentColor">
          <defs>
            <linearGradient id="half-static-${i}">
              <stop offset="50%" stop-color="#FFD700"/>
              <stop offset="50%" stop-color="#ccc"/>
            </linearGradient>
          </defs>
          <polygon
            points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02
                    12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"
            fill="${starClass === 'full' ? '#FFD700' : starClass === 'half' ? 'url(#half-static-'+i+')' : '#ccc'}"
          />
        </svg>
      `;
      container.appendChild(star);
    }
  });
});







// Dropdown menu logic
document.addEventListener('DOMContentLoaded', function() {
    const mainMenu = document.getElementById('main-menu');
    const submenuList = document.getElementById('submenu-list');
    const dropdownMenu = mainMenu.parentElement;

    // Example submenu data
const submenuOptions = {
  genre: [
    'Action',
    'Comedy',
    'Drama',
    'Horror',
    'Sci-Fi',
    'Thriller',
    'Romance',
    'Animation'
  ],

  year: Array.from(
    { length: 2025 - 1930 + 1 },
    (_, i) => String(2025 - i) // keep them as strings
  ),

  country: ['USA', 'UK', 'France', 'Germany', 'Japan', 'India'],
};

console.log(submenuOptions.year);


    mainMenu.addEventListener('click', function(e) {
        if (e.target.matches('[data-submenu]')) {
            e.preventDefault();
            const submenuKey = e.target.getAttribute('data-submenu');
            const options = submenuOptions[submenuKey] || [];
            submenuList.innerHTML = `
                <li>
                  <a href="#" class="dropdown-item text-light" id="back-to-main">&larr; Back</a>
                </li>
                ${options.map(opt => `<li><a class="dropdown-item text-light" id="${opt}" href="#">${opt}</a></li>`).join('')}
            `;
            mainMenu.classList.add('d-none');
            submenuList.classList.remove('d-none');
            // Make submenu scrollable if too long
            submenuList.style.maxHeight = '200px';
            submenuList.style.overflowY = 'auto';
        }
    });

    submenuList.addEventListener('click', function(e) {
        if (e.target.id === 'back-to-main') {
            e.preventDefault();
            submenuList.classList.add('d-none');
            mainMenu.classList.remove('d-none');
        }
        // You can handle submenu option clicks here if needed
    });
});





document.addEventListener('DOMContentLoaded', function() {
    const modalInput = document.querySelector('#modal-form input[name="title"]');
    const suggestionsModal = document.getElementById('suggestions_modal');
    if (!modalInput || !suggestionsModal) return;

    modalInput.addEventListener('input', function() {
        const query = modalInput.value.trim();
        suggestionsModal.innerHTML = '';
        if (query.length === 0) {
            suggestionsModal.style.display = 'none';
            return;
        }
        fetch(`${window.location.pathname}?q=${encodeURIComponent(query)}`)
            .then(response => response.text())
            .then(html => {
                // Create a temporary DOM to extract suggestions from the returned HTML
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = html;
                const newSuggestions = tempDiv.querySelectorAll('#suggestions_modal li.list-group-item');
                if (newSuggestions.length > 0) {
                    newSuggestions.forEach(li => {
                        const newLi = document.createElement('li');
                        newLi.className = 'list-group-item';
                        newLi.textContent = li.textContent;
                        newLi.setAttribute('data-title', li.getAttribute('data-title'));
                        newLi.onclick = function() {
                            modalInput.value = newLi.textContent;
                            suggestionsModal.innerHTML = '';
                            suggestionsModal.style.display = 'none';
                        };
                        suggestionsModal.appendChild(newLi);
                    });
                    suggestionsModal.style.display = 'block';
                } else {
                    suggestionsModal.style.display = 'none';
                }
            })
            .catch(() => {
                suggestionsModal.style.display = 'none';
            });
    });
});

document.addEventListener('DOMContentLoaded', function() {
  const suggestionsModal = document.getElementById('suggestions_modal');
  if (suggestionsModal) {
    suggestionsModal.addEventListener('click', function(e) {
      if (e.target && e.target.matches('li.list-group-item')) {
        const title = e.target.getAttribute('data-title');
        fetch(`${window.location.pathname}?title=${encodeURIComponent(title)}&ajax=1`)
          .then(response => response.json())
          .then(data => {
            // Update modal title
            const modalTitle = document.querySelector('#modal-form h2');
            if (modalTitle) modalTitle.textContent = data.first_title;

            // Update modal image
            const modalImg = document.querySelector('#modal-form img');
            if (modalImg) {
              modalImg.src = `https://image.tmdb.org/t/p/w300${data.image}`;
              modalImg.alt = data.first_title;
            }

            // Optionally hide suggestions
            suggestionsModal.style.display = 'none';
          });
      }
    });
  }
});

