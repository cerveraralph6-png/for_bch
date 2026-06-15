function attemptLogin() {
    const passkey = document.getElementById('passkey').value;
    const errorDiv = document.getElementById('error-msg');

    if (!passkey) {
        errorDiv.innerText = "Please enter a passkey";
        return;
    }

    fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ passkey: passkey })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            // Redirect to the internal dashboard
            window.location.href = "/dashboard";
        } else {
            errorDiv.innerText = data.message;
        }
    })
    .catch(err => {
        errorDiv.innerText = "Database connection error";
        console.error(err);
    });
}