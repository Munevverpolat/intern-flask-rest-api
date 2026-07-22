const userTableBody = document.getElementById("userTableBody");

function renderUsers(users) {
    if (!Array.isArray(users) || users.length === 0) {
        userTableBody.innerHTML = `
            <tr>
                <td colspan="5" class="text-center py-4">
                    No users found.
                </td>
            </tr>
        `;

        return;
    }

    userTableBody.innerHTML = users.map((user) => `
        <tr>
            <td>${user.id}</td>

            <td>
                <strong>${escapeHtml(user.username)}</strong>
            </td>

            <td>
                ${escapeHtml(user.firstname)}
                ${escapeHtml(user.lastname)}
            </td>

            <td>${escapeHtml(user.email)}</td>

            <td>
                <div class="action-buttons">

                    <a
                        href="/users/edit/${user.id}"
                        class="btn btn-sm edit-button"
                    >
                        Edit
                    </a>

                    <button
                        type="button"
                        class="btn btn-sm delete-button"
                        onclick="deleteUser(${user.id})"
                    >
                        Delete
                    </button>

                </div>
            </td>
        </tr>
    `).join("");
}

function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

async function loadUsers() {
    try {
        const response = await fetch("/user/list", {
            headers: getAuthHeaders(),
        });

        if (await handleUnauthorized(response)) {
            return;
        }

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Users could not be loaded."
            );
        }

        renderUsers(data);
    } catch (error) {
        showGlobalAlert(error.message);
    }
}

async function deleteUser(userId) {
    const confirmed = window.confirm(
        "Are you sure you want to delete this user?"
    );

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(
            `/user/delete/${userId}`,
            {
                method: "DELETE",
                headers: getAuthHeaders(),
            }
        );

        if (await handleUnauthorized(response)) {
            return;
        }

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "User could not be deleted."
            );
        }

        showGlobalAlert(
            "User deleted successfully.",
            "success"
        );

        await loadUsers();
    } catch (error) {
        showGlobalAlert(error.message);
    }
}

loadUsers();