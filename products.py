"""
products.py
===========

A small built-in product catalogue for the shopping assistant.
No external API or database is needed — products are stored as
plain Python dictionaries in a list.

Each product has:
    id, name, category, price, rating, brand, features, description
"""

PRODUCTS = [
    # ── Laptops (4) ──────────────────────────────────────
    {
        "id": 1,
        "name": "Dell Inspiron 15 3000",
        "category": "Laptops",
        "price": 55000,
        "rating": 4.2,
        "brand": "Dell",
        "features": ["Intel Core i5", "8GB RAM", "512GB SSD", "15.6 inch"],
        "description": "Reliable laptop with Intel Core i5 processor, perfect for coding and everyday productivity.",
    },
    {
        "id": 2,
        "name": "HP Pavilion 15 EG",
        "category": "Laptops",
        "price": 62000,
        "rating": 4.3,
        "brand": "HP",
        "features": ["AMD Ryzen 5", "8GB RAM", "512GB SSD", "15.6 inch"],
        "description": "AMD Ryzen 5 laptop with a comfortable keyboard, great for programming and light gaming.",
    },
    {
        "id": 3,
        "name": "Lenovo IdeaPad Slim 3",
        "category": "Laptops",
        "price": 45000,
        "rating": 4.0,
        "brand": "Lenovo",
        "features": ["AMD Ryzen 3", "8GB RAM", "256GB SSD", "15.6 inch"],
        "description": "Budget-friendly laptop ideal for students and first-time coders.",
    },
    {
        "id": 4,
        "name": "Apple MacBook Air M2",
        "category": "Laptops",
        "price": 110000,
        "rating": 4.8,
        "brand": "Apple",
        "features": ["M2 Chip", "8GB RAM", "256GB SSD", "13.6 inch"],
        "description": "Ultra-slim laptop with Apple M2 chip, excellent battery life, and a premium build for professional developers.",
    },

    # ── Smartphones (4) ───────────────────────────────────
    {
        "id": 5,
        "name": "Xiaomi Redmi Note 13 Pro",
        "category": "Smartphones",
        "price": 24000,
        "rating": 4.4,
        "brand": "Xiaomi",
        "features": ["Snapdragon 7 Gen 3", "256GB", "200MP Camera", "5G"],
        "description": "Affordable phone with an excellent 200MP camera and 5G support.",
    },
    {
        "id": 6,
        "name": "Samsung Galaxy S24",
        "category": "Smartphones",
        "price": 100000,
        "rating": 4.5,
        "brand": "Samsung",
        "features": ["Snapdragon 8 Gen 3", "128GB", "50MP Camera", "5G"],
        "description": "Flagship phone with top-tier performance and a stunning AMOLED display.",
    },
    {
        "id": 7,
        "name": "Apple iPhone 15 Pro",
        "category": "Smartphones",
        "price": 130000,
        "rating": 4.7,
        "brand": "Apple",
        "features": ["A17 Pro Chip", "128GB", "Triple Camera", "5G"],
        "description": "Premium iPhone with the fastest chip, perfect for creators and power users.",
    },
    {
        "id": 8,
        "name": "Google Pixel 8",
        "category": "Smartphones",
        "price": 70000,
        "rating": 4.3,
        "brand": "Google",
        "features": ["Google Tensor G3", "256GB", "AI Camera", "5G"],
        "description": "Clean Android experience with outstanding AI-powered camera features.",
    },

    # ── Headphones (4) ────────────────────────────────────
    {
        "id": 9,
        "name": "Sony WH-1000XM5",
        "category": "Headphones",
        "price": 30000,
        "rating": 4.9,
        "brand": "Sony",
        "features": ["Noise Cancelling", "30h Battery", "Bluetooth", "Foldable"],
        "description": "Industry-leading noise cancelling headphones with 30-hour battery life and premium sound.",
    },
    {
        "id": 10,
        "name": "JBL Tune 510BT",
        "category": "Headphones",
        "price": 8000,
        "rating": 4.2,
        "brand": "JBL",
        "features": ["Wireless", "70h Battery", "Pure Bass", "Foldable"],
        "description": "Affordable wireless headphones with an incredible 70-hour battery life.",
    },
    {
        "id": 11,
        "name": "Bose QuietComfort 45",
        "category": "Headphones",
        "price": 32000,
        "rating": 4.8,
        "brand": "Bose",
        "features": ["Noise Cancelling", "24h Battery", "Bluetooth", "Comfortable"],
        "description": "Legendary noise cancellation and comfort for long listening sessions.",
    },
    {
        "id": 12,
        "name": "Apple AirPods Max",
        "category": "Headphones",
        "price": 52000,
        "rating": 4.7,
        "brand": "Apple",
        "features": ["Noise Cancelling", "Spatial Audio", "Over-ear", "High-Fidelity"],
        "description": "Premium over-ear wireless headphones with spatial audio and active noise cancellation.",
    },

    # ── Smartwatches (3) ─────────────────────────────────
    {
        "id": 13,
        "name": "Apple Watch Series 9",
        "category": "Smartwatches",
        "price": 45000,
        "rating": 4.7,
        "brand": "Apple",
        "features": ["Always-On Display", "ECG", "Waterproof", "iPhone Integration"],
        "description": "Latest Apple Watch with advanced health sensors and seamless iPhone pairing.",
    },
    {
        "id": 14,
        "name": "Samsung Galaxy Watch 6",
        "category": "Smartwatches",
        "price": 30000,
        "rating": 4.4,
        "brand": "Samsung",
        "features": ["Body Composition", "ECG", "Sleep Tracking", "Android Integration"],
        "description": "Comprehensive health tracking with body composition analysis and ECG monitoring.",
    },
    {
        "id": 15,
        "name": "Fitbit Charge 6",
        "category": "Smartwatches",
        "price": 18000,
        "rating": 4.3,
        "brand": "Fitbit",
        "features": ["Fitness Tracking", "20d Battery", "Stress Management", "Waterproof"],
        "description": "Fitness-focused tracker with 20-day battery life and stress management tools.",
    },
]


def get_all_products():
    """Return the full list of products."""
    return PRODUCTS


def get_categories():
    """Return a list of unique product categories."""
    return sorted(set(p["category"] for p in PRODUCTS))
