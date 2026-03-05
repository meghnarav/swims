import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from dash import html, dash_table, dcc
import plotly.express as px

from backend import queries

# Fetch data
products = queries.fetch_products()
suppliers = queries.fetch_suppliers()
inventory = queries.fetch_inventory()
transactions = queries.fetch_stock_transactions()

# Convert to DataFrame
products_df = pd.DataFrame(products)
suppliers_df = pd.DataFrame(suppliers)
inventory_df = pd.DataFrame(inventory)
transactions_df = pd.DataFrame(transactions)

# ======================
# KPI METRICS
# ======================

total_products = len(products_df)
total_suppliers = len(suppliers_df)
total_inventory = inventory_df["quantity"].sum() if not inventory_df.empty else 0
total_transactions = len(transactions_df)

# ======================
# CHARTS
# ======================

if not inventory_df.empty:
    inventory_chart = px.bar(
        inventory_df,
        x="location",
        y="quantity",
        color="product_name",
        title="Inventory by Warehouse"
    )
else:
    inventory_chart = {}

if not transactions_df.empty:
    transaction_chart = px.histogram(
        transactions_df,
        x="transaction_type",
        title="Stock Transactions"
    )
else:
    transaction_chart = {}

# ======================
# TABLE GENERATOR
# ======================

def create_table(df):

    if df.empty:
        return html.Div("No Data Available")

    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        page_size=10,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left", "padding": "5px"},
        style_header={"fontWeight": "bold"}
    )

products_table = create_table(products_df)
suppliers_table = create_table(suppliers_df)
inventory_table = create_table(inventory_df)
transactions_table = create_table(transactions_df)

# ======================
# KPI CARDS
# ======================

kpi_cards = html.Div([

    html.Div([
        html.H4("Products"),
        html.H2(total_products)
    ], style={"border":"1px solid #ddd","padding":"20px","width":"200px"}),

    html.Div([
        html.H4("Suppliers"),
        html.H2(total_suppliers)
    ], style={"border":"1px solid #ddd","padding":"20px","width":"200px"}),

    html.Div([
        html.H4("Inventory Units"),
        html.H2(total_inventory)
    ], style={"border":"1px solid #ddd","padding":"20px","width":"200px"}),

    html.Div([
        html.H4("Transactions"),
        html.H2(total_transactions)
    ], style={"border":"1px solid #ddd","padding":"20px","width":"200px"}),

], style={
    "display":"flex",
    "gap":"30px",
    "marginBottom":"40px"
})

# ======================
# FINAL LAYOUT
# ======================

layout = html.Div([

    html.H1("SWIMS Inventory Dashboard"),

    kpi_cards,

    html.H2("Analytics"),

    html.Div([
        dcc.Graph(figure=inventory_chart),
        dcc.Graph(figure=transaction_chart)
    ], style={"display":"flex","gap":"40px"}),

    html.H2("Products"),
    products_table,

    html.H2("Suppliers"),
    suppliers_table,

    html.H2("Inventory"),
    inventory_table,

    html.H2("Stock Transactions"),
    transactions_table

], style={"margin":"40px"})