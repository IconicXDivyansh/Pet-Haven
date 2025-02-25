function showModal(event, eventId, title, description, date, price, image, location, eligibility, prizes) {
    event.preventDefault();
    event.stopPropagation();

    // Set modal content dynamically
    document.getElementById('modalImage').src = `/static/images/${image}`;
    document.getElementById('modalTitle').textContent = title;
    document.getElementById('modalDate').textContent = `📅 ${date}`;
    document.getElementById('modalLocation').textContent = `${location}`;
    document.getElementById('modalPrice').textContent = `Fees: ₹ ${price}`;
    document.getElementById('modalDesc').textContent = description;
    document.getElementById('modalEligibility').textContent = eligibility;
    document.getElementById('modalPrizes').textContent = prizes;
    document.querySelector('.payment-btn').setAttribute(
        'onclick',
        `window.location.href='/register_event/event_id=${eventId}'`
    );
    
    // Show modal
    document.getElementById('detailsModal').style.display = 'flex';

    console.log("Modal opened for Event ID:", eventId); // Debugging
}





function toggleDropdown() {
    document.querySelector(".profile-dropdown").classList.toggle("active");
}

// Close dropdown when clicking outside
window.onclick = function(event) {
    if (!event.target.closest('.profile-dropdown')) {
        document.querySelector(".profile-dropdown").classList.remove("active");
    }
}








document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        document.querySelectorAll(".flash-message").forEach(function (msg) {
            msg.style.opacity = "0";
            setTimeout(() => msg.remove(), 500);  // Removes after fade out
        });
    }, 3000);  // Message disappears after 3 seconds
});


// Show modal for a specific event
function showModal(eventId) {
    document.getElementById(`modal-${eventId}`).style.display = 'flex';
}

function closeModal(eventId, event = null) {
    const modal = document.getElementById(`modal-${eventId}`);

    // Check if the modal exists
    if (!modal) return;

    // Close modal when clicking on the close button
    if (!event || event.target.classList.contains('modal')) {
        modal.style.display = "none";
    }
}


function redirectToRegister(eventId) {
    window.location.href = `/register/${eventId}`;
}

document.addEventListener("DOMContentLoaded", function () {
    const burger = document.getElementById("burger-menu");
    const sidebar = document.getElementById("sidebar");

    
    if (burger && sidebar) {
        burger.addEventListener("click", function () {
            sidebar.classList.toggle("show");
        });
    } else {
        console.error("Burger menu or sidebar not found!");
    }
});

document.getElementById("my-registrations").addEventListener("click", function() {
    document.getElementById("registered-events-container").style.display = "block";
    document.getElementById("all-events-container").style.display = "none"; // Hide all events if needed
});



