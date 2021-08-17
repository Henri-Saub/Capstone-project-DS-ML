# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
# Filtering dataframe for the needs of the callbacks operations
df1 = spacex_df.groupby(['class']).sum()
df2 = spacex_df.groupby(['Launch Site','class']).agg({'count':sum})
df3 = spacex_df['Payload Mass (kg)', 'class']
df4 = spacex_df['Launch site', 'Payload Mass (kg)', 'class'].groupby(['Launch Site'])


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    value='ALL', 
                                    options=[
                                        {'label': 'CCAFS LC-40', 'value': 'class'},
                                        {'label': 'VAFB SLC-4E', 'value': 'class'},
                                        {'label': 'KSC LC-39A', 'value': 'class'},
                                        {'label': 'ALL', 'value': 'class'}
                                    ],
                                        
                                    placeholder = 'Select a Launch Site here',
                                    searchable = True,
                                    style={'width': '90%'}
                                    ),                                
                                
                                html.Br(),                                
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                    id='my-range-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    value=[min_payload, max_payload]
                                )

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart', figure=fig)),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))

def update_chart(site_dropdown):
    if site_dropdown == ['ALL']:
        dff = df1
    else:
        dff = df2
        
        piechart = px.pie(data_frame=dff,names='class')
    
        return piechart

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value')),
               Input(component_id='payload-slider', component_property='value'))]

def update_chart(site_dropdown):
    if site_dropdown == ['ALL']:
        dff = df3
    else:
        dff = df4
        fig = px.scatter(dff, x='Payload Mass (kg)', y='Mission Outcome', color="Booster Version Category")
    
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
