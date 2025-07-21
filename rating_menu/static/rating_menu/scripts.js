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
        genre: ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi', 'Thriller', 'Romance', 'Animation'],
        year: ['2025', '2024', '2023', '2022', '2021', '2020'],
        country: ['USA', 'UK', 'France', 'Germany', 'Japan', 'India'],
        producer: ['Producer 1', 'Producer 2', 'Producer 3'],
        director: ['Director 1', 'Director 2', 'Director 3'],
        actor: ['Actor 1', 'Actor 2', 'Actor 3', 'Actor 4']
    };

    mainMenu.addEventListener('click', function(e) {
        if (e.target.matches('[data-submenu]')) {
            e.preventDefault();
            const submenuKey = e.target.getAttribute('data-submenu');
            const options = submenuOptions[submenuKey] || [];
            submenuList.innerHTML = `
                <li>
                  <a href="#" class="dropdown-item text-light" id="back-to-main">&larr; Back</a>
                </li>
                ${options.map(opt => `<li><a class="dropdown-item text-light" href="#">${opt}</a></li>`).join('')}
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
