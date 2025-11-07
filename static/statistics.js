document.addEventListener("DOMContentLoaded", async () => {
    const messageElement = document.getElementById("statisticsMessage");
    const contentElement = document.getElementById("statisticsContent");

    if (!messageElement || !contentElement) {
        return;
    }

    try {
        const response = await fetch("/admin/statistics");

        if (!response.ok) {
            if (response.status === 403) {
                messageElement.textContent = "You do not have permission to view these statistics.";
                return;
            }
            throw new Error("Failed to fetch statistics");
        }

        const stats = await response.json();
        renderStatistics(stats, messageElement, contentElement);
    } catch (err) {
        console.error("Statistics error:", err);
        messageElement.textContent = "Unable to load statistics. Please try again.";
    }
});

function renderStatistics(stats, messageElement, contentElement) {
    const mostBought = stats?.most_bought_product;
    const avgRevenue = stats?.average_revenue_by_month || {};
    const avgQty = stats?.average_quantity_per_product || {};

    const formatCurrency = (v) => {
        const n = Number(v);
        return Number.isNaN(n) ? v : `$${n.toFixed(2)}`;
    };

    //JS object into html ul
    const renderList = (obj, valFmt) => {
        const entries = obj ? Object.entries(obj) : [];
        if (!entries.length) return "<p>No data available.</p>";
        return `<ul>${entries.map(([k, v]) => `<li>${k}: ${valFmt ? valFmt(v) : v}</li>`).join("")}</ul>`;
    };

    contentElement.innerHTML = `
        <article class="card">
            <h2>Most Bought Product</h2>
            ${mostBought ? `
                <ul>
                    <li>Product: ${mostBought.product_name ?? "N/A"}</li>
                    <li>Total Quantity: ${mostBought.total_quantity ?? 0}</li>
                </ul>
            ` : `<p>No data available.</p>`}
        </article>

        <article class="card">
            <h2>Average Revenue by Month</h2>
            ${renderList(avgRevenue, formatCurrency)}
        </article>

        <article class="card">
            <h2>Average Quantity per Product</h2>
            ${renderList(avgQty)}
        </article>
    `;
    messageElement.textContent = "";
}


