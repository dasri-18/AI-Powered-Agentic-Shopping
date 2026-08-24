# AI-Powered Agentic Shopping Assistant

## Problem Statement

Shopping online can be overwhelming. A user often knows what they need in natural language — for example, *"I need a laptop under ₹60,000 for programming"* — but has to manually search through dozens of products, compare prices, read reviews, and figure out which one suits their needs. There is a gap between how people naturally describe what they want and the structured filters that e-commerce sites require.

This project addresses that gap by building a simple AI-powered shopping assistant that understands natural-language requests, finds matching products, ranks them, and explains why each product is a good fit.

## Project Objective

Build a small, beginner-friendly web application that demonstrates how an **agentic AI workflow** can help users find and compare products using everyday language. The project is intentionally kept simple so it can be easily understood, explained, and extended — ideal for learning and internship demonstrations.

## Features

- **Natural Language Search** — Type requests like "I need a laptop under ₹60,000 for programming."
- **Automatic Category & Budget Detection** — The app identifies the product category and maximum budget from your query.
- **Product Filtering & Ranking** — Matching products are filtered and ranked by a relevance score.
- **AI-Generated Explanations** — Each recommendation comes with a short explanation of why it fits your needs.
- **Top 3 Recommendations** — Only the best matches are shown.
- **Clean, Responsive UI** — Works on desktop and mobile browsers.
- **No API Keys Required** — Works out of the box with a built-in product catalogue (15 sample products).

## Technologies Used

| Layer        | Technology      |
|--------------|-----------------|
| Backend      | Python, Flask   |
| Frontend     | HTML, CSS, JavaScript |
| Data         | Python list (in-memory) |
| Deployment   | Flask dev server |

No database, no external APIs, and no authentication are required.

## System Architecture

The application follows a simple **three-agent workflow**. Each agent is a Python function that passes its output to the next:

```
User Query
    │
    ▼
┌─────────────┐     ┌────────────┐     ┌────────────────┐
│ Agent 1     │     │ Agent 2    │     │ Agent 3        │
│ understand_ │────▶│ search_    │────▶│ recommend_     │
│ request()   │     │ products() │     │ products()     │
└─────────────┘     └────────────┘     └────────────────┘
    │                    │                    │
    ▼                    ▼                    ▼
Extract category   Filter product list   Rank & return top 3
& budget           by category & price  with score & explanation
```

1. **Agent 1 — `understand_request()`**
   Uses keyword matching and regular expressions to extract:
   - **Category** (Laptops, Smartphones, Headphones, Smartwatches)
   - **Budget** (maximum price in rupees)

2. **Agent 2 — `search_products()`**
   Filters the built-in product catalogue by the extracted category and budget.

3. **Agent 3 — `recommend_products()`**
   Ranks matching products using a simple scoring formula and returns the top 3:
   - **Rating** contributes positively (higher rating = higher score)
   - **Price** contributes negatively (lower price = higher score)
   - **Within budget** adds a small bonus

### Project Structure

```
ai-powered-agentic-shopping-assistant/
│
├── app.py                    # Flask backend + 3 agent functions
├── products.py               # Built-in product catalogue (15 products)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── templates/
│   └── index.html            # Main page template
│
└── static/
    ├── style.css             # Stylesheet
    └── script.js             # Frontend JavaScript (AJAX calls)
```

## Installation Steps

1. **Clone or download** this project folder to your computer.

2. **Install Python 3.8+** from [python.org](https://www.python.org/downloads/) if not already installed.

3. **(Optional) Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate       # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## How to Run the Project

```bash
python app.py
```

Then open your browser and visit:
```
http://127.0.0.1:5000
```

Type your request in the text box and click **Find Products**.

## Example User Queries

| Query | What the app detects |
|-------|---------------------|
| "I need a laptop under ₹60,000 for coding" | Category: Laptops, Budget: 60000 |
| "Suggest a phone under ₹25,000 with a good camera" | Category: Smartphones, Budget: 25000 |
| "I need wireless headphones for studying" | Category: Headphones, Budget: None |
| "Show me a smartwatch under 40000" | Category: Smartwatches, Budget: 40000 |
| "I want a laptop" | Category: Laptops, Budget: None |

## Screenshots

> *(Add screenshots of your running application here after launching.)*
>
> 1. **Home page** — search box and placeholder text
> 2. **Search results** — product cards with price, rating, features, and explanation
> 3. **Mobile view** — responsive layout

## Future Enhancements

- **Connect to a real product API** (e.g., Flipkart, Amazon) to show live product data.
- **Add an LLM** (OpenAI / Gemini) for more natural explanations and follow-up chat.
- **Add product comparison** — let users compare two or more products side by side.
- **Add a chat interface** — allow follow-up questions like "Which is better for gaming?"
- **Add a SQLite database** — persist products and search history.
- **Add user authentication** — save favorite products per user.
- **Add price tracking** — notify users when prices drop.

## License

This project is for educational purposes. Feel free to use and modify it.
