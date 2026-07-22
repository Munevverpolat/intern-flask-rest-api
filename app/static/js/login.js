const loginForm = document.getElementById("loginForm");
const loginButton = document.getElementById("loginButton");
const loginAlert = document.getElementById("loginAlert");

function showLoginAlert(message, type) {
    loginAlert.textContent = message;
    loginAlert.className = `alert alert-${type}`;
}

loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    loginAlert.className = "alert d-none";
    loginButton.disabled = true;
    loginButton.textContent = "Signing in...";

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email,
                password,
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            showLoginAlert(
                data.error || "Login failed.",
                "danger"
            );

            return;
        }

        localStorage.setItem("token", data.token);

        window.location.href = "/dashboard";
    } catch (error) {
        showLoginAlert(
            "Could not connect to the server.",
            "danger"
        );
    } finally {
        loginButton.disabled = false;
        loginButton.textContent = "Sign In";
    }
});