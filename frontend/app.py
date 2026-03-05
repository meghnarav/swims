import sys
import os
import pandas as pd
import dash
from dash import html, dcc, dash_table, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend import queries

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "SWIMS Management"

# UI Components
sidebar = html.Div([
    html.H2("SWIMS", className="display-6 text-primary"),
    html.Hr(),
    dbc.Button("Log Stock Move", id="open-modal-btn", color="success", className="w-100"),
], style={"padding": "2rem", "height": "100vh", "backgroundColor": "#f8f9fa", "position": "fixed", "width": "16rem"})

modal = dbc.Modal([
    dbc.ModalHeader("Record Stock Movement"),
    dbc.ModalBody([
        dbc.Label("Product"), dcc.Dropdown(id='m-prod'),
        dbc.Label("Warehouse"), dcc.Dropdown(id='m-wh'),
        dbc.Label("Employee"), dcc.Dropdown(id='m-emp'),
        dbc.Label("Quantity"), dbc.Input(id='m-qty', type='number', value=1),
        dbc.Label("Type"), dbc.Select(id='m-type', options=[{"label": "IN", "value": "IN"}, {"label": "OUT", "value": "OUT"}], value="IN"),
    ]),
    dbc.ModalFooter(dbc.Button("Submit", id="save-db-btn", color="primary"))
], id="modal-move", is_open=False)

content = html.Div([
    dbc.Row(id="kpi-row", className="mb-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(id='graph-inv'), width=7),
        dbc.Col(dcc.Graph(id='graph-trans'), width=5),
    ]),
    html.Div(id="table-inventory", className="mt-4"),
], style={"marginLeft": "18rem", "padding": "2rem"})

app.layout = html.Div([sidebar, content, modal, dcc.Interval(id='refresher', interval=5000)])

# Toggle Modal
@app.callback(
    Output("modal-move", "is_open"),
    [Input("open-modal-btn", "n_clicks"), Input("save-db-btn", "n_clicks")],
    [State("modal-move", "is_open")]
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2: return not is_open
    return is_open

# Save Data
@app.callback(
    Output("save-db-btn", "n_clicks"), # Reset n_clicks
    Input("save-db-btn", "n_clicks"),
    [State("m-prod", "value"), State("m-wh", "value"), State("m-emp", "value"), 
     State("m-qty", "value"), State("m-type", "value")]
)
def handle_save(n, p, w, e, q, t):
    if n:
        queries.add_stock_movement(p, w, e, q, t)
    return 0

# Refresh View
@app.callback(
    [Output("kpi-row", "children"), Output("table-inventory", "children"),
     Output("graph-inv", "figure"), Output("graph-trans", "figure"),
     Output("m-prod", "options"), Output("m-wh", "options"), Output("m-emp", "options")],
    [Input("refresher", "n_intervals"), Input("save-db-btn", "n_clicks")]
)
def update_view(n, n_save):
    # Fetch
    df_p = pd.DataFrame(queries.fetch_products())
    df_i = pd.DataFrame(queries.fetch_inventory())
    df_t = pd.DataFrame(queries.fetch_stock_transactions())
    df_w = pd.DataFrame(queries.fetch_warehouses())
    df_e = pd.DataFrame(queries.fetch_employees())

    # Protect against empty DB
    if df_i.empty: df_i = pd.DataFrame(columns=['Product_name', 'Location', 'quantity'])
    
    # KPIs
    kpis = [
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Products"), html.H3(len(df_p))]))),
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Stock Units"), html.H3(df_i['quantity'].sum() if not df_i.empty else 0)]))),
    ]

    # Table
    tbl = dash_table.DataTable(df_i.to_dict('records'), [{"name": i, "id": i} for i in df_i.columns], page_size=5)

    # Graphs
    fig_i = px.bar(df_i, x="Location", y="quantity", color="Product_name") if not df_i.empty else {}
    
    if not df_t.empty:
        df_t["Transaction_date"] = pd.to_datetime(df_t["Transaction_date"])
        fig_t = px.line(df_t, x="Transaction_date", y="quantity", color="transaction_type")
    else:
        fig_t = {}

    # Dropdowns
    opt_p = [{"label": r['Product_name'], "value": r['Product_id']} for r in df_p.to_dict('records')] if not df_p.empty else []
    opt_w = [{"label": r['Location'], "value": r['warehouse_id']} for r in df_w.to_dict('records')] if not df_w.empty else []
    opt_e = [{"label": r['name'], "value": r['Employee_id']} for r in df_e.to_dict('records')] if not df_e.empty else []

    return kpis, tbl, fig_i, fig_t, opt_p, opt_w, opt_e

if __name__ == "__main__":
    app.run(debug=True)