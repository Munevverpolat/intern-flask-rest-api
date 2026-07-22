async function loadDashboard() {
    try {
        const [
            healthResponse,
            usersResponse,
            onlineResponse,
        ] = await Promise.all([
            fetch("/health"),
            fetch("/user/list", {
                headers: getAuthHeaders(),
            }),
            fetch("/onlineusers", {
                headers: getAuthHeaders(),
            }),
        ]);

        if (
            await handleUnauthorized(usersResponse) ||
            await handleUnauthorized(onlineResponse)
        ) {
            return;
        }

        const healthData = await healthResponse.json();
        const users = await usersResponse.json();
        const onlineUsers = await onlineResponse.json();

        document.getElementById("totalUsers").textContent =
            Array.isArray(users) ? users.length : 0;

        document.getElementById("onlineUsers").textContent =
            Array.isArray(onlineUsers) ? onlineUsers.length : 0;

        document.getElementById("apiStatus").textContent =
            healthResponse.ok
                ? healthData.message
                : "API unavailable";
    } catch (error) {
        showGlobalAlert(
            "Dashboard data could not be loaded."
        );
    }
}

loadDashboard();