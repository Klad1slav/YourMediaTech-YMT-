function showForm() {
    document.getElementById('modal-overlay').style.display = 'flex';
}
function hideForm() {
    document.getElementById('modal-overlay').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.btn.btn-success').onclick = showForm;
});
