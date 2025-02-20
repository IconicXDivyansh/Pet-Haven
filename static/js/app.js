import { competitions } from './seedData.js';

function initApp() {
	renderCompetitions();
	addNavListeners();
}

function renderCompetitions() {
	const grid = document.getElementById('competitionsGrid');
	grid.innerHTML = '';

	competitions.forEach((comp) => {
		const card = document.createElement('div');
		card.className = 'card';
		card.innerHTML = `
          <img src="${comp.image}" class="card-img" alt="${comp.title}">
          <div class="card-content">
              <h2>${comp.title}</h2>
              <br>
              <p>${new Date(comp.date).toLocaleDateString()}</p>
              
              <p>${comp.location} </p>
              <br>
              <p class="price"><span style='color:black'>Fees: </span>₹${
								comp.price
							}</p>
              <button class='register-btn'>Register Now</button>
          </div>
      `;
		// Add event listener to the Register button
		const registerButton = card.querySelector('.register-btn');
		registerButton.addEventListener('click', () => showModal(comp));

		card.addEventListener('click', () => showModal(comp));
		grid.appendChild(card);
	});
}

function showModal(comp) {
	const modal = document.getElementById('detailsModal');
	document.getElementById('modalImage').src = comp.image;
	document.getElementById('modalTitle').textContent = comp.title;
	document.getElementById('modalDate').textContent = new Date(
		comp.date
	).toLocaleDateString();
	document.getElementById('modalLocation').textContent = comp.location;
	document.getElementById('modalPrice').textContent = `₹${comp.price}`;
	document.getElementById('modalDesc').textContent = comp.description;
	document.getElementById('modalEligibility').textContent = comp.eligibility;
	document.getElementById('modalPrizes').textContent = comp.prizes;
	modal.style.display = 'flex';
}

function closeModal() {
	document.getElementById('detailsModal').style.display = 'none';
}

function redirectToPayment() {
	// Add payment redirection logic
	window.location.href = 'payment.html';
}

function addNavListeners() {
	document.querySelectorAll('.nav-item').forEach((item) => {
		item.addEventListener('click', function () {
			document
				.querySelectorAll('.nav-item')
				.forEach((i) => i.classList.remove('active'));
			this.classList.add('active');
		});
	});
}

// Initialize app
initApp();

// Close modal when clicking outside
window.onclick = function (event) {
	const modal = document.getElementById('detailsModal');
	if (event.target === modal) {
		closeModal();
	}
};

function toggleSidebar() {
	const sidebar = document.getElementById('sidebar');
	const navbar = document.getElementById('navbar');
	const mainContent = document.getElementById('mainContent');

	if (sidebar.classList.contains('show')) {
		sidebar.classList.remove('show');
		navbar.style.left = '0';
		navbar.style.width = '100%';
		mainContent.style.marginLeft = '0';
	} else {
		sidebar.classList.add('show');
		navbar.style.left = '250px';
		navbar.style.width = 'calc(100% - 250px)';
		mainContent.style.marginLeft = '250px';
	}
}
