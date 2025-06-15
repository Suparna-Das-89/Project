import streamlit as st
import json
import difflib
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import random

# ---------- Data Handling ----------
def load_data(filepath="store_price_data.json"):
    with open(filepath, "r") as f:
        return json.load(f)

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

def match_product_name(user_input, reference_names):
    matches = difflib.get_close_matches(user_input.lower(), reference_names, n=1, cutoff=0.6)
    return matches[0] if matches else None

def compare_prices(data, product_name, country):
    country = country.lower()
    if country not in data:
        return f"❌ Country '{country}' not found. Available: {list(data.keys())}"

    all_products = list(next(iter(data[country].values())).keys())
    matched_product = match_product_name(product_name, all_products)
    if not matched_product:
        return f"❌ Product '{product_name}' not found in database. Try something else."

    result = f'''
    <div class='result-box'>
    <h3>📊 Price Comparison for: <code>{matched_product}</code> in <strong>{country.title()}</strong></h3>
    <table>
        <thead><tr><th>🏬 Store</th><th>💰 Price</th></tr></thead>
        <tbody>
    '''
    for store, prices in data[country].items():
        price = prices.get(matched_product, "❌ Not available")
        result += f"<tr><td>{store}</td><td>{price}</td></tr>"
    result += "</tbody></table></div>"
    return result

# ---------- Streamlit Config ----------
st.set_page_config(page_title="Geo-Smart PriceBot", page_icon="🛒")

# ---------- Load Data ----------
data = load_data()

# ---------- Title ----------
st.markdown("""
    <h1 style='text-align: center;'>🛍️ <span style="color:#FFD700;">Geo-Smart PriceBot</span></h1>
    <h4 style='text-align: center;'>Compare grocery prices across countries and stores!</h4>
""", unsafe_allow_html=True)

# ---------- UI Layout ----------
col1, col2 = st.columns(2)

with col1:
    country = st.selectbox("🌍 Select a country", sorted(data.keys()))

with col2:
    available_products = list(next(iter(data[country].values())).keys())
    categorized = categorize_items(available_products)

    category_emojis = {
        "Dairy": "🧀", "Grains": "🌾", "Proteins": "🍗",
        "Fruits": "🍎", "Vegetables": "🥦", "Beverages": "🥤",
        "Essentials": "🛒", "Personal Care": "🧼", "Cleaning": "🧽"
    }
    categories_display = [f"{category_emojis.get(cat, '')} {cat}" for cat in categorized.keys()]
    selected_display = st.selectbox("📦 Choose a category", categories_display)
    category = selected_display.split(" ", 1)[1]
    product = st.selectbox("🔍 Select a product", sorted(categorized[category]))

# ---------- World Map Display (Always Visible) ----------
country_coords = {
    "usa": [37.0902, -95.7129], "uk": [55.3781, -3.4360],
    "germany": [51.1657, 10.4515], "spain": [40.4637, -3.7492],
    "india": [20.5937, 78.9629], "denmark": [56.2639, 9.5018]
}
coord = country_coords.get(country.lower())
if coord:
    st.markdown("### 🗺️ Selected Country on World Map")
    map_ = folium.Map(location=[20, 0], zoom_start=2, tiles="cartodbpositron")
    folium.Marker(location=coord, tooltip=f"{country.title()}", icon=folium.Icon(color="red")).add_to(map_)
    st_folium(map_, width=800, height=450)
else:
    st.warning("📍 Map coordinates not found for selected country.")

# ---------- Trigger Comparison ----------
if st.button("Compare"):
    comparison_html = compare_prices(data, product, country)
    st.markdown(comparison_html, unsafe_allow_html=True)

    if st.checkbox("📈 Show simulated price trend"):
        dates = pd.date_range(end=pd.Timestamp.today(), periods=10)

        # Try to find a valid price from any store
        base_price = None
        for store_prices in data[country].values():
            price_str = store_prices.get(product)
            if price_str:
                try:
                    base_price = float(''.join(c for c in price_str if c.isdigit() or c == '.'))
                    break
                except ValueError:
                    continue

        if base_price:
            prices = np.random.normal(loc=base_price, scale=0.2, size=10)
            trend_df = pd.DataFrame({'Date': dates, 'Price': prices})
            st.line_chart(trend_df.set_index('Date'))
        else:
            st.warning("No valid price found to simulate trend.")

# ---------- Sidebar with Smart Tips ----------
with st.sidebar:
    st.markdown("## 💡 Smart Tip")
    st.info(random.choice([
        "💰 Prices can vary ~20% across stores — compare before you shop!",
        "📦 Use category filters to find specific items fast.",
        "🛒 You can plug in real-time APIs when needed!"
    ]))

# ---------- Footer ----------
st.markdown("---")
st.markdown("Made with ❤️ using [Streamlit](https://streamlit.io) | Hosted via PythonAnywhere")
