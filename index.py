import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from application import application
from apps import welcome,live_twitter_sentiment,live_discussion_sentiment
from navbar import Navbar
navi=Navbar()


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

application = app.server

app.layout = html.Div([
    navi,
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/' or pathname=='/welcome':
         return welcome.layout
    #elif pathname == '/dashboard':
    #     return dashboard.layout
    elif pathname == '/live_twitter_sentiment':
         return live_twitter_sentiment.layout
    elif pathname =='/live_discussion_sentiment':
         return live_discussion_sentiment.layout
    elif pathname =='/chatbot':
        return redirect('https://coronabothc.eu-gb.mybluemix.net/ui/')
    else:
        return '404'

external_stylesheets = [dbc.themes.BOOTSTRAP]

if __name__ == '__main__':
    from os import environ
    app.run_server(debug=False,host="0.0.0.0",port=environ.get("PORT", 5000),dev_tools_hot_reload= True,threaded=True)
