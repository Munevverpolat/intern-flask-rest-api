const createUserForm = document.getElementById("createUserForm");
const createUserButton = document.getElementById("createUserButton");
const createUserAlert = document.getElementById("createUserAlert");

function showCreateAlert(message, type) {
    createUserAlert.textContent = message;
    createUserAlert.className = `alert alert-${type}`;
}

createUserForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    createUserAlert.className = "alert d-none";
    createUserButton.disabled = true;
    createUserButton.textContent = "Creating...";

    const payload = {
        username: document.getElementById("username").value.trim(),
        firstname: document.getElementById("firstname").value.trim(),
        middlename: document.getElementById("middlename").value.trim(),
        lastname: document.getElementById("lastname").value.trim(),
        birthdate: document.getElementById("birthdate").value,
        email: document.getElementById("email").value.trim(),
        password: document.getElementById("password").value,
    };

    try {
        const response = await fetch("/user/create", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (!response.ok) {
            showCreateAlert(
                data.error || "User could not be created.",
                "danger"
            );

            return;
        }

        showCreateAlert(
            "User created successfully. Redirecting to login...",
            "success"
        );

        createUserForm.reset();

        setTimeout(() => {
            window.location.href = "/login-page";
        }, 1500);
    } catch (error) {
        showCreateAlert(
            "Could not connect to the server.",
            "danger"
        );
    } finally {
        createUserButton.disabled = false;
        createUserButton.textContent = "Create User";
    }
});