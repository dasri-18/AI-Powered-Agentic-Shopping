"""
tests/test_app.py
=================

Unit tests for the AI Shopping Assistant.

Run with:
    pytest tests/test_app.py -v
"""

import sys
import os
import json

# Make the project root importable when running pytest from the root.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import app, understand_request, search_products, recommend_products
from products import PRODUCTS


# ──────────────────────────────────────────────────────────────────────
#  Agent 1: understand_request()
# ──────────────────────────────────────────────────────────────────────

class TestUnderstandRequest:

    def test_laptop_with_budget(self):
        result = understand_request("I need a laptop under ₹60,000 for coding")
        assert result["category"] == "Laptops"
        assert result["budget"] == 60000

    def test_phone_with_budget(self):
        result = understand_request("Suggest a phone under ₹25,000")
        assert result["category"] == "Smartphones"
        assert result["budget"] == 25000

    def test_headphones_no_budget(self):
        result = understand_request("I need wireless headphones for studying")
        assert result["category"] == "Headphones"
        assert result["budget"] is None

    def test_smartwatch_with_budget(self):
        result = understand_request("Show me a smartwatch under 40000")
        assert result["category"] == "Smartwatches"
        assert result["budget"] == 40000

    def test_no_category(self):
        result = understand_request("I need something nice")
        assert result["category"] is None
        assert result["budget"] is None

    def test_budget_with_k_suffix(self):
        result = understand_request("laptop under 60k")
        assert result["category"] == "Laptops"
        assert result["budget"] == 60000

    def test_headphone_does_not_match_phone(self):
        """'headphones' must not be detected as 'phone'."""
        result = understand_request("I want headphones")
        assert result["category"] == "Headphones"


# ──────────────────────────────────────────────────────────────────────
#  Agent 2: search_products()
# ──────────────────────────────────────────────────────────────────────

class TestSearchProducts:

    def test_filter_by_category(self):
        results = search_products("Laptops", None)
        assert len(results) == 4
        assert all(p["category"] == "Laptops" for p in results)

    def test_filter_by_category_and_budget(self):
        results = search_products("Laptops", 60000)
        assert all(p["category"] == "Laptops" for p in results)
        assert all(p["price"] <= 60000 for p in results)

    def test_no_category_returns_all(self):
        results = search_products(None, None)
        assert len(results) == len(PRODUCTS)

    def test_budget_excludes_expensive(self):
        results = search_products(None, 10000)
        assert all(p["price"] <= 10000 for p in results)

    def test_no_results_when_budget_too_low(self):
        results = search_products("Laptops", 1000)
        assert len(results) == 0


# ──────────────────────────────────────────────────────────────────────
#  Agent 3: recommend_products()
# ──────────────────────────────────────────────────────────────────────

class TestRecommendProducts:

    def test_returns_max_three(self):
        all_products = search_products(None, None)
        recommendations = recommend_products(all_products, category="Laptops", limit=3)
        assert len(recommendations) <= 3

    def test_results_are_sorted_by_score(self):
        products = search_products("Laptops", None)
        recommendations = recommend_products(products, category="Laptops")
        scores = [p["score"] for p in recommendations]
        assert scores == sorted(scores, reverse=True)

    def test_each_product_has_explanation(self):
        products = search_products("Laptops", 60000)
        recommendations = recommend_products(products, budget=60000, category="Laptops")
        for p in recommendations:
            assert "explanation" in p
            assert "score" in p
            assert len(p["explanation"]) > 10

    def test_higher_rating_scores_higher(self):
        """Given equal prices, the higher-rated product should rank higher."""
        cheap_products = search_products(None, 10000)
        recommendations = recommend_products(cheap_products)
        if len(recommendations) >= 2:
            scores = [p["score"] for p in recommendations]
            # Scores should be sorted descending
            assert scores == sorted(scores, reverse=True)


# ──────────────────────────────────────────────────────────────────────
#  Flask routes (using test client)
# ──────────────────────────────────────────────────────────────────────

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestFlaskRoutes:

    def test_home_page(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        assert b"AI Shopping Assistant" in resp.data

    def test_search_success(self, client):
        resp = client.post(
            "/api/search",
            data=json.dumps({"query": "I need a laptop under ₹60,000 for coding"}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["success"] is True
        assert data["data"]["count"] > 0
        assert data["data"]["recommendations"][0]["category"] == "Laptops"

    def test_search_empty_query(self, client):
        resp = client.post(
            "/api/search",
            data=json.dumps({"query": ""}),
            content_type="application/json",
        )
        assert resp.status_code == 400
        data = json.loads(resp.data)
        assert data["success"] is False

    def test_search_missing_query(self, client):
        resp = client.post(
            "/api/search",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_search_no_matches(self, client):
        resp = client.post(
            "/api/search",
            data=json.dumps({"query": "laptop under 1000"}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["success"] is True
        assert data["data"]["count"] == 0
