import dash_bootstrap_components as dbc
import dash_core_components as dcc
def Navbar():
    navbar = dbc.NavbarSimple(
           children=[

    		dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem("Welcome", href="/welcome"),
                dbc.DropdownMenuItem("Dashboard", href="/dashboard"),
                dbc.DropdownMenuItem("Live Twitter Sentiment", href="/live_twitter_sentiment"),
                dbc.DropdownMenuItem("Expert Insights",href="/live_discussion_sentiment"),
                dbc.DropdownMenuItem("CoronaBot", href="https://coronabothc.eu-gb.mybluemix.net/ui/")
            ],
            label="Menu",
        ),
              ],
           brand="Wizards at Work",
           color="primary",
           )
    return navbar
