import plotly.express as px
import pandas as pd
import datetime
import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash import Dash, html, dcc




df=pd.read_csv('climate.csv')

df=df.dropna()

df.head()

df.info()

df_september = df[df['date'] >= str(datetime.date(2023,9,1))]
df_september

# Remove the quotes around city names
df['city'] = df['city'].str.strip('"')
df['region'] = df['region'].str.strip('"')
df['country'] = df['country'].str.strip('"')

df.head()

fig_bar = px.bar(df_september[df_september['city'].isin(['Helsinki', 'Amsterdam', 'Tirana'])], 
             x='date', 
             y='avg_temp',  
             color='country',
             barmode='group',
             height=400)

fig_bar.write_html("bar_side.html")

graph5 = dcc.Graph(figure=fig_bar)

df['country'].unique()

df_finland = df[df['city'] == 'Helsinki']
df_finland = df_finland.sort_values(by='date')
df_finland

#line chart

fig = px.line(df_finland, x='date', y='avg_temp', height=500, title="Average Temperature", markers=False)

# Visualizing Geospatial Data with Plotly

fig_choropleth = px.choropleth(
    data_frame=df,  # Use the original DataFrame
    locations="country",
    locationmode='country names',  # Use the 'country' column directly
    color="avg_temp",  # You can choose maxtemp_c, mintemp_c, or avgtemp_c
    hover_name="country",
    projection='natural earth',
    animation_frame="date",
    title="Temperature Variation Over Time",
    color_continuous_scale=px.colors.sequential.YlOrRd,
    labels={'avg_temp': 'Average Temperature (°C)'}
)

fig_choropleth.update_geos(showcoastlines=True, coastlinecolor="Black", showland=True, landcolor="white")

graph4 = dcc.Graph(figure=fig_choropleth)

fig_scattermap = px.scatter_geo(
    df,
    lat='lat',  # Column containing latitude data
    lon='lon',  # Column containing longitude data
    text='city',  # Column containing city names (optional)
    title='Weather Station/City Locations',
    projection='winkel tripel',
)

fig_scattermap.update_geos(showcoastlines=True, coastlinecolor="Black", showland=True, landcolor="white")

# Assuming you have a specific city/station in mind, let's say "Mariehamn"
city_name = "Helsinki"

# Filter data for the specific city
city_data = df[df['city'] == city_name]

# Sort the data by date for a chronological order
city_data['date'] = pd.to_datetime(city_data['date'])
city_data = city_data.sort_values(by='date')

# Create warming stripes plot
fig_warming_stripes = px.bar(
    city_data,
    x='date',
    y='avg_temp',
    labels={'avg_temp': 'Average Temperature (°C)'},
    title=f'Warming Stripes for {city_name}',
    template="plotly_white",  # Use a white template for clearer visualization
    color='avg_temp',
    color_continuous_scale="RdYlBu_r",  # Use a red-blue color scale
)

# Customize the layout (optional)
fig_warming_stripes.update_layout(
    xaxis_title='Year',
    yaxis_title='Average Temperature (°C)',
    showlegend=False,
)

fig_warming_stripes.update_xaxes(
    showline=True, showgrid=False
)

graph1 = dcc.Graph(figure=fig_warming_stripes)

# Assuming you have a specific city/station in mind, let's say "Mariehamn"
city_name = "Tirana"

# Filter data for the specific city
city_data = df[df['city'] == city_name]

# Sort the data by date for a chronological order
city_data['date'] = pd.to_datetime(city_data['date'])
city_data = city_data.sort_values(by='date')

# Create warming stripes plot
fig_warming_stripes = px.bar(
    city_data,
    x='date',
    y='avg_temp',
    labels={'avg_temp': 'Average Temperature (°C)'},
    title=f'Warming Stripes for {city_name}',
    template="plotly_white",  # Use a white template for clearer visualization
    color='avg_temp',
    color_continuous_scale="RdYlBu_r",  # Use a red-blue color scale
)

# Customize the layout (optional)
fig_warming_stripes.update_layout(
    xaxis_title='Year',
    yaxis_title='Average Temperature (°C)',
    showlegend=False,
)

fig_warming_stripes.update_xaxes(
    showline=True, showgrid=False
)

graph2 = dcc.Graph(figure=fig_warming_stripes)

# Assuming you have a specific city/station in mind, let's say "Mariehamn"
city_name = "Amsterdam"

# Filter data for the specific city
city_data = df[df['city'] == city_name]

# Sort the data by date for a chronological order
city_data['date'] = pd.to_datetime(city_data['date'])
city_data = city_data.sort_values(by='date')

# Create warming stripes plot
fig_warming_stripes = px.bar(
    city_data,
    x='date',
    y='avg_temp',
    labels={'avg_temp': 'Average Temperature (°C)'},
    title=f'Warming Stripes for {city_name}',
    template="plotly_white",  # Use a white template for clearer visualization
    color='avg_temp',
    color_continuous_scale="RdYlBu_r",  # Use a red-blue color scale
)

# Customize the layout (optional)
fig_warming_stripes.update_layout(
    xaxis_title='Year',
    yaxis_title='Average Temperature (°C)',
    showlegend=False,
)

fig_warming_stripes.update_xaxes(
    showline=True, showgrid=False
)

graph3 = dcc.Graph(figure=fig_warming_stripes)

# Create a dash app

# Sample DataTable
d_table = dash_table.DataTable(
    df_finland.to_dict('records'),
    [{"name": i, "id": i} for i in df_finland.columns],
    style_data={'color': 'white', 'backgroundColor': 'black'},
    style_header={
        'backgroundColor': 'rgb(210, 180, 210)',
        'color': 'black',
        'fontWeight': 'lighter'
    }
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])

app.layout = html.Div([
    html.H1('Temperature Analysis Dashboard', style={'textAlign': 'center', 'color': 'green'}),
    html.H2('Welcome', style={'paddingLeft': '30px'}),
    html.H3('These are the Graphs'),
    html.Div([
        html.Div('Finland', style={'backgroundColor': 'green', 'color': 'white', 'width': "Finland"}),
        d_table,
        graph1,
        graph2,
        graph3,
        graph4,
        graph5,
        # You should define `graph1` before using it in the layout
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8052)

# Add Interactive Components to Your Dash App

from dash.dependencies import Input, Output, State

# Dropdown

dropdown = dcc.Dropdown([{'label': ['Finland', 'Albania', 'Croatia'], 'value': 'Finland'},])

# add call back and a function

@app.callback(
    Output(graph1, "figure"), 
    Input(dropdown, "value"))

def update_bar_chart(country): 
    mask = df_countries["country"] == country
    fig =px.bar(df_countries[mask], 
             x='date', 
             y='average temperature',  
             color='country',
             barmode='group',
             height=300, title = "Finland vs. Albania & Croatia")
    return fig

# Radio Items

radio= dcc.RadioItems(id="countries",options=['Finland', 'Albania', 'Croatia'], value="Finland", inline=True)

# Download Button

html.Button("Download Data", id="btn-download-txt"),dcc.Download(id="download-text")

@app.callback(
    Output("download-text", "data"),
    Input("btn-download-txt", "n_clicks"),
    prevent_initial_call=True
)


def download_table(n_clicks):
    return dict(content="Temperature Averages", filename="temperature_table.txt")