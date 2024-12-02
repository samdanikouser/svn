    // Toggle function for accordion-style activity content
    function toggleAccordion(locationId) {
        var content = document.querySelector('#' + locationId + ' .activity-content');
        var button = document.querySelector('#' + locationId + ' .accordion-btn');

        content.classList.toggle('open');
        button.classList.toggle('active');
    }

    // Toggle the visibility of location-specific content
    function toggleActivity(locationId) {
        // Close all activities
        var allActivities = document.querySelectorAll('.activity-section .activity-content');
        allActivities.forEach(function(activity) {
            activity.classList.remove('open');
        });
        var allButtons = document.querySelectorAll('.accordion-btn');
        allButtons.forEach(function(button) {
            button.classList.remove('active');
        });

        // Show the selected activity
        var activity = document.querySelector('#' + locationId + ' .activity-content');
        var button = document.querySelector('#' + locationId + ' .accordion-btn');

        activity.classList.toggle('open');
        button.classList.toggle('active');
    }

    // Function to handle Save button click
    async function checkAndSave(itemId, minInputId, maxInputId, timeValue) {
    const minValue = parseFloat(document.getElementById(minInputId).value);
    const maxValue = parseFloat(document.getElementById(maxInputId).value);

    // Send item ID and entered min/max values to the backend to check the range
    const response = await fetch('user/check-range/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // CSRF token for Django
        },
        body: JSON.stringify({
            item_id: itemId,
            entered_min: minValue,
            entered_max: maxValue
        })
    });

    const data = await response.json();

    if (data.out_of_range) {
    // Display corrective actions in the modal
    const correctiveMessageDiv = document.getElementById('correctiveMessage');
    correctiveMessageDiv.innerHTML = ''; // Clear previous messages

    const correctiveActionsList = document.getElementById('correctiveActionsList');
    correctiveActionsList.innerHTML = ''; // Clear previous actions

    // Create checkboxes for each corrective action
    data.corrective_actions.forEach(action => {
        const actionItem = document.createElement('div');
        actionItem.innerHTML = `
            <input type="checkbox" id="action_${action.id}" value="${action.id}" />
            <label for="action_${action.id}">${action.name}</label>
        `;
        correctiveActionsList.appendChild(actionItem);
    });

    // Show modal
    document.getElementById('correctiveModal').style.display = 'block';

    // Store data for later use
    window.dataToSave = { itemId, minValue, maxValue, timeValue, correctiveActions: data.corrective_actions };
} else {
    // Save data directly if values are in range
    saveData(itemId, minValue, maxValue, timeValue, null);
}
    
}

// Function to save data after corrective action is confirmed
async function confirmSave() {
    // Collect selected checkboxes
    const selectedActions = [];
    window.dataToSave.correctiveActions.forEach(action => {
        const checkbox = document.getElementById(`action_${action.id}`);
        if (checkbox.checked) {
            selectedActions.push(action.id); // Add selected action ID
        }
    });

    // Get the comment from the single text box
    const actionComment = document.getElementById('actionComment').value;

    // Call saveData function with the selected actions and the comment
    const { itemId, minValue, maxValue, timeValue } = window.dataToSave;
    saveData(itemId, minValue, maxValue, timeValue, { selectedActions, comment: actionComment });
}

// Function to send data to backend to save it
async function saveData(itemId, minValue, maxValue, timeValue, correctiveData) {
    if(correctiveData){
        data_to_send =  JSON.stringify({
            item_id: itemId,
            entered_min: minValue,
            entered_max: maxValue,
            corrective_actions: correctiveData.selectedActions,
            comment: correctiveData.comment,
            time: timeValue

        })
    }else{
        data_to_send =  data_to_send =  JSON.stringify({
            item_id: itemId,
            entered_min: minValue,
            entered_max: maxValue,
            time: timeValue
        })
    }
    const response = await fetch('user/save-data/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // CSRF token for Django
        },
        body:data_to_send
    });

    const result = await response.json();
    if (result.success) {
        alert('Data saved successfully!');
        closeModal();
        location.reload();
    } else {
        alert('Error saving data:', result.error);
    }
}

// Function to close the modal
function closeModal() {
    document.getElementById('correctiveModal').style.display = 'none';
}

// Helper function to get CSRF token (for Django)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



document.addEventListener("DOMContentLoaded", async function() {
    // Get the current time (in hour:minute format)
    const currentTime = new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});

    // Send a request to the backend to check if data exists for today's time
    const response = await fetch('user/check-daily-update/', {
        method: 'GET',  // Use 'GET' method as no data is being sent in the body
        headers: {
            'Content-Type': 'application/json'
        }
    });

    const data = await response.json();
    if(data.data_exists){
    
        for (let i = 0; i < data.data_exists.length; i++) {
            const element = document.getElementById(data.data_exists[i].id);
            if (element) {
            element.style.display = "none"; // Hide the element
        } else {
            console.log(`Element with ID ${data.data_exists[i]} not found.`);
        }
        }
    }
});


