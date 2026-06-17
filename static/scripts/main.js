function attemptLogin() {
    const passkeyElement = document.getElementById("passkey");
    const errorMsgElement = document.getElementById("error-msg");
    
    if (!passkeyElement) return;
    const passkey = passkeyElement.value;
    errorMsgElement.innerText = "";

    // Using the relative path '/login' is standard and reliable
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ passkey: passkey })
    })
    .then(response => {
        if (!response.ok) {
            // Attempt to read JSON error payload; fall back to standard text if fails
            return response.json()
                .then(err => { throw new Error(err.message || 'Login failed') })
                .catch(() => { throw new Error('Server returned an error status') });
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            window.location.href = data.redirect; // Redirect to dashboard
        }
    })
    .catch(err => {
        console.error("Login failure details:", err);
        errorMsgElement.innerText = "Invalid Passkey or connection loss.";
    });
}