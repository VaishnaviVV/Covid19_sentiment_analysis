import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash
from navbar import Navbar

navw=Navbar()

# app=dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
layout=html.Div(
    [
        dbc.Jumbotron(
            [
                dbc.Container(
                    [
                        html.Div(children=
                                 [

                                     dbc.Card(
                                         [
                                             html.H1(children="Welcome"),
                                             html.P("This is a visualization dashboard of sentiment analysis of tweets from Indians during CoVid-19, built using Python, Dash and VADER"),
                                        ]),

                                     dbc.Card(
                                         [
                                            html.H1(children="About Us"),
                                            html.P("We are \'Wizards at Work\' and we love solving problems. We are a group of freshmen from Vellore Institute of Technology, Chennai, and we decided to take up this challenge primarily to learn, and to help contribute to the society by working on one of the biggest problem at hand: COVID-19. We want to help the nation understand the impacts of lockdowns on the society, and aid the government in making the right decisions by providing deeper statistical insights.\nTeam members: Narendra Omprakash, Makesh Srinivasan, Sruthi Srinivasan, and Vaishnavi V V")
                                          ])
                                     ]
                                 )
                        ]
                    )
                ]
            )
        ]
    )
