import sys
import os
import pandas as pd
import dash
from dash import html, dcc, dash_table, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend import queries

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "SWIMS Management"

# Sidebar
sidebar = html.Div([
    html.H2("SWIMS", className="display-6 text-primary"),
    html.Hr(),
    dbc.Button("Log Stock Move", id="open-modal-btn", color="success", className="w-100"),
], style={"padding": "2rem", "height": "100vh", "backgroundColor": "#f8f9fa",
          "position": "fixed", "width": "16rem"})

# Modal for Stock Movement
modal = dbc.Modal([
    dbc.ModalHeader("Record Stock Movement"),
    dbc.ModalBody([
        dbc.Label("Product"), dcc.Dropdown(id='m-prod'),
        dbc.Label("Warehouse"), dcc.Dropdown(id='m-wh'),
        dbc.Label("Employee"), dcc.Dropdown(id='m-emp'),
        dbc.Label("Quantity"), dbc.Input(id='m-qty', type='number', value=1),
        dbc.Label("Type"), dbc.Select(id='m-type', options=[
            {"label": "IN", "value": "IN"}, {"label": "OUT", "value": "OUT"}], value="IN"),
    ]),
    dbc.ModalFooter(dbc.Button("Submit", id="save-db-btn", color="primary"))
], id="modal-move", is_open=False)

# Main Content
content = html.Div([
    dbc.Row(id="kpi-row", className="mb-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(id='graph-inv'), width=7),
        dbc.Col(dcc.Graph(id='graph-trans'), width=5),
    ]),
    html.Div(id="table-inventory", className="mt-4"),
], style={"marginLeft": "18rem", "padding": "2rem"})

app.layout = html.Div([sidebar, content, modal, dcc.Interval(id='refresher', interval=5000)])

# ----------------- CALLBACKS -----------------

# Toggle Modal
@app.callback(
    Output("modal-move", "is_open"),
    [Input("open-modal-btn", "n_clicks"), Input("save-db-btn", "n_clicks")],
    [State("modal-move", "is_open")]
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2: 
        return not is_open
    return is_open

# Save Data
@app.callback(
    Output("save-db-btn", "n_clicks"),  # reset n_clicks
    Input("save-db-btn", "n_clicks"),
    [State("m-prod", "value"), State("m-wh", "value"), State("m-emp", "value"),
     State("m-qty", "value"), State("m-type", "value")]
)
def handle_save(n, prod, wh, emp, qty, t_type):
    if n:
        queries.add_stock_movement(prod, wh, emp, qty, t_type)
    return 0

# Refresh Dashboard
@app.callback(
    [Output("kpi-row", "children"),
     Output("table-inventory", "children"),
     Output("graph-inv", "figure"),
     Output("graph-trans", "figure"),
     Output("m-prod", "options"),
     Output("m-wh", "options"),
     Output("m-emp", "options")],
    [Input("refresher", "n_intervals"), Input("save-db-btn", "n_clicks")]
)
def update_view(n, n_save):
    # Fetch data
    df_products = pd.DataFrame(queries.fetch_products())
    df_inventory = pd.DataFrame(queries.fetch_inventory())
    df_trans = pd.DataFrame(queries.fetch_stock_transactions())
    df_warehouses = pd.DataFrame(queries.fetch_warehouses())
    df_employees = pd.DataFrame(queries.fetch_employees())

    # Protect against empty
    if df_inventory.empty: df_inventory = pd.DataFrame(columns=['Product_name', 'Location', 'quantity'])

    # KPI Cards
    kpis = [
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Products"), html.H3(len(df_products))]))),
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Stock Units"), html.H3(df_inventory['quantity'].sum() if not df_inventory.empty else 0)]))),
    ]

    # Inventory Table
    table_inv = dash_table.DataTable(
        df_inventory.to_dict('records'),
        [{"name": i, "id": i} for i in df_inventory.columns],
        page_size=8,
        style_data_conditional=[
            {
                'if': {'filter_query': '{quantity} < 10'},
                'backgroundColor': '#FFCCCC',
                'color': 'red'
            }
        ],
        style_table={"overflowX": "auto"}
    )

    # Inventory Graph
    fig_inv = px.bar(df_inventory, x="Location", y="quantity", color="Product_name") if not df_inventory.empty else {}

    # Transaction Graph
    if not df_trans.empty:
        df_trans["Transaction_date"] = pd.to_datetime(df_trans["Transaction_date"])
        fig_trans = px.line(df_trans, x="Transaction_date", y="quantity", color="transaction_type")
    else:
        fig_trans = {}

    # Dropdown Options
    prod_opts = [{"label": r['Product_name'], "value": r['Product_id']} for r in df_products.to_dict('records')] if not df_products.empty else []
    wh_opts = [{"label": r['Location'], "value": r['warehouse_id']} for r in df_warehouses.to_dict('records')] if not df_warehouses.empty else []
    emp_opts = [{"label": r['name'], "value": r['Employee_id']} for r in df_employees.to_dict('records')] if not df_employees.empty else []

    return kpis, table_inv, fig_inv, fig_trans, prod_opts, wh_opts, emp_opts

# ----------------- RUN APP -----------------
if __name__ == "__main__":
    app.run(debug=True)