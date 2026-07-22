const token = localStorage.getItem("token");

const publicPaths = [
    "/",
    "/login-page",
    "/users/create",
];

const currentPath = window.location.pathname;

if (!token && !publicPaths.includes(currentPath)) {
    window.location.href = "/login-page";
}

function getAuthHeaders(includeJson = false) {
    const headers = {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
    };

    if (includeJson) {
        headers["Content-Type"] = "application/json";
    }

    return headers;
}

function showGlobalAlert(message, type = "danger") {
    const alertElement = document.getElementById("globalAlert");

    if (!alertElement) {
        return;
    }

    alertElement.textContent = message;
    alertElement.className = `alert alert-${type}`;
}

async function handleUnauthorized(response) {
    if (response.status === 401) {
        localStorage.removeItem("token");
        window.location.href = "/login-page";
        return true;
    }

    return false;
}

const logoutButton = document.getElementById("logoutButton");

if (logoutButton) {
    logoutButton.addEventListener("click", async () => {
        try {
            await fetch("/logout", {
                method: "POST",
                headers: getAuthHeaders(),
            });
        } finally {
            localStorage.removeItem("token");
            window.location.href = "/login-page";
        }
    });
}