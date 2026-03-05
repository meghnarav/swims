from dash import Dash
from layouts import layout

app = Dash(__name__)
app.title = "SWIMS Dashboard"
app.layout = layout

if __name__ == "__main__":
    app.run_server(debug=True)