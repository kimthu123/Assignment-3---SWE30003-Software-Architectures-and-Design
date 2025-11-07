document.addEventListener("DOMContentLoaded", () => {
    const loginTab = document.getElementById("loginTab");
    const signupTab = document.getElementById("signupTab");
    const deleteTab = document.getElementById("deleteTab");
    const loginForm = document.getElementById("loginForm");
    const signupForm = document.getElementById("signupForm");
    const deleteForm = document.getElementById("deleteForm");
    const updateTab = document.getElementById("updateTab");
    const updateForm = document.getElementById("updateForm");


    // Switch between login and signup forms
    loginTab.addEventListener("click", () => switchTab("login"));
    signupTab.addEventListener("click", () => switchTab("signup"));
    deleteTab.addEventListener("click", () => switchTab("delete"));
    updateTab.addEventListener("click", () => switchTab("update"));

    function switchTab(tab) {
        loginForm.classList.add("hidden");
        signupForm.classList.add("hidden");
        deleteForm.classList.add("hidden");
        updateForm.classList.add("hidden");

        loginTab.classList.remove("active");
        signupTab.classList.remove("active");
        deleteTab.classList.remove("active");
        updateTab.classList.remove("active");

        if (tab === "login") {
            loginForm.classList.remove("hidden");
            loginTab.classList.add("active");
        } else if (tab === "signup") {
            signupForm.classList.remove("hidden");
            signupTab.classList.add("active");
        } else if (tab === "delete") {
            deleteForm.classList.remove("hidden");
            deleteTab.classList.add("active");
        } else if (tab === "update") {
            updateForm.classList.remove("hidden");
            updateTab.classList.add("active");
        }
    }


    // Handle login
    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const email = document.getElementById("loginEmail").value;
        const password = document.getElementById("loginPassword").value;

        try {
            const res = await fetch("/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });
            const data = await res.json();

            const msg = document.getElementById("loginMessage");
            if (data.error) {
                msg.textContent = data.error;
                msg.style.color = "red";
            } else {
                msg.textContent = "Login successful!";
                msg.style.color = "green";
                localStorage.setItem("user", JSON.stringify(data.account));
                setTimeout(() => window.location.href = "/", 1000);
            }
        } catch (err) {
            console.error(err);
        }
    });

    signupForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const email = document.getElementById("signupEmail").value;
        const password = document.getElementById("signupPassword").value;
        const account_type = document.getElementById("account_type").value;

        try {
            const res = await fetch("/signup", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password, account_type })
            });
            const data = await res.json();

            const msg = document.getElementById("signupMessage");
            if (data.error) {
                msg.textContent = data.error;
                msg.style.color = "red";
            } else {
                msg.textContent = "Account created successfully!";
                msg.style.color = "green";
                setTimeout(() => switchTab("login"), 1000);
            }
        } catch (err) {
            console.error(err);
        }
    });

    // Handle account deletion
    deleteForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const email = document.getElementById("deleteEmail").value;
        const msg = document.getElementById("deleteMessage");

        try {
            const res = await fetch("/delete_account", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email })
            });
            const data = await res.json();

            if (data.error) {
                msg.textContent = data.error;
                msg.style.color = "red";
            } else {
                msg.textContent = data.message;
                msg.style.color = "green";

                // Clear form fields
                document.getElementById("deleteEmail").value = "";

                // Switch back to login after 1 second
                setTimeout(() => switchTab("login"), 1000);
            }
        } catch (err) {
            console.error(err);
            msg.textContent = "Failed to delete account.";
            msg.style.color = "red";
        }
    });

    updateForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const currentEmail = document.getElementById("currentEmail").value;
        const currentPassword = document.getElementById("currentPassword").value;
        const newEmail = document.getElementById("newEmail").value;
        const newPassword = document.getElementById("newPassword").value;
        const msg = document.getElementById("updateMessage");

        try {
            const res = await fetch("/update_account", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    email: currentEmail,
                    new_email: newEmail,
                    new_password: newPassword
                })
            });
            const data = await res.json();

            if (data.error) {
                msg.textContent = data.error;
                msg.style.color = "red";
            } else {
                msg.textContent = data.message;
                msg.style.color = "green";

                // Clear fields
                document.getElementById("currentEmail").value = "";
                document.getElementById("currentPassword").value = "";
                document.getElementById("newEmail").value = "";
                document.getElementById("newPassword").value = "";

                // Switch back to login after 1 second
                setTimeout(() => switchTab("login"), 1000);
            }
        } catch (err) {
            console.error(err);
            msg.textContent = "Failed to update account.";
            msg.style.color = "red";
        }
    });

});
