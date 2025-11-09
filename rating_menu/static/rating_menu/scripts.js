function showForm() {
  document.getElementById('modal-overlay').style.display = 'flex';
}

document.querySelector('.js-show-form').onclick = showForm;

function hideForm() {
  document.getElementById('modal-overlay').style.display = 'none';
}

document.querySelector('.js-hide-form').onclick = hideForm;

// Star rating logic for 0.5 increments, 1-10 scale
const starContainer = document.getElementById('star-rating');

let rating = 0; // 0 to 10, increments of 1
let hoverRating = 0;

function renderStars() {
  starContainer.innerHTML = '';
  for (let i = 1; i <= 5; i++) {
    let starValue = i * 2;
    let fill = hoverRating ? hoverRating : rating;

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
    star.addEventListener('mousemove', function (e) {
      const rect = star.getBoundingClientRect();
      const x = e.clientX - rect.left;
      hoverRating = x < rect.width / 2 ? starValue - 1 : starValue;
      renderStars();
    });

    star.addEventListener('mouseleave', function () {
      hoverRating = 0;
      renderStars();
    });

    star.addEventListener('click', function (e) {
      const rect = star.getBoundingClientRect();
      const x = e.clientX - rect.left;
      rating = x < rect.width / 2 ? starValue - 1 : starValue;

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

if (starContainer) renderStars();

document.querySelectorAll('.star-display').forEach(container => {
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
      <svg width="40" height="40" viewBox="0 0 50 50" stroke="currentColor">
        <defs>
          <linearGradient id="half-static-${i}">
            <stop offset="50%" stop-color="#FFD700"/>
            <stop offset="50%" stop-color="#ccc"/>
          </linearGradient>
        </defs>
        <polygon
          points="25,1 31,18 49,18 35,29 40,46 25,36 10,46 15,29 1,18 19,18"
          fill="${starClass === 'full' ? '#FFD700' : starClass === 'half' ? 'url(#half-static-'+i+')' : '#ccc'}"
        />
      </svg>
    `;
    container.appendChild(star);
  }
});

// Show suggestions modal
const modalInput = document.querySelector('#modal-form input[name="title"]');
const suggestionsModal = document.getElementById('suggestions_modal');

if (modalInput || suggestionsModal) {
  modalInput.addEventListener('input', function () {
    const query = modalInput.value.trim();
    const maxLength = 30;
    suggestionsModal.innerHTML = '';
    if (query.length === 0) {
      suggestionsModal.style.display = 'none';
      return;
    }
    fetch(`${window.location.pathname}?q=${encodeURIComponent(query)}`)
      .then(response => response.text())
      .then(html => {
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = html;
        const newSuggestions = tempDiv.querySelectorAll('#suggestions_modal li.list-group-item');
        if (newSuggestions.length >= 5) {
          suggestionsModal.innerHTML = '';
        }

        if (newSuggestions.length > 0) {
          newSuggestions.forEach(li => {
            const newLi = document.createElement('li');
            newLi.className = 'list-group-item';
            newLi.textContent = li.textContent < maxLength? li.textContent: li.textContent.slice(0, maxLength);
            newLi.setAttribute('data-title', li.getAttribute('data-title'));
            newLi.onclick = function () {
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
}

let description_data = "";
let curentIndex = 0;

if (suggestionsModal) {
  const maxLength = 50;
  const modalImg = document.querySelector('#modal-form img');
  const modalTitle = document.querySelector('#gallery-title');
  const nextButton = document.querySelector('#next-btn');
  const prevButton = document.querySelector('#prev-btn');
  const indexInput = document.querySelector('#index-input')

  // Show description modal
  suggestionsModal.addEventListener('click', e => {
    if (e.target && e.target.matches('li.list-group-item')) {
      const title = e.target.getAttribute('data-title');
      fetch(`${window.location.pathname}?title=${encodeURIComponent(title)}`)
        .then(response => response.json())
        .then(data => {
          curentIndex = 0;
          description_data = data;

          modalTitle.textContent = data[curentIndex].title.length < maxLength ? data[curentIndex].title: data[curentIndex].title.slice(0,maxLength)+ '...';
          modalImg.src = data[curentIndex].poster_path;
          modalImg.alt = data[curentIndex].title;
          suggestionsModal.style.display = 'none';
          indexInput.value = curentIndex
        });
    }
  });

  nextButton.addEventListener('click', event => {
    if (!(description_data.length <= 1) && curentIndex < description_data.length - 1) {
      curentIndex += 1;
    } else if (curentIndex >= description_data.length - 1) {
      curentIndex = 0;
    }
    modalTitle.textContent = description_data[curentIndex].title;
    modalImg.src = description_data[curentIndex].poster_path;
    modalImg.alt = description_data[curentIndex].title;
    indexInput.value = curentIndex
  });

  prevButton.addEventListener('click', event => {
    if (!(description_data.length <= 1) && curentIndex > 0) {
      curentIndex -= 1;
    } else if (curentIndex <= 0) {
      curentIndex = description_data.length - 1;
    }
    modalTitle.textContent = description_data[curentIndex].title;
    modalImg.src = description_data[curentIndex].poster_path;
    modalImg.alt = description_data[curentIndex].title;
    indexInput.value = curentIndex
    console.log(indexInput)
  });
}