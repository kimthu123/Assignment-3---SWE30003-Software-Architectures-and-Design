document.addEventListener("DOMContentLoaded", loadCatalogue);

async function loadCatalogue() {
  const container = document.getElementById("catalogue");
  
  try {
    const res = await fetch("/catalogue");
    const products = await res.json();

    if (!products.length) {
      container.innerHTML = "<p>No products available.</p>";
      return;
    }

    container.innerHTML = products.map(p => `
      <div class="product">
        <h3>${p.name}</h3>
        <p>${p.description}</p>
        <p><b>Price: $${p.price}</b></p>
        <button onclick="addToCart(${p.id}, 1)">Add to Cart</button>
      </div>
    `).join("");

  } catch (err) {
    container.innerHTML = "<p>Error loading products.</p>";
    console.error(err);
  }
}

async function addToCart(productId, quantity) {
        const res = await fetch("/add_to_cart", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ product_id: productId, quantity: quantity })
        });

        const data = await res.json();
        alert(data.message || data.error);
}