import streamlit as st
import json
import difflib

# Load data from JSON file
def load_data(filepath="store_price_data.json"):
    with open(filepath, "r") as f:
        return json.load(f)

# Group items by category
def categorize_items(products):
    categories = {
        "Dairy": ["milk", "cheese", "butter", "yogurt"],
        "Grains": ["rice", "flour", "bread", "pasta", "cereal"],
        "Proteins": ["eggs", "chicken", "beef"],
        "Fruits": ["apples", "bananas", "oranges", "tomatoes"],
        "Vegetables": ["onions", "potatoes"],
        "Beverages": ["coffee", "tea", "juice", "water"],
        "Essentials": ["sugar", "salt", "oil"],
        "Personal Care": ["soap", "shampoo", "toothpaste"],
        "Cleaning": ["detergent", "toilet paper"]
    }
    categorized = {}
    for cat, items in categories.items():
        categorized[cat] = [item for item in items if item in products]
    return categorized

# Compare prices and format result
def compare_prices(data, product_name, country):
    country = country.lower()
    if country not in data:
        return f"❌ Country '{country}' not found. Available: {list(data.keys())}"

    all_products = list(next(iter(data[country].values())).keys())
    matched_product = match_product_name(product_name, all_products)
    if not matched_product:
        return f"❌ Product '{product_name}' not found in database. Try something else."

    result = f"""
    <div class='result-box'>
    <h3>📊 Price Comparison for: <code>{matched_product}</code> in <strong>{country.title()}</strong></h3>
    <table>
        <thead><tr><th>🏬 Store</th><th>💰 Price</th></tr></thead>
        <tbody>
    """
    for store, prices in data[country].items():
        price = prices.get(matched_product, "❌ Not available")
        result += f"<tr><td>{store}</td><td>{price}</td></tr>"
    result += "</tbody></table></div>"
    return result

# Find closest match to user input
def match_product_name(user_input, reference_names):
    matches = difflib.get_close_matches(user_input.lower(), reference_names, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Streamlit App
st.set_page_config(page_title="Geo-Smart PriceBot", page_icon="🛒")

# Custom styling with fonts and animation
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }
    .stApp {
        background: linear-gradient(to right, #6dd5ed, #2193b0);
        color: white;
    }
    .main > div {
        background-color: rgba(0, 0, 0, 0.6);
        padding: 2rem;
        border-radius: 15px;
    }
    h1 span {
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% {opacity: 1;}
        50% {opacity: 0.6;}
        100% {opacity: 1;}
    }
    .result-box {
        animation: fadeIn 1s ease-in-out;
    }
    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }
    .stButton > button {
        background-color: #FFD700;
        color: black;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5em 1em;
    }
    input {
        border-radius: 10px;
        padding: 0.4em;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 1em;
    }
    th, td {
        text-align: left;
        padding: 0.5em;
        border-bottom: 1px solid #ccc;
    }
    </style>
""", unsafe_allow_html=True)

# Logo and Title


st.markdown("""
    <h1 style='text-align: center;'>🛍️ <span>Geo-Smart PriceBot</span></h1>
    <h4 style='text-align: center;'>Compare grocery prices across countries and stores!</h4>
""", unsafe_allow_html=True)

# Load data
data = load_data()

# UI layout
col1, col2 = st.columns(2)
with col1:
    country = st.selectbox("🌍 Select a country", sorted(data.keys()))
with col2:
    available_products = list(next(iter(data[country].values())).keys())
    categorized = categorize_items(available_products)
    category = st.selectbox("📦 Choose a category", list(categorized.keys()))
    product = st.selectbox("🔍 Select a product", sorted(categorized[category]))

# Trigger comparison
if st.button("Compare"):
    st.markdown(compare_prices(data, product, country), unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using [Streamlit](https://streamlit.io) | Powered by smart simulated data")
