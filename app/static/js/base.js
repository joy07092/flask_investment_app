function loadContent(endpoint) {  //only with button without changing link
    fetch(endpoint, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (response.status === 401) {
            // Session expired or unauthorized
            window.location.href = "/login";
        }
        if (!response.ok) throw new Error('Failed to load content');
        return response.text();
    })
    .then(data => {
        document.getElementById('content-area').innerHTML = data;
    })
    .catch(error => {
        console.error('Error loading content:', error);
        document.getElementById('content-area').innerHTML = `
            <div class="alert alert-danger mt-3" role="alert">
                Failed to load content.
            </div>`;
    });
}



function toggleClientId() {
    const userType = document.getElementById('userType')?.value;
    const clientIdField = document.getElementById('clientIdField');
    const clientIdInput = document.getElementById('clientIdInput');

    if (!clientIdField || !clientIdInput) return;

    if (userType === 'Client') {
        clientIdField.style.display = 'flex';  // Use 'flex' for Bootstrap row layout
        clientIdInput.setAttribute('required', 'required');
    } else {
        clientIdField.style.display = 'none';
        clientIdInput.removeAttribute('required');
        clientIdInput.value = '';  // Clear stale value
    }
}



function toggleVisibility(id) {
    const input = document.getElementById(id);
    input.type = input.type === "password" ? "text" : "password";
}

function hideForm(id) {
    const formContainer = document.getElementById(id);
    if (formContainer) {
        const form = formContainer.querySelector('form');
        if (form) form.reset();  
        formContainer.style.display = 'none';
    }
}

function showForm(id) {
    const formContainer = document.getElementById(id);
    if (formContainer) {
        const form = formContainer.querySelector('form');
        if (form) form.reset();  
        formContainer.style.display = 'block';
    }
}



