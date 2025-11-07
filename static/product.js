document.addEventListener("DOMContentLoaded", () => {
    fetchProducts();

    const addForm = document.getElementById("addProductForm");
    addForm.addEventListener("submit", handleAddProduct);
});

async function fetchProducts() {
    try {
        const res = await fetch("/catalogue");
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

async function handleAddProduct(e) {
    e.preventDefault();

    const name = document.getElementById("name").value.trim();
    const description = document.getElementById("description").value.trim();
    const category = document.getElementById("category").value.trim();
    const priceRaw = document.getElementById("price").value;
    const stockRaw = document.getElementById("stock").value;
    const msg = document.getElementById("addMessage");

    msg.textContent = "";
    if (!name) {
        msg.textContent = "Product name is required.";
        return;
    }

    if (name.length < 3) {
        msg.textContent = "Product name must be at least 3 characters.";
        return;
    }

    if (name.length > 255) {
        msg.textContent = "Product name must be 255 characters or fewer.";
        return;
    }

    if (!description) {
        msg.textContent = "Product description is required.";
        return;
    }

    if (description.length < 5) {
        msg.textContent = "Description must be at least 5 characters.";
        return;
    }

    if (description.length > 500) {
        msg.textContent = "Description must be 500 characters or fewer.";
        return;
    }

    if (!category) {
        msg.textContent = "Product category is required.";
        return;
    }

    if (category.length < 3) {
        msg.textContent = "Category must be at least 3 characters.";
        return;
    }

    if (category.length > 20) {
        msg.textContent = "Category must be 20 characters or fewer.";
        return;
    }

    const price = Number(priceRaw);
    if (!Number.isFinite(price) || priceRaw.trim() === "") {
        msg.textContent = "Price must be a valid number.";
        return;
    }

    if (price < 0) {
        msg.textContent = "Price cannot be negative.";
        return;
    }

    const stock = Number(stockRaw);
    if (!Number.isInteger(stock) || stockRaw.trim() === "") {
        msg.textContent = "Stock must be a whole number.";
        return;
    }

    if (stock < 0) {
        msg.textContent = "Stock cannot be negative.";
        return;
    }

    try {
        const res = await fetch("/admin/products", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, description, category, price, stock })
        });

        const data = await res.json();

        if (res.ok && !data.error) {
            msg.textContent = data.message;
            e.target.reset();
            fetchProducts();
        } else {
            msg.textContent = data.error || "Failed to add product.";
        }
    } catch (err) {
        console.error("Error adding product:", err);
        msg.textContent = "Error adding product.";
    }
}

async function removeProduct(productId) {
    if (!confirm(`Are you sure you want to remove product #${productId}?`)) {
        return;
    }

    try {
        const res = await fetch(`/admin/products/${productId}`, {
            method: "DELETE",
            headers: { "Content-Type": "application/json" }
        });

        const data = await res.json();

        if (res.status === 403) {
            alert("You do not have permission to remove products.");
        } else if (data.error) {
            alert(data.error);
        } else {
            alert(data.message);
            fetchProducts();
        }
    } catch (err) {
        console.error(err);
        alert("Error removing product.");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const removeForm = document.getElementById("removeProductForm");
    const msg = document.getElementById("removeProductMessage");

    removeForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const productId = document.getElementById("removeProductId").value.trim();

        msg.textContent = "";

        if (!productId) {
            msg.textContent = "Please enter a product ID.";
            return;
        }

        const parsedId = Number(productId);
        if (!Number.isInteger(parsedId) || parsedId <= 0) {
            msg.textContent = "Product ID must be a positive full number.";
            return;
        }

        try {
            const res = await fetch(`/admin/products/${parsedId}`, {
                method: "DELETE",
                headers: { "Content-Type": "application/json" }
            });

            const data = await res.json();

            if (res.status === 403) {
                msg.textContent = "You do not have permission to remove products.";
            } else if (data.error) {
                msg.textContent = data.error;
            } else {
                msg.textContent = data.message;
                document.getElementById("removeProductId").value = "";
                fetchProducts();
            }

        } catch (err) {
            console.error(err);
            msg.textContent = "Error removing product.";
        }
    });
});

