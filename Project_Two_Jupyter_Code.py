# Setup the Jupyter version of Dash
from jupyter_dash import JupyterDash

# Configure the necessary Python module imports for dashboard components
import dash_leaflet as dl
from dash import dcc
from dash import html
import plotly.express as px
from dash import dash_table
from dash.dependencies import Input, Output, State
import base64

# Configure OS routines
import os

# Configure the plotting routines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#########
# change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
from my_crud import MyCrud

###########################
# Data Manipulation / Model
###########################

username = "aacuser"
password = "WhoaAcuser14!"

# Connect to database via CRUD Module
db = MyCrud(username, password)

# class read method must support return of list object and accept projection json input
# sending the read method an empty document requests all documents be returned
df = pd.DataFrame.from_records(db.read({}))

# MongoDB v5+ is going to return the '_id' column and that is going to have an 
# invlaid object type of 'ObjectID' - which will cause the data_table to crash - so we remove
# it in the dataframe here. The df.drop command allows us to drop the column. If we do not set
# inplace=True - it will reeturn a new dataframe that does not contain the dropped column(s)
df.drop(columns=['_id'],inplace=True)

## Debug
# print(len(df.to_dict(orient='records')))
# print(df.columns)


#########################
# Dashboard Layout / View
#########################
app = JupyterDash(__name__)


#FIX ME Add in Grazioso Salvare’s logo
image_filename = 'logo.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

#FIX ME Place the HTML image tag in the line below into the app.layout code according to your design
#FIX ME Also remember to include a unique identifier such as your name or date
#html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))

app.layout = html.Div([
#    html.Div(id='hidden-div', style={'display':'none'}),
    html.Img(
        src='data:image/png;base64,{}'.format(encoded_image.decode()),
        style={'height': '100px', 'display': 'block', 'margin-right': 'auto', 'margin-left': 'auto'}
    ),
    html.Center(html.B(html.H2('CS-340 Dashboard - Chrysanthemum'))),
    html.Hr(),
    html.Div([
        html.Label("Select Rescue Type:"),
        dcc.Dropdown(
            id='filter-type',
            options=[
                {'label': 'Water Rescue', 'value': 'Water'},
                {'label': 'Mountain or Wilderness Rescue', 'value': 'Mountain'},
                {'label': 'Disaster or Individual Tracking', 'value': 'Disaster'},
                {'label': 'Reset Filters', 'value': 'All'}
            ],
            value='All'
        )
#FIXME Add in code for the interactive filtering options. For example, Radio buttons, drop down, checkboxes, etc.

    ]),
    html.Hr(),
    dash_table.DataTable(id='datatable-id',
                         columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns],
                         data=df.to_dict('records'),
#FIXME: Set up the features for your interactive data table to make it user-friendly for your client
#If you completed the Module Six Assignment, you can copy in the code you created here 
                         filter_action="native",
                         sort_action="native",
                         sort_mode="multi",
                         page_size=10,
                         row_selectable = 'single',
                         selected_rows = [0]
                        ),
    html.Br(),
    html.Hr(),
#This sets up the dashboard so that your chart and your geolocation chart are side-by-side
    html.Div(className='row',
         style={'display' : 'flex'},
             children=[
        html.Div(
            id='graph-id',
            className='col s12 m6',

            ),
        html.Div(
            id='map-id',
            className='col s12 m6',
            )
        ])
])

#############################################
# Interaction Between Components / Controller
#############################################

    
@app.callback(Output('datatable-id','data'),
              [Input('filter-type', 'value')])
def update_dashboard(filter_type):
## FIX ME Add code to filter interactive data table with MongoDB queries
#
#        
#        columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]
#        data=df.to_dict('records')
#       
#       
#        return (data,columns)
    global df
    if filter_type == 'All':
        data = db.read({})
    
    elif filter_type == 'Water':
        data = db.read({
            "animal_type": "Dog", 
            "breed": {"$regex": "^Labrador Retriever Mix|Chesapeake Bay Retriever|Newfoundland", "$options": "i"},
            "age_upon_outcome_in_weeks": {
                "$gte": 26,
                "$lte": 156
            },
            "sex_upon_outcome": "Intact Female",
            "outcome_type": {"$ne": "Euthanasia"}
        })
    
    elif filter_type == 'Mountain':
        data = db.read({
            "animal_type": "Dog", 
            "breed": {"$regex": "^(German Shepherd|Alaskan malamute|Old English Shepdog|Siberian Husky|Rottweiler)", "$options": "i"},
            "age_upon_outcome_in_weeks": {
                "$gte": 26,
                "$lte": 156
            },
            "sex_upon_outcome": "Intact Male",
            "outcome_type": {"$ne": "Euthanasia"}
        })
        
    elif filter_type == 'Disaster':
        data = db.read({
            "animal_type": "Dog", 
            "breed": {"$regex": "^(Doberman Pinsher|German Shepherd|Golden Retriever|Bloodhound|Rottweiler)", "$options": "i"},
            "age_upon_outcome_in_weeks": {
                "$gte": 20,
                "$lte": 300
            },
            "sex_upon_outcome": "Intact Male",
            "outcome_type": {"$ne": "Euthanasia"}
        })
        
    else:
        data = db.read({})
    
    df = pd.DataFrame.from_records(data)
    if '_id' in df.columns:
        df.drop(columns=['_id'], inplace=True)
    
    return df.to_dict('records')
# Display the breeds of animal based on quantity represented in
# the data table
@app.callback(
   Output('graph-id', "children"),
   [Input('datatable-id', "derived_virtual_data")])
def update_graphs(viewData):
    ###FIX ME ####
    # add code for chart of your choice (e.g. pie chart) #
    global df
    dff = df
    
    # Count the occurrences
    breed_counts = dff['breed'].value_counts()
    
    # Create a pie chart from the counts
    fig = px.pie(
        names = breed_counts.index,
        values = breed_counts.values,
        title = 'Breed Distribution'
    )
    
    return [
        dcc.Graph(
            figure = fig
        )
    ]
    
#This callback will highlight a cell on the data table when the user selects it
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]


# This callback will update the geo-location chart for the selected data entry
# derived_virtual_data will be the set of data available from the datatable in the form of 
# a dictionary.
# derived_virtual_selected_rows will be the selected row(s) in the table in the form of
# a list. For this application, we are only permitting single row selection so there is only
# one value in the list.
# The iloc method allows for a row, column notation to pull data from the datatable

@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),
     Input('datatable-id', "derived_virtual_selected_rows")])
def update_map(viewData, index):
#FIXME Add in the code for your geolocation chart
    global df
    dff = df
    # Because we only allow single row selection, the list can be converted to a row index
    if index is None or len(index) == 0:
        row = 0
    else:
        row = index[0]
    
    # Ausin TX is at [30.75, -97.48]
    return [
        dl.Map(style={'width': '800px', 'height': '400px'},
              center=[30.75,-97.48], zoom=10, children=[
                  dl.TileLayer(id='base-layer-id'),
                  dl.Marker(position=[dff.iloc[row,13],dff.iloc[row,14]],
                           children=[
                               dl.Tooltip(dff.iloc[row,4]),
                               dl.Popup([
                                   html.H1("Animal Name"),
                                   html.P(dff.iloc[row,9])
                               ])
                           ])
              ])
    ]


app.run_server(debug=True)
