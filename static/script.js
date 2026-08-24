/* ===============================================================
   script.js — Frontend logic for the AI Shopping Assistant
   Sends search queries to the Flask backend and renders results.
   =============================================================== */

document.addEventListener("DOMContentLoaded", function () {
    const queryInput = document.getElementById("query-input");
    const findBtn = document.getElementById("find-btn");
    const resultsDiv = document.getElementById("results");
    const loadingDiv = document.getElementById("loading");

    // ── Send a search request to the backend ─────────────────────────
    async function search() {
        const query = queryInput.value.trim();
        if (!query) {
            alert("Please enter what you are looking for.");
            return;
        }

        // Show loading state.
        loadingDiv.classList.remove("hidden");
        resultsDiv.innerHTML = "";
        findBtn.disabled = true;
        queryInput.disabled = true;

        try {
            const response = await fetch("/api/search", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: query }),
            });
            const result = await response.json();

            if (!result.success) {
                showError(result.error || "Something went wrong.");
                return;
            }

            renderResults(result.data);

        } catch (error) {
            showError("Could not connect to the server.");
            console.error("Search error:", error);
        } finally {
            loadingDiv.classList.add("hidden");
            findBtn.disabled = false;
            queryInput.disabled = false;
            queryInput.focus();
        }
    }

    // ── Render the search results on the page ────────────────────────
    function renderResults(data) {
        resultsDiv.innerHTML = "";

        // 1. Summary message
        const summaryDiv = document.createElement("div");
        summaryDiv.className = "summary";
        summaryDiv.innerHTML = formatMessage(data.explanation);
        resultsDiv.appendChild(summaryDiv);

        // 2. Product cards
        const products = data.recommendations;
        if (products.length > 0) {
            const grid = document.createElement("div");
            grid.className = "product-grid";

            products.forEach((product) => {
                const card = createProductCard(product);
                grid.appendChild(card);
            });

            resultsDiv.appendChild(grid);
        }
    }

    // ── Create a single product card element ────────────────────────
    function createProductCard(product) {
        const card = document.createElement("div");
        card.className = "product-card";

        // Star rating display
        const fullStars = Math.round(product.rating);
        const emptyStars = 5 - fullStars;
        const stars = "★".repeat(fullStars) + "☆".repeat(emptyStars);

        let featuresHtml = "";
        product.features.slice(0, 4).forEach((feat) => {
            featuresHtml += '<span class="feature-tag">' + escapeHtml(feat) + "</span>";
        });

        card.innerHTML =
            "<h3>" + escapeHtml(product.name) + "</h3>" +
            '<div class="brand">' + escapeHtml(product.brand) + "</div>" +
            '<div class="price">&#8377;' + Number(product.price).toLocaleString("en-IN") + "</div>" +
            '<div class="rating">' + stars + " (" + product.rating + ")</div>" +
            (product.score !== undefined
                ? '<div class="score">Match Score: ' + product.score + "</div>"
                : "") +
            '<div class="features">' + featuresHtml + "</div>" +
            '<div class="explanation">' + escapeHtml(product.explanation) + "</div>";

        return card;
    }

    // ── Helper: escape HTML to prevent XSS ──────────────────────────
    function escapeHtml(text) {
        const div = document.createElement("div");
        div.textContent = text;
        return div.innerHTML;
    }

    // ── Helper: format simple markdown to HTML ────────────────────────
    function formatMessage(text) {
        return text
            .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
            .replace(/\n/g, "<br>");
    }

    // ── Show an error message ────────────────────────────────────────
    function showError(message) {
        resultsDiv.innerHTML =
            '<div class="summary" style="color: #ef4444;">Error: ' +
            escapeHtml(message) +
            "</div>";
    }

    // ── Event listeners ──────────────────────────────────────────────
    findBtn.addEventListener("click", search);

    queryInput.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            e.preventDefault();
            search();
        }
    });

    // Focus the input on page load.
    queryInput.focus();
});
