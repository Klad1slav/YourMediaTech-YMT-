document.addEventListener('DOMContentLoaded', function() {
    document.body.addEventListener('click', function(e) {
        if (e.target.classList.contains('btn-primary')) {
            // Remove active from all .btn-primary buttons
            document.querySelectorAll('.btn-primary').forEach(btn => btn.classList.remove('active'));
            // Add active to the clicked button
            e.target.classList.add('active');
        }
    });
});

function toggleLight() {
    document.body.classList.toggle('light-mode');
}