# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import math

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
rounded_max_payload = math.ceil(max_payload / 1000) * 1000
print('max_payload ', math.ceil(max_payload / 1000) * 1000, 'min_payload ', min_payload)

# Create a dash application
app = dash.Dash(__name__)

site_options = [
    {'label': 'All Sites', 'value': 'ALL'},
]

for element in spacex_df['Launch Site'].unique():
    d = {'label': element, 'value': element}
    site_options.append(d)

mark_options = {}

for element in range(int(min_payload), int(rounded_max_payload)+1, int(rounded_max_payload/4)):
    mark_options.update({element: str(element)})
print(mark_options)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                    options=site_options,
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),

                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=min_payload, max=rounded_max_payload, step=2500,
                                    marks=mark_options,
                                    value=[min_payload, rounded_max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class',
            names=spacex_df['Launch Site'],
            title='Total Success Launches By Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        a = spacex_df[spacex_df['Launch Site'] == entered_site]

        fig = px.pie(
            a.assign(c=1),
            # values='c',
            names='class',
            title='Total Success Launches for site ' + entered_site
        )
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'),
            Input(component_id="payload-slider", component_property="value"))

def get_scatter_chart(entered_site, slider):
    filtered_payload_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= slider[0]) & (spacex_df['Payload Mass (kg)'] <= slider[1])]
    if entered_site == 'ALL':
        fig = px.scatter(
            filtered_payload_df,
            x=filtered_payload_df['Payload Mass (kg)'],
            y=filtered_payload_df['class'],
            color="Booster Version Category",
            title="Correlation between Payload and Success for all Sites"
        )
        return fig
    else:
        # return the outcomes scatter plot for a selected site
        a = filtered_payload_df[filtered_payload_df['Launch Site'] == entered_site]

        fig = px.scatter(
            a,
            x=a['Payload Mass (kg)'],
            y=a['class'],
            color="Booster Version Category",
            title="Correlation between Payload and Success for site " + entered_site
        )
        return fig


# Run the app
if __name__ == '__main__':
    app.run()
