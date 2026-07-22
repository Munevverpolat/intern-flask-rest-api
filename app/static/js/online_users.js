const onlineUsersTableBody = document.getElementById(
    "onlineUsersTableBody"
);

const refreshOnlineUsersButton = document.getElementById(
    "refreshOnlineUsers"
);

function renderOnlineUsers(users) {
    if (!Array.isArray(users) || users.length === 0) {
        onlineUsersTableBody.innerHTML = `
            <tr>
                <td colspan="4" class="text-center py-4">
                    No online users found.
                </td>
            </tr>
        `;

        return;
    }

    onlineUsersTableBody.innerHTML = users.map((user) => `
        <tr>
            <td>${user.id}</td>

            <td>
                <span class="online-user">
                    <span class="online-dot"></span>
                    ${user.username}
                </span>
            </td>

            <td>${user.ipaddress}</td>

            <td>${user.logindatetime}</td>
        </tr>
    `).join("");
}

async function loadOnlineUsers() {
    try {
        const response = await fetch("/onlineusers", {
            headers: getAuthHeaders(),
        });

        if (await handleUnauthorized(response)) {
            return;
        }

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Online users could not be loaded."
            );
        }

        renderOnlineUsers(data);
    } catch (error) {
        showGlobalAlert(error.message);
    }
}

refreshOnlineUsersButton.addEventListener(
    "click",
    loadOnlineUsers
);

loadOnlineUsers();