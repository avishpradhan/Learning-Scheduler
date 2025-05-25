
document.querySelectorAll('.delete-subject').forEach(btn => {
    btn.addEventListener('click', function() {
        const subjectId = this.dataset.id;
        if (confirm('Are you sure you want to permanently delete this subject?')) {
            fetch(`/subjects/${subjectId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrf-token]').content
                }
            })
            .then(response => {
                if (response.ok) {
                    window.location.reload();
                } else {
                    alert('Error deleting subject');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to delete subject');
            });
        }
    });
});

// Edit Subject Redirect
document.querySelectorAll('.edit-subject').forEach(btn => {
    btn.addEventListener('click', function() {
        const subjectId = this.dataset.id;
        window.location.href = `/subjects/${subjectId}/edit`;
    });
});

// Flash Message Auto-Close
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        });
    }, 5000);
});

// Progress Bar Animation
document.querySelectorAll('.progress-bar').forEach(bar => {
    const width = bar.style.width;
    bar.style.width = '0';
    setTimeout(() => bar.style.width = width, 100);
});