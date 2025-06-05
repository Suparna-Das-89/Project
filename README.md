# Geo-Smart PriceBot

Geo-Smart PriceBot is an interactive Streamlit chatbot app that lets users compare simulated grocery prices across multiple countries and supermarkets. Ask natural-language questions like:

-- Compare milk in India  
-- What's the price of eggs in Germany?  
-- Find cheapest oil in USA
It uses fuzzy matching to handle spelling or singular/plural variations, and displays results in a beautiful, responsive layout.

#  Supported Countries & Stores

Currently comparing simulated prices across 6 countries, each with 3 popular stores and 30 common products:

🇺🇸 USA: Amazon.com, Walmart, Target
🇬🇧 UK: Tesco, Sainsbury's, Asda
🇩🇪 Germany: Lidl, Aldi, Edeka
🇪🇸 Spain: Mercadona, Carrefour, Dia
🇮🇳 India: BigBasket, JioMart, Reliance Fresh
🇩🇰 Denmark: Netto, Føtex, Bilka

# Features

-- Chat-style input with natural-language parsing
-- Fuzzy matching for product name variations (e.g., egg vs. eggs)
-- Side-by-side comparison of store prices
-- Custom UI: gradients, animations, table styling, and logo
-- Lightweight: no database or API needed — powered by a store_price_data.json file
-- (Optional): Daily price updates via PythonAnywhere scheduler

# Installation & Run Locally

-- Installed and ran locally first.

# Deploy on Streamlit Cloud

Pushed my project (with app.py, store_price_data.json, and requirements.txt) to GitHub and deployed on Streamlit cloud.

# Corresponding link to the app

https://project-hbh5unscnnzsnwik2yyn65.streamlit.app
