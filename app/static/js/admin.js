// Admin Panel JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Admin panel loaded');
    
    // Simple cache control for development
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.getRegistrations().then(function(registrations) {
            for(let registration of registrations) {
                registration.unregister();
            }
        });
    }
    
    // Disable caching for development
    if (window.caches) {
        caches.keys().then(function(names) {
            for (let name of names) {
                caches.delete(name);
            }
        });
    }
});

// Utility functions
function showSuccess(message) {
    alert('Success: ' + message);
}

function showError(message) {
    alert('Error: ' + message);
}

function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}