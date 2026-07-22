const editUserPage = document.getElementById("editUserPage");
const userId = editUserPage.dataset.userId;

const editUserForm = document.getElementById("editUserForm");
const updateUserButton = document.getElementById("updateUserButton");
const editUserAlert = document.getElementById("editUserAlert");

function showEditAlert(message, type) {
    editUserAlert.textContent = message;
    editUserAlert.className = `alert alert-${type}`;
}

async function loadUser() {
    try {
        const response = await fetch("/user/list", {
            headers: getAuthHeaders(),
        });

        if (await handleUnauthorized(response)) {
            return;
        }

        const users = await response.json();

        if (!response.ok) {
            throw new Error(
                users.error || "User could not be loaded."
            );
        }

        const user = users.find(
            (item) => Number(item.id) === Number(userId)
        );

        if (!user) {
            throw new Error("User not found.");
        }

        document.getElementById("firstname").value =
            user.firstname || "";

        document.getElementById("lastname").value =
            user.lastname || "";

        document.getElementById("email").value =
            user.email || "";
    } catch (error) {
        showEditAlert(error.message, "danger");
    }
}

editUserForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    updateUserButton.disabled = true;
    updateUserButton.textContent = "Saving...";

    const payload = {
        firstname: document.getElementById("firstname").value.trim(),
        lastname: document.getElementById("lastname").value.trim(),
        email: document.getElementById("email").value.trim(),
    };

    try {
        const response = await fetch(
            `/user/update/${userId}`,
            {
                method: "PUT",
                headers: getAuthHeaders(true),
                body: JSON.stringify(payload),
            }
        );

        if (await handleUnauthorized(response)) {
            return;
        }

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "User could not be updated."
            );
        }

        showEditAlert(
            "User updated successfully.",
            "success"
        );

        setTimeout(() => {
            window.location.href = "/users";
        }, 1000);
    } catch (error) {
        showEditAlert(error.message, "danger");
    } finally {
        updateUserButton.disabled = false;
        updateUserButton.textContent = "Save Changes";
    }
});

loadUser();