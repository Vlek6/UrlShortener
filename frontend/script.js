document.getElementById('shortenForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent default form submission

    const url = document.getElementById('urlInput').value.trim();
    const resultDiv = document.getElementById('result');

    if (!url) {
        resultDiv.innerHTML = "<p class='error'>Please enter a URL.</p>";
        return;
    }

    resultDiv.innerHTML = "<p>Processing...</p>";

    try {
        const response = await fetch('http://localhost:8000/shrink', {  // Use 'localhost'
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ original_url: url })  // Match the backend's expected schema
        });

        const data = await response.json();

        if (response.ok) {
            if (data.short_url) {
                // Display the shortened URL
                const shortUrl = `http://localhost:8000/${data.short_url}`;
                resultDiv.innerHTML = `<p>Your shortened URL: <a href="${shortUrl}" target="_blank">${shortUrl}</a></p>`;
            } else if (data.message) {
                // Display the processing message
                resultDiv.innerHTML = `<p>${data.message}</p>`;
            } else {
                resultDiv.innerHTML = `<p class='error'>Unexpected response format.</p>`;
            }
        } else {
            // Display error message from backend
            resultDiv.innerHTML = `<p class='error'>Error: ${data.detail || 'Something went wrong.'}</p>`;
        }
    } catch (error) {
        // Display network or other errors
        resultDiv.innerHTML = `<p class='error'>An error occurred: ${error.message}</p>`;
    }
});
