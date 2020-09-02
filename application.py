import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

print(dcc.__version__) # 0.6.0 or above is required

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

application = app.server
app.config.suppress_callback_exceptions = True
