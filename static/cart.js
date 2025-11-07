document.addEventListener("DOMContentLoaded", () => {
    loadCart();

    // attach clear cart button listener
    const clearBtn = document.getElementById("clearCartBtn");
    if (clearBtn) {
        clearBtn.addEventListener("click", clearCart);
    }

    // attach checkout button listener
    const checkoutBtn = document.getElementById("checkoutBtn");
    if (checkoutBtn) {
        checkoutBtn.addEventListener("click", processCheckout);
    }
});

async function processCheckout() {
    const messageDiv = document.getElementById("checkoutMessage");
    const checkoutBtn = document.getElementById("checkoutBtn");
    
    messageDiv.innerHTML = "<p>Checkout Processing</p>";

    try {
        const res = await fetch("/checkout", {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });
        
        const data = await res.json();
        
        if (data.error) {
            messageDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
            if (checkoutBtn) {
                checkoutBtn.disabled = false;
                checkoutBtn.textContent = "Checkout";
            }
        } else {
            // success, show details of order
            const order = data.order || {};
            const invoice = data.invoice || {};
            const payment = data.payment || {};
            
            messageDiv.innerHTML = `
                <div>
                    <h2>Checkout Successful!</h2>
                    <p><strong>Order ID:</strong> ${order.order_id || 'N/A'}</p>
                    <p><strong>Total Amount:</strong> $${order.total_amount || '0.00'}</p>
                    <p><strong>Payment Status:</strong> ${payment.status || 'N/A'}</p>
                    <p><strong>Invoice Number:</strong> ${invoice.invoice_id || 'N/A'}</p>
                    <p><strong>Status:</strong> ${order.status || 'N/A'}</p>
                    <p>Your order has been processed! We will pack and deliver your order soon!</p>
                </div>
            `;
            
            // reload cart (empty)
            loadCart();
        }
    } catch (err) {
        console.error("Checkout error:", err);
        messageDiv.innerHTML = `<p style="color: red;">Error: Unable  to process checkout. Please try again.</p>`;
        if (checkoutBtn) {
            checkoutBtn.disabled = false;
            checkoutBtn.textContent = "Checkout";
        }
    }
}

async function clearCart() {
    try {
        const res = await fetch("/cart/clear", {
            method: "POST"
        });
        const data = await res.json();
        alert(data.message || "Cart cleared!");
        loadCart(); // refresh cart
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
            
            // disable checkout button if empty
            const checkoutBtn = document.getElementById("checkoutBtn");
            if (checkoutBtn) {
                checkoutBtn.disabled = true;
            }
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

        // enable or disable checkout button
        const checkoutBtn = document.getElementById("checkoutBtn");
        if (checkoutBtn) {
            checkoutBtn.disabled = false;
        }

    } catch (err) {
        console.error(err);
        cartItemsDiv.innerHTML = "<p>Error loading cart.</p>";
        cartTotalP.innerHTML = "<b>Total: $0</b>";
    }
}
