function loadContent(endpoint) {
    fetch(endpoint)
        .then(response => {
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
