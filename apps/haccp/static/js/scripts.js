// scripts.js

document.addEventListener('DOMContentLoaded', function() {
    const dayButtons = document.querySelectorAll('.day');

    dayButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.classList.toggle('active');
        });
    });
});

function getSelectedDays() {
    const selectedDays = [];
    document.querySelectorAll('.day.active').forEach(button => {
        selectedDays.push(button.getAttribute('data-day'));
    });
    return selectedDays;
}

// Include this in your save function if needed
function save() {
    const selectedDays = getSelectedDays();
    console.log('Selected days:', selectedDays);

    // Include selectedDays in your AJAX request or form submission
}
