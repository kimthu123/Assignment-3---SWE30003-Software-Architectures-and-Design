document.addEventListener("DOMContentLoaded", () => {
    loadCart();

    // attach clear cart button listener
    const clearBtn = document.getElementById("clearCartBtn");
    if (clearBtn) {
        clearBtn.addEventListener("click", clearCart);
    }
});

async function clearCart() {
    try {
        const res = await fetch("/cart/clear", {
            method: "POST"
        });
        const data = await res.json();
        alert(data.message || "Cart cleared!");
        loadCart(); // refresh cart display
    } catch (err) {
        console.error(err);
        alert("Failed to clear cart");
    }
}

async function loadCart() {
    const cartItemsDiv = document.getElementById("cartItems");
    const cartTotalP = document.getElementById("cartTotal");

    try {
        const res = await fetch("/cart");
        const cartData = await res.json();
        const cartItems = cartData.items;

        if (!cartItems || !cartItems.length) {
            cartItemsDiv.innerHTML = "<p>Your cart is empty.</p>";
            cartTotalP.innerHTML = "<b>Total: $0</b>";
            return;
        }

        let total = 0;

        const detailedItems = await Promise.all(
            cartItems.map(async item => {
                const res = await fetch(`/catalogue/product/${item.product_id}`);
                const product = await res.json();
                return {...product, quantity: item.quantity};
            })
        );

        cartItemsDiv.innerHTML = detailedItems.map(item => {
            if (item.error) return "";
            const subtotal = item.price * item.quantity;
            total += subtotal;
            return `
                <div class="cart-item">
                    <p>${item.name} x ${item.quantity} — $${item.price} each, subtotal: $${subtotal}</p>
                </div>
            `;
        }).join("");

        cartTotalP.innerHTML = `<b>Total: $${total}</b>`;

    } catch (err) {
        console.error(err);
        cartItemsDiv.innerHTML = "<p>Error loading cart.</p>";
        cartTotalP.innerHTML = "<b>Total: $0</b>";
    }
}
