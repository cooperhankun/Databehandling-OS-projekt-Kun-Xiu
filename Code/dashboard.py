import pandas as pd
from dash import dcc, html
import dash
from dash.dependencies import Output, Input
import plotly_express as px
import seaborn as sns
import dash_bootstrap_components as dbc
from SportFig import SportFig

# Data cleaning:
players_os = pd.read_csv("C:/Users/Kun/Documents/GitHub/Databehandling-OS-projekt-Kun-Xiu/Data/athlete_events.csv")
os_medal_event = players_os.drop_duplicates(subset=["Event", "Year", "Medal"]) 

# China team data collections:
China_team = players_os[players_os["Team"] == "China"]
China_medal = China_team.drop_duplicates(subset=["Event", "Year", "Medal"])
China_most_gold = pd.DataFrame(China_medal["Sport"][China_medal["Medal"] == "Gold"].value_counts().head(10))
China_most_medal = China_medal.dropna(subset=['Medal'])
China_most_medal = pd.DataFrame(China_most_medal.Sport.value_counts().head(10))
china_medal_year = China_medal.groupby(["Year"]).count().reset_index()
most_gold_China = China_team[["Name", "Sport"]][China_team["Medal"] == "Gold"].value_counts().head(10)
most_gold_China = pd.DataFrame(most_gold_China.sort_values(ascending=False).reset_index())
china_age = China_team[["Age", "Sex"]].reset_index()

# Sports statistic data collections:
sport_evelution = players_os.groupby(["City", "Year","Season"]).Sport.nunique().reset_index()

os_sport_medal = os_medal_event[["Sex", "NOC", "Team", "Age", "Sport", "Medal"]]
os_sport_medal = os_sport_medal.dropna() 

football = SportFig(os_sport_medal, "Football")
Swimming = SportFig(os_sport_medal, "Swimming")
Ice_Hockey = SportFig(os_sport_medal, "Ice Hockey")

# ------------------------------------------------------------------------------------------------------

china_dict = dict(Medal="Medal", Gold="Gold", Players="Players", Age="Age")
china_options_dropdown = [{"label": name, "value": symbol}
                          for symbol, name in china_dict.items()]

options_dict =dict(Gender="Gender", Country="Country", Age="Age")
attributes_options_dropdown = [{"label": name, "value": symbol}
                          for symbol, name in options_dict.items()]

#------------------------------------------------------------------------------------------------------- China team
stylesheets = [dbc.themes.MATERIAL]
app = dash.Dash(__name__, external_stylesheets=stylesheets,
                meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0")])

app.layout = dbc.Container([
    html.Div([
    html.H1('OS Dashboard', style={'textAlign': 'center', 'color':'#87CEEB'})]),

    dbc.Row([
        dbc.Card([
        dbc.CardBody(html.H4("China-team",
                             className="card-text", style={'color':'green'})
                )], className="mb-2"),

        dbc.Col(html.P("Choose a option for China team: "), className="mt-1", style={'color':'grey'},
                lg="4", xl={"size": 6, "offset": 0.5}),
            ], className="mt-4"),

    dbc.Col(
        dcc.Dropdown(id='china-dropdown', className='',
                        options=china_options_dropdown,
                        value= "Medal"), lg="4", xl="3"),

    dbc.Row([
        dbc.Col(
                dcc.Graph(id='china-graph', className=''))
            ]),

#------------------------------------------------------------------------------------------------------- sport statistic
    dbc.Row(
        dbc.Card([
        dbc.CardBody(html.H4("Sports-statistic",
                             className="card-text", style={'color':'green'}))], className="mb-2"),
           ),
        
    dbc.Row([    
        dcc.Graph(id='sports-history-graph', className=''),
        dcc.Slider(id='year-slider', className='',
                           min=1896, max=2016,
                           step=2,
                           value=1896,
                           tooltip={"placement": "bottom", "always_visible": True})
                ]),

 #-------------------------------------------------------------------------------------------------------
    
    
    
    dbc.Col(
            html.P("Choose options for a football figures: "), className="mt-1", style={'color':'grey'},
                lg="4", xl={"size": 6, "offset": 0.5}),
                
    dbc.Col(
            dcc.Dropdown(id='football-dropdown', className='',
                         options=attributes_options_dropdown,
                         value= "Gender"),lg="4", xl="3"),
    dbc.Row([
        dbc.Col(
                dcc.Graph(id='football-graph', className=''))
            ]),
            
            
    dbc.Row(
        dbc.Col(
            html.P("Choose options for a swimming figures: "), className="mt-1", style={'color':'grey'},
                lg="4", xl={"size": 6, "offset": 0.5})),
        dbc.Col(
            dcc.Dropdown(id='swimming-dropdown', className='',
                    options=attributes_options_dropdown,
                    value= "Country"),lg="4", xl="3"),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='swimming-graph', className=''))
            ]),


    dbc.Row(
        dbc.Col(
            html.P("Choose options for a Ice-Hockey figures: "), className="mt-1", style={'color':'grey'},
                lg="4", xl={"size": 6, "offset": 0.5})),
                
        dbc.Col(
            dcc.Dropdown(id='Hockey-dropdown', className='',
                    options=attributes_options_dropdown,
                    value= "Age"),lg="4", xl="3"),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='Hockey-graph', className=''))
            ]),


            
])

#--------------------------------------------------------------------------------------------------------callback
@app.callback(
    Output("china-graph", "figure"),
    Input("china-dropdown", "value"))

def update_graph(value):

    Medal= px.bar(China_most_medal, x=China_most_medal.index, y="Sport", title="Most Medal sports, China")
    Gold = px.bar(China_most_gold, x=China_most_gold.index, y="Sport", title="Most gold sports, China")
    Players = px.bar(most_gold_China, x="Name", y=0, title="Top gold gained players") 
    Age = px.histogram(china_age, x="Age", color="Sex", title="Histgram of age from China team")

    if value == "Medal":
        return Medal

    if value == "Gold":
        return Gold

    if value == "Players":
        return Players

    if value == "Age":
        return Age


@app.callback(
    Output("sports-history-graph", "figure"),
    Input("year-slider", "value"),
)

def update_graph(Year):
    Years = sport_evelution[["City","Sport","Season"]][sport_evelution["Year"] == Year]
    fig = px.scatter(Years, x="City", y="Sport", size="Sport", color="Season", title="Olympic Games Sport Count Changing Over Years")
    return fig


@app.callback(
    Output("football-graph", "figure"),
    Input("football-dropdown", "value"))

def update_graph(football_value):
    
    fig1=football.sport_gender()
    fig2=football.sport_country()
    fig3=football.sport_age()

    if football_value == "Gender":
        return fig1
    if football_value == "Country":
        return fig2
    if football_value == "Age":
        return fig3

@app.callback(
    Output("swimming-graph", "figure"),
    Input("swimming-dropdown", "value"))

def update_graph(value):

    fig1=Swimming.sport_gender()
    fig2=Swimming.sport_country()
    fig3=Swimming.sport_age()

    if value == "Gender":
        return fig1
    if value == "Country":
        return fig2
    if value == "Age":
    
        return fig3

@app.callback(
    Output("Hockey-graph", "figure"),
    Input("Hockey-dropdown", "value"))

def update_graph(value):

    fig1=Ice_Hockey.sport_gender()
    fig2=Ice_Hockey.sport_country()
    fig3=Ice_Hockey.sport_age()

    if value == "Gender":
        return fig1
    if value == "Country":
        return fig2
    if value == "Age":
        return fig3

if __name__ == "__main__":
    app.run_server(debug=True)