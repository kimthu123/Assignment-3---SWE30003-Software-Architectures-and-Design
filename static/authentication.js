// authentication
window.loginEmail = null;

// check localstorage on page load
function checkLoginStatus() {
    const storedUser = localStorage.getItem("user");

    if (storedUser) {
        try {
            const user = JSON.parse(storedUser);
            window.loginEmail = user?.email || null;
        } catch (err) {
            window.loginEmail = null;
            localStorage.removeItem("user");
        }
    } else {
        window.loginEmail = null;
    }

    if (window.loginEmail) {
        updateNavForLoggedIn();
    } else {
        updateNavLoggedOut();
    }
}

// update nav bar when user is logged in
function updateNavForLoggedIn() {
    const navs = document.querySelectorAll("nav");
    navs.forEach(nav => {
        if (window.loginEmail) {
            // Find Account link
            const accountLink = Array.from(nav.querySelectorAll("a")).find(a => 
                a.textContent.includes("Account") || a.href.includes("login_page")
            );
            
            if (accountLink) {
                // replace account with email + logout button
                const emailSpan = document.createElement("span");
                emailSpan.textContent = window.loginEmail;
                emailSpan.style.marginRight = "10px";

                const productLink = document.createElement("a");
                productLink.textContent = "Product Management";
                productLink.href = "/product_page"; // <-- your Flask route for the page
                productLink.style.marginRight = "10px";
                productLink.style.textDecoration = "none";
                productLink.style.color = "blue";
                productLink.style.cursor = "pointer";
                
                const logoutBtn = document.createElement("button");
                logoutBtn.textContent = "Logout";
                logoutBtn.onclick = (e) => {
                    e.preventDefault();
                    logout();
                };
                logoutBtn.style.marginLeft = "10px";
                logoutBtn.style.cursor = "pointer";
                
                // Replace the Account link
                accountLink.replaceWith(emailSpan, productLink, logoutBtn);
            }
        }
    });
}

// update nav bar when logged out
function updateNavLoggedOut() {
    const navs = document.querySelectorAll("nav");
    navs.forEach(nav => {
        // Check if there's a logout button (means user was logged in)
        const logoutBtn = Array.from(nav.querySelectorAll("button")).find(btn => 
            btn.textContent === "Logout"
        );
        
        if (logoutBtn) {
            // locate email span
            const emailSpan = logoutBtn.previousSibling;
            
            // remove span for email + remove logout button
            if (emailSpan && emailSpan.nodeType === 1) {
                emailSpan.remove();
            }
            logoutBtn.remove();
            
            // add account to nav bar
            const separator = document.createTextNode(" | ");
            const accountLink = document.createElement("a");
            accountLink.href = "/login_page";
            accountLink.textContent = "Account";
            
            // Find the last link (Cart) and add after it
            const cartLink = Array.from(nav.querySelectorAll("a")).find(a => 
                a.href.includes("cart_page")
            );
            if (cartLink && cartLink.nextSibling) {
                cartLink.parentNode.insertBefore(separator, cartLink.nextSibling);
                cartLink.parentNode.insertBefore(accountLink, separator.nextSibling);
            } else if (cartLink) {
                nav.appendChild(separator);
                nav.appendChild(accountLink);
            }
        }
    });
}

// logout function
function logout() {
    window.loginEmail = null;
    localStorage.removeItem("user");
    updateNavLoggedOut();
    window.location.href = "/";
}

// initialize on page load
document.addEventListener("DOMContentLoaded", () => {
    checkLoginStatus();
});
