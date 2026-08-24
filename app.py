"""
app.py
======

A simple, beginner-friendly AI shopping assistant built with Flask.

The application demonstrates a basic *agentic workflow* with three
steps, each implemented as a separate function:

  1. understand_request()  — Agent 1: extracts category & budget
  2. search_products()      — Agent 2: finds matching products
  3. recommend_products()   — Agent 3: ranks & returns the best 3

Run locally:
    pip install -r requirements.txt
    python app.py
Then visit http://127.0.0.1:5000 in your browser.
"""

import re

from flask import Flask, render_template, request, jsonify

from products import get_all_products

app = Flask(__name__)


# ============================================================================
#  Agent 1: Understand the user's request
# ============================================================================

# Keywords that map to each product category.
CATEGORY_KEYWORDS = {
    "Laptops": ["laptop", "notebook", "ultrabook"],
    "Smartphones": ["phone", "smartphone", "mobile", "android"],
    "Headphones": ["headphone", "headset", "earphone", "speaker", "audio"],
    "Smartwatches": ["watch", "smartwatch", "fitness band", "wearable"],
}


def extract_category(query):
    """Detect the product category from keywords in the query."""
    query_lower = query.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            # \b ensures we match whole words only, so "phone"
            # does not accidentally match inside "headphones".
            if re.search(r"\b" + re.escape(kw) + r"s?\b", query_lower):
                return category
    return None


def extract_budget(query):
    """Extract the maximum budget (as an integer) from the query.

    Handles patterns like:
      ₹60,000   ₹60000   60000   60k   60 thousand
    Returns None if no budget is mentioned.
    """
    query_lower = query.lower()

    # Pattern 1: ₹60,000 or ₹60000
    match = re.search(r"[₹$]\s*([\d,]+)", query)
    if match:
        return int(match.group(1).replace(",", ""))

    # Pattern 2: 60k or 60 thousand
    match = re.search(r"(\d+)\s*(?:k|thousand)", query_lower)
    if match:
        return int(match.group(1)) * 1000

    # Pattern 3: "under 60000" / "below 25000" / "budget 50000"
    match = re.search(
        r"(?:under|below|budget|max|cost\s*limit|less than)\s*[^\d]{0,5}([\d,]+)",
        query_lower,
    )
    if match:
        return int(match.group(1).replace(",", ""))

    return None


def understand_request(query):
    """Agent 1 — Understand the user's request.

    Parses a natural-language query and returns a dictionary with
    two keys:
      - 'category'  : the detected product category (or None)
      - 'budget'    : the maximum price as an integer (or None)

    Example:
        >>> understand_request("I need a laptop under ₹60,000 for coding")
        {'category': 'Laptops', 'budget': 60000}
    """
    return {
        "category": extract_category(query),
        "budget": extract_budget(query),
    }


# ============================================================================
#  Agent 2: Search for matching products
# ============================================================================

def search_products(category, budget):
    """Agent 2 — Search the product catalogue.

    Filters the built-in product list by *category* and/or *budget*.
    If no category is detected, returns products from all categories.

    Parameters
    ----------
    category : str or None — e.g. "Laptops"
    budget   : int or None — maximum price in rupees

    Returns
    -------
    list[dict] — matching product dictionaries
    """
    all_products = get_all_products()

    # Step 1: filter by category (if one was detected).
    if category:
        results = [p for p in all_products if p["category"] == category]
    else:
        results = list(all_products)

    # Step 2: filter by budget (keep only affordable products).
    if budget is not None:
        results = [p for p in results if p["price"] <= budget]

    return results


# ============================================================================
#  Agent 3: Rank and recommend the best products
# ============================================================================

def calculate_score(product, budget=None):
    """Compute a simple relevance score for a product.

    Higher is better.  The score rewards:
      • A higher rating          (+ rating * 10 points)
      • A lower price             (- price / 10000, so cheaper wins)
      • Staying within budget     (+5 bonus)

    Returns a float rounded to 2 decimal places.
    """
    score = product["rating"] * 10.0          # rating component
    score -= product["price"] / 10000.0       # price component (lower = better)

    if budget is not None and product["price"] <= budget:
        score += 5.0  # bonus for staying within budget

    return round(score, 2)


def generate_explanation(product, budget=None, category=None):
    """Create a short, human-readable explanation for why a product
    is a good recommendation."""
    parts = []

    # Rating
    parts.append(f"It has a {product['rating']}-star rating")

    # Price vs. budget
    if budget is not None:
        if product["price"] <= budget:
            diff = budget - product["price"]
            parts.append(
                f"is within your budget of ₹{budget:,} "
                f"(₹{diff:,} under)"
            )
        else:
            parts.append(f"costs ₹{product['price']:,} (slightly above budget)")
    else:
        parts.append(f"costs ₹{product['price']:,}")

    # Category fit
    if category:
        parts.append(f"suitable for {category.lower()}")

    explanation = ", ".join(parts) + "."
    return explanation[0].upper() + explanation[1:]


def recommend_products(products, budget=None, category=None, limit=3):
    """Agent 3 — Rank products and return the best *limit*.

    Each returned product is a copy of the original dictionary
    with two extra fields:
      - 'score'         : relevance score (float)
      - 'explanation'   : why it is recommended (str)
    """
    # Compute scores and enrich each product.
    enriched = []
    for p in products:
        p_copy = dict(p)
        p_copy["score"] = calculate_score(p, budget)
        p_copy["explanation"] = generate_explanation(p, budget, category)
        enriched.append(p_copy)

    # Sort by score, highest first.
    enriched.sort(key=lambda x: x["score"], reverse=True)

    # Return the top *limit* products.
    return enriched[:limit]


# ============================================================================
#  Flask routes
# ============================================================================

@app.route("/")
def home():
    """Serve the main page."""
    return render_template("index.html")


@app.route("/api/search", methods=["POST"])
def api_search():
    """
    Handle a search request.

    Expects JSON:  {"query": "I need a laptop under ₹60,000 for coding"}
    Returns JSON:  {"success": true, "data": { ...recommendations... }}
    """
    try:
        data = request.get_json(silent=True)
        if not data or "query" not in data:
            return jsonify({"success": False, "error": "Query is required"}), 400

        query = str(data["query"]).strip()
        if not query:
            return jsonify({"success": False, "error": "Query cannot be empty"}), 400

        # ── Agentic workflow ──────────────────────────────────────
        # Agent 1: Understand what the user wants.
        requirements = understand_request(query)

        # Agent 2: Find matching products.
        matches = search_products(requirements["category"], requirements["budget"])

        # Agent 3: Rank and recommend the best 3.
        recommendations = recommend_products(
            matches,
            budget=requirements["budget"],
            category=requirements["category"],
            limit=3,
        )

        # Build a friendly summary message.
        if not recommendations:
            summary = (
                "I could not find any products matching your criteria. "
                "Please try again with a different budget or category."
            )
        else:
            top = recommendations[0]
            summary = (
                f"Found {len(recommendations)} product(s) matching your request. "
                f"My top recommendation is **{top['name']}** "
                f"(₹{top['price']:,}, {top['rating']}-star rating)."
            )
            if requirements["budget"]:
                summary += f" All results are within your budget of ₹{requirements['budget']:,}."

        return jsonify({
            "success": True,
            "data": {
                "query": query,
                "requirements": requirements,
                "recommendations": recommendations,
                "explanation": summary,
                "count": len(recommendations),
            },
        })

    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


# ============================================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
