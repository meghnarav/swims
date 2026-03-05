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
        dbc.Label("Quantity"), dbc.Input(id='m-qty', type='number', value=1, min=1),
        dbc.Label("Type"), dbc.Select(
            id='m-type',
            options=[
                {"label": "INWARD (Stock In)", "value": "INWARD"},
                {"label": "OUTWARD (Stock Out)", "value": "OUTWARD"},
            ],
            value="INWARD",
        ),
    ]),
    dbc.ModalFooter(dbc.Button("Submit", id="save-db-btn", color="primary"))
], id="modal-move", is_open=False)

# Overview tab content (KPIs + charts + inventory table)
overview_tab = html.Div([
    dbc.Row(id="kpi-row", className="mb-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(id='graph-inv'), width=7),
        dbc.Col(dcc.Graph(id='graph-trans'), width=5),
    ]),
    html.Div(id="table-inventory", className="mt-4"),
])

def crud_section(entity_name, id_prefix):
    """Reusable CRUD form + table section for simple entities."""
    return html.Div([
        html.H4(f"{entity_name} Management", className="mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Label("Name"),
                dbc.Input(id=f"{id_prefix}-name", type="text"),
            ], md=4),
            dbc.Col([
                dbc.Label("Extra 1"),
                dbc.Input(id=f"{id_prefix}-extra1", type="text"),
            ], md=4),
            dbc.Col([
                dbc.Label("Extra 2"),
                dbc.Input(id=f"{id_prefix}-extra2", type="text"),
            ], md=4),
        ], className="g-3"),
        dbc.Row([
            dbc.Col(dbc.Button("Create / Update", id=f"{id_prefix}-save", color="primary", className="mt-2")),
            dbc.Col(dbc.Button("Delete Selected", id=f"{id_prefix}-delete", color="danger", className="mt-2"), width="auto"),
            dbc.Col(html.Div(id=f"{id_prefix}-message", className="mt-3 text-success"), width="auto"),
        ], className="mt-1"),
        html.Hr(),
        dash_table.DataTable(
            id=f"{id_prefix}-table",
            columns=[],
            data=[],
            row_selectable="single",
            page_size=8,
            style_table={"overflowX": "auto"},
        ),
    ])

tabs = dcc.Tabs(id="main-tabs", value="tab-overview", children=[
    dcc.Tab(label="Overview", value="tab-overview", children=overview_tab),
    dcc.Tab(label="Products", value="tab-products", children=crud_section("Products", "prod")),
    dcc.Tab(label="Suppliers", value="tab-supp", children=crud_section("Suppliers", "supp")),
    dcc.Tab(label="Warehouses", value="tab-wh", children=crud_section("Warehouses", "wh")),
    dcc.Tab(label="Employees", value="tab-emp", children=crud_section("Employees", "emp")),
])

content = html.Div(
    [tabs],
    style={"marginLeft": "18rem", "padding": "2rem"}
)

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

# Refresh Dashboard (overview + dropdowns + CRUD tables)
@app.callback(
    [Output("kpi-row", "children"),
     Output("table-inventory", "children"),
     Output("graph-inv", "figure"),
     Output("graph-trans", "figure"),
     Output("m-prod", "options"),
     Output("m-wh", "options"),
     Output("m-emp", "options"),
     Output("prod-table", "columns"),
     Output("prod-table", "data"),
     Output("supp-table", "columns"),
     Output("supp-table", "data"),
     Output("wh-table", "columns"),
     Output("wh-table", "data"),
     Output("emp-table", "columns"),
     Output("emp-table", "data"),
     ],
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

    # CRUD tables (simple reflection of backend data)
    def table_struct(df):
        if df.empty:
            return [], []
        cols = [{"name": c, "id": c} for c in df.columns]
        return cols, df.to_dict("records")

    prod_cols, prod_data = table_struct(df_products)
    supp_cols, supp_data = table_struct(pd.DataFrame(queries.fetch_suppliers()))
    wh_cols, wh_data = table_struct(df_warehouses)
    emp_cols, emp_data = table_struct(df_employees)

    return (
        kpis,
        table_inv,
        fig_inv,
        fig_trans,
        prod_opts,
        wh_opts,
        emp_opts,
        prod_cols,
        prod_data,
        supp_cols,
        supp_data,
        wh_cols,
        wh_data,
        emp_cols,
        emp_data,
    )


# Simple create-only handlers for now; they rely on periodic refresh to update UI.
@app.callback(
    Output("prod-message", "children"),
    Input("prod-save", "n_clicks"),
    State("prod-name", "value"),
    State("prod-extra1", "value"),
    State("prod-extra2", "value"),
    prevent_initial_call=True,
)
def save_product(n, name, supplier_id, extra):
    if not n:
        return ""
    try:
        sid = int(supplier_id) if supplier_id is not None else None
    except ValueError:
        sid = None
    if not name or not sid:
        return "Product name and supplier ID are required."
    success = queries.create_product(name, sid, None, None)
    return "Saved." if success else "Failed to save."


@app.callback(
    Output("supp-message", "children"),
    Input("supp-save", "n_clicks"),
    State("supp-name", "value"),
    State("supp-extra1", "value"),
    State("supp-extra2", "value"),
    prevent_initial_call=True,
)
def save_supplier(n, name, email, phone):
    if not n:
        return ""
    if not name:
        return "Supplier name is required."
    success = queries.create_supplier(name, email, phone) is not None
    return "Saved." if success else "Failed to save."


@app.callback(
    Output("wh-message", "children"),
    Input("wh-save", "n_clicks"),
    State("wh-name", "value"),
    State("wh-extra1", "value"),
    State("wh-extra2", "value"),
    prevent_initial_call=True,
)
def save_warehouse(n, location, capacity, _unused):
    if not n:
        return ""
    cap = None
    if capacity not in (None, ""):
        try:
            cap = int(capacity)
        except ValueError:
            return "Capacity must be a number."
    if not location:
        return "Location is required."
    success = queries.create_warehouse(location, cap) is not None
    return "Saved." if success else "Failed to save."


@app.callback(
    Output("emp-message", "children"),
    Input("emp-save", "n_clicks"),
    State("emp-name", "value"),
    State("emp-extra1", "value"),
    State("emp-extra2", "value"),
    prevent_initial_call=True,
)
def save_employee(n, name, role, _unused):
    if not n:
        return ""
    if not name or not role:
        return "Name and role are required."
    success = queries.create_employee(name, role) is not None
    return "Saved." if success else "Failed to save."

# ----------------- RUN APP -----------------
if __name__ == "__main__":
    app.run(debug=True)