// Load all products on page load
document.addEventListener("DOMContentLoaded", () => {
    fetchProducts();

    const addForm = document.getElementById("addProductForm");
    addForm.addEventListener("submit", handleAddProduct);
});

// Fetch product list from the server (use your existing catalogue endpoint)
async function fetchProducts() {
    try {
        const res = await fetch("/catalogue"); // or your endpoint for listing all products
        if (!res.ok) throw new Error("Failed to load products");
        const products = await res.json();

        const tbody = document.getElementById("productTableBody");
        tbody.innerHTML = "";

        products.forEach(product => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${product.id}</td>
                <td>${product.name}</td>
                <td>${product.category}</td>
                <td>$${product.price.toFixed(2)}</td>
                <td>${product.stock}</td>
                <td>${product.on_shelf ? "On Shelf" : "Removed"}</td>
                <td>
                    ${product.on_shelf
                        ? `<button onclick="removeProduct(${product.id})">Remove</button>`
                        : `<em>Inactive</em>`}
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (err) {
        console.error("Error loading products:", err);
    }
}

// Handle adding a new product
async function handleAddProduct(e) {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const description = document.getElementById("description").value;
    const category = document.getElementById("category").value;
    const price = parseFloat(document.getElementById("price").value);
    const stock = parseInt(document.getElementById("stock").value);
    const msg = document.getElementById("addMessage");

    try {
        const res = await fetch("/admin/products", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, description, category, price, stock })
        });

        const data = await res.json();

        if (res.ok && !data.error) {
            msg.textContent = data.message;
            msg.style.color = "green";
            e.target.reset();
            fetchProducts(); // refresh table
        } else {
            msg.textContent = data.error || "Failed to add product.";
            msg.style.color = "red";
        }
    } catch (err) {
        console.error("Error adding product:", err);
        msg.textContent = "Error adding product.";
        msg.style.color = "red";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const removeForm = document.getElementById("removeProductForm");
    const msg = document.getElementById("removeProductMessage");

    removeForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const productId = document.getElementById("removeProductId").value;

        if (!productId) {
            msg.textContent = "Please enter a product ID.";
            msg.style.color = "red";
            return;
        }

        try {
            const res = await fetch(`/admin/products/${productId}`, {
                method: "DELETE",
                headers: { "Content-Type": "application/json" }
            });

            const data = await res.json();

            if (res.status === 403) {
                msg.textContent = "You do not have permission to remove products.";
                msg.style.color = "red";
            } else if (data.error) {
                msg.textContent = data.error;
                msg.style.color = "red";
            } else {
                msg.textContent = data.message;
                msg.style.color = "green";

                // Clear the form
                document.getElementById("removeProductId").value = "";
            }

        } catch (err) {
            console.error(err);
            msg.textContent = "Error removing product.";
            msg.style.color = "red";
        }
    });
});

