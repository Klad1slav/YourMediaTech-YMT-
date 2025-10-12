const djangoValue = document.title;

// Only target buttons inside #header_buttons
const headerButtons = document.querySelectorAll('#header_buttons button');
headerButtons.forEach(btn => {
    // Remove all active classes
    btn.classList.remove('active');
    // Add 'active' class if button text matches djangoValue
    if (btn.textContent.trim().toLowerCase() === djangoValue.trim().toLowerCase()) {
        btn.classList.add('active');
    }
});

function toggleLight() {
    document.body.classList.toggle('light-mode');
}

//Show suggestions

const searchInput = document.querySelector('.input-group input.form-control');
const suggestionsList = document.getElementById('suggestions');
const suggestionForm = document.getElementById('suggestion-form');
const suggestionInput = document.getElementById('suggestion-input');

searchInput.addEventListener('input', function() {
    const query = this.value.trim().toLowerCase();
    suggestionsList.innerHTML = '';
    if (query.length === 0) {
        suggestionsList.style.display = 'none';
        return;
    }
    const matches = movieTitles.filter(title => title.toLowerCase().includes(query)).slice(0, 6);
    matches.forEach(title => {
        const li = document.createElement('li');
        li.className = 'list-group-item';
        li.setAttribute('data-title', title); // Add data-title attribute
        li.textContent = title;
        li.onclick = () => {
            searchInput.value = title;
            suggestionsList.innerHTML = '';
            suggestionsList.style.display = 'none';
        };
        suggestionsList.appendChild(li);
    });
    suggestionsList.style.display = matches.length ? 'block' : 'none';
});

suggestionsList.addEventListener('click', function(e) {
    if (e.target && e.target.matches('li.list-group-item')) {
        suggestionInput.value = e.target.getAttribute('data-title');
        suggestionForm.submit();
    }
});

