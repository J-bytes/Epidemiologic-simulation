# -*- coding: utf-8 -*-



#========================================================================================
#Importation des modules
import dash


import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

from dash.dependencies import Input, Output
import dash_table
from flask_babel import _ ,Babel
from flask import session, redirect, url_for


import numpy as np

from prerequisite import small_world_power_law, watts_strogatz,personne#,grid_graph#!!!!! add grid_graph generator to prerequisite
from plague import epidemic
import  networkx as nx
import plotly.graph_objects as go
from modals import modals_language





#==========================================================================================
# Importation des scripts et feuille de style pour l'application
#Initialisation du serveur

external_stylesheets = [
                        'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
                        'https://wet-boew.github.io/themes-dist/GCWeb/css/theme.min.css',
                        'https://codepen.io/chriddyp/pen/bWLwgP.css',
                        'https://wet-boew.github.io/themes-dist/GCWeb/wet-boew/css/noscript.min.css']  # Link to external CSS

external_scripts = [
    'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.js',
    'https://wet-boew.github.io/themes-dist/GCWeb/wet-boew/js/wet-boew.min.js',
    'https://wet-boew.github.io/themes-dist/GCWeb/js/theme.min.js',
    'https://cdn.plot.ly/plotly-locale-de-latest.js',

]




prefixe=""

app = dash.Dash(__name__,meta_tags=[{"name": "viewport", "content": "width=device-width"}],external_stylesheets=external_stylesheets,external_scripts=external_scripts,)
server = app.server
server.config['SECRET_KEY'] = '78b81502f7e89045fe634e85d02f42c5'  # Setting up secret key to access flask session
babel = Babel(server)  # Hook flask-babel to the app



#======================================================================================
# Controls for webapp

# Dropdown options
model_options = [


    {'label': _('Small-world (watts-strogatz)'), 'value': "watts"},
    {'label': _('Small-world (connected watts-strogatz)'), 'value':  "connected-watts"},
    {'label': _('2D Grid'), 'value':    "grid"},
    {'label': _('Power Law'), 'value':    "power_law"},


   ]
#--------------------------------------------------------
#Advanced feature control
#!!!! Modifying those three element will require manual changes in grid_init,which is located inside plague.py
params_table = [
    'infectiosity', 'movements', 'mortality','proportion of population'
]



params_table_limits={'infectiosity' : [0,1],'movements' : [0,1],'mortality' : [0,1],'proportion of population' : ['%']}
Age_groups=["0-24","25-50","50+"]
df_diseases=pd.read_csv('disease_compare.csv')
Age_groups_dict={}
for (ex,p) in enumerate(params_table) :
    Age_groups_dict.update({p : ex})
#======================================================================================


# Create global chart template
mapbox_access_token = "pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w"

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Gas Concentration Overview",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",

        zoom=2,
    ),
    transition={'duration': 500},
)


#===========================================================================
# Builds the layout for the header
def build_header():
    
    return html.Div(
            [
                html.Div([], className="one column"),
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("logo_jonathan2.png"),
                            id="CSA-logo",
                            style={
                                "height": "140px",
                                "width": "auto",
                                "margin": "25px",
                            },
                            alt="Logo"
                        )
                    ],
                    className="one column",
                ),
                html.Div(
                    [
                        html.H1(
                             _("Application to visualise epidemiologic simulation"),
                            style={"margin-bottom": "10px", "margin-left": "15%"},
                           ),
                    ],
                    className="six columns",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button( _("Learn more about covid"), className="dash_button"),
                            href="",id='learn-more-link'
                        ),
                        html.A(
                            html.Button('FR', id='language-button', className="dash_button"),
                            href='/language/fr', id='language-link'
                        ),
                    ],
                    className="four columns",
                    id="button-div",
                    style={"text-align": "center"}
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        )

#===========================================================================
# Builds the layout and components for the inputs to control the simulation

cote_gauche= html.Div(
                    [
                        html.Div(
                            [
                                 html.Div(html.H3(_("Parameters of the model"))),

                                  html.Div(
                            children=[
                                html.H4(
                                    [
                                        _("Selection of the model for generating the space"),
                                        html.Img(
                                            id="show-model-modal",
                                            src="assets/question-circle-solid.svg",
                                            n_clicks=0,
                                            className="info-icon",
                                        ),
                                    ],
                                    className="container_title",
                                    style={"margin-bottom" : "0 0 0px"}
                                )],
                            id="model-div"),
                                html.Div([
                                html.Label(
                                    dcc.Dropdown(
                                        id="model_list",
                                        options= model_options,
                                        multi=False,
                                        value='connected-watts',
                                        className="dcc_control",


                                    ),
                                ),

                                 ],style={"padding-bottom": "15px"}),

                               html.Div([
                                html.Div( #connectivity parameter
                                    [
                                           html.Div(
                            children=[
                                html.H4(
                                    [
                                        _("Connectivity of the graph"),
                                        html.Img(
                                            id="show-connectivity-modal",
                                            src="assets/question-circle-solid.svg",
                                            n_clicks=0,
                                            className="info-icon",
                                        ),
                                    ],
                                     className="container_title",
                                    style={"margin_bottom" : "0px"}
                                )],
                            id="connectivity-div"),

                                       dcc.Slider(
                                            id="connectivity-parameter",

                                            value=2,

                                            min=0,
                                            max=10,
                                            marks=dict([(i,str(i)) for i in range(0,10)]),
                                            step=None,
                                        ),
                                        html.H5(
                                            "", style={"margin-top": "0px"},
                                             className="one-half column"
                                        )]


                                ),


                                html.Div( #connectivity parameter
                                    [
                                          html.Div(
                            children=[
                                html.H4(
                                    [
                                        _("Randomness of the graph"),
                                        html.Img(
                                            id="show-connectivity_node-modal",
                                            src="assets/question-circle-solid.svg",
                                            n_clicks=0,
                                            className="info-icon",
                                        ),
                                    ],
                                     className="container_title",
                                    style={"margin_bottom" : "0px"}
                                )],
                            id="connectivity_node-div"),

                                       dcc.Slider(
                                            id="max-connectivity-parameter",

                                            value=2,

                                            min=0,
                                            max=10,
                                            marks=dict([(i,str(i)) for i in range(0,10)]),
                                            step=10,
                                        ),
                                        html.H5(
                                            "", style={"margin-top": "0px"},
                                             className="one-half column"
                                        )]


                                ),


                                html.Div( #network size
                                    [
                                            html.Div(
                            children=[
                                html.H4(
                                    [
                                        _("Size of the network"),
                                        html.Img(
                                            id="show-size-modal",
                                            src="assets/question-circle-solid.svg",
                                            n_clicks=0,
                                            className="info-icon",
                                        ),
                                    ],
                                     className="container_title",
                                    style={"margin_bottom" : "0 0 0px"}

                                )],
                            id="size-div"),

                                        dcc.Slider(
                                            id="network-size",

                                            value=500,

                                            min=500,
                                            max=5000,
                                            marks=dict([(i,str(i)) for i in range(500,5500,500)]),
                                            step=None,

                                        ),
                                    ],
                                 #   className="one-half column"
                                    ),

                                 html.Div( #network size
                                    [
                                         html.Div(
                            children=[
                                html.H4(
                                    [
                                        _("Number of walker in the network"),
                                        html.Img(
                                            id="show-n_walker-modal",
                                            src="assets/question-circle-solid.svg",
                                            n_clicks=0,
                                            className="info-icon",
                                        ),
                                    ],
                                     className="container_title",
                                    style={"margin_bottom" : "0 0 0px"}

                                ),
                              ],
                            id="n_walker-div"),

                                        dcc.Slider(
                                            id="n_walkers",

                                            value=1000,

                                            min=1000,
                                            max=51000,
                                            marks=dict([(i,str(i)) for i in range(1000,56000,5000)]),
                                            step=None,

                                        ),
                                     html.Span(children=_("Selection of the range of longitude"),className="wb-inv") ],
                                 #   className="one-half column"
                                    ),

                                  html.Div( #network size
                                    [
                                         html.Div(
                            children=[
                                html.H4(
                                    [
                                        _("Number of repetition (for statistical analysis)"),
                                        html.Img(
                                            id="show-n_repetition-modal",
                                            src="assets/question-circle-solid.svg",
                                            n_clicks=0,
                                            className="info-icon",
                                        ),
                                    ],
                                     className="container_title",
                                    style={"margin_bottom" : "0 0 0px"}
                                )],
                            id="n_repetition-div"),

                                        dcc.Slider(
                                            id="repetition",

                                            value=1,

                                            min=1,
                                            max=10,
                                            marks=dict([(i,str(i)) for i in range(1,10)]),
                                            step=10,

                                        ),
                                     html.Span(children=_("Selection of the range of longitude"),className="wb-inv") ],
                                 #   className="one-half column"
                                    ),

                                html.H5(
                                    "", style={"margin-top": "0px"}
                                    ),
                            ],
                            id="map-options",
                            ), #End of map options
                                ]),


                    ],
                    id="left-column-1",
                    style={"flex-grow": 1},
                    className="six columns",
                    )






cote_droit=html.Div(
                    [
                        html.Div(   #Gas Picker
                            [

                                 html.Div(html.H3(_("Parameters of the disease"))),
                          
#                                 html.Div(
#                            children=[
#                                html.H4(
#                                    [
#                                        _("Select presets based on a specific disease"),
#                                        html.Img(
#                                            id="show-preset-modal",
#                                            src="assets/question-circle-solid.svg",
#                                            n_clicks=0,
#                                            className="info-icon",
#                                        ),
#                                    ],
#                                     className="container_title",
#                                    style={"margin_bottom" : "0 0 0px"}
#                                )],
#                            id="preset-div"),
#                                
#                                html.Div([
#                                html.Label(
#                                    dcc.Dropdown(
#                                        id="preset_list",
#                                        options= model_options,
#                                        multi=False,
#                                        value='',
#                                        className="dcc_control",
#
#
#                                    ),
#                                ),
#
#                                  ], style={"padding-bottom": "15px"}
#                                    ),

                               html.Div([
                                html.Div( #connectivity parameter
                                    [
                                        html.Div(
                            children=[
                                html.H4(
                                    [
                                        _("Infectiosity"),

                                        html.Img(
                                            id="show-infectiosity-modal",
                                            src="assets/question-circle-solid.svg",
                                            n_clicks=0,
                                            className="info-icon",
                                        ),
                                    ],
                                     className="container_title",
                                    style={"margin_bottom" : "0 0 0px"}
                                )],
                            id="infectiosity-div"),

                                       dcc.Slider(
                                            id="infectiosity-parameter",

                                            value=2,

                                            min=0,
                                            max=10,
                                            marks=dict([(i,str(i)) for i in range(0,10)]),
                                            step=10,
                                        ),
                                        html.H5(
                                            "", style={"margin-top": "0px"},
                                             className="one-half column"
                                        )]


                                ),


                                html.Div( #connectivity parameter
                                    [
                                         html.Div(
                            children=[
                                html.H4(
                                    [
                                        _("Mortality"),

                                        html.Img(
                                            id="show-mortality-modal",
                                            src="assets/question-circle-solid.svg",
                                            n_clicks=0,
                                            className="info-icon",
                                        ),
                                    ],
                                      className="container_title",
                                    style={"margin_bottom" : "0 0 0px"}
                                )],
                            id="mortality-div")
                                        ,

                                       dcc.Slider(
                                            id="mortality-parameter",

                                            value=2,

                                            min=0,
                                            max=10,
                                            marks=dict([(i,str(i)) for i in range(0,10)]),
                                            step=10,
                                        ),
                                        html.H5(
                                            "", style={"margin-top": "0px"},
                                             className="one-half column"
                                        )]


                                ),

                                 html.Div(
                                    [
                                       html.Div(
                            children=[
                                html.H4(
                                    [
                                        _("Number of person sick at iteration 0"),

                                        html.Img(
                                            id="show-n_sick-modal",
                                            src="assets/question-circle-solid.svg",
                                            n_clicks=0,
                                            className="info-icon",
                                        ),
                                    ],
                                      className="container_title",
                                    style={"margin_bottom" : "0 0 0px"}
                                )],
                            id="n_sick-div"),

                                       dcc.Slider(
                                            id="n_sick_initial",

                                            value=1,

                                            min=1,
                                            max=100,
                                            marks=dict([(i,str(i)) for i in range(1,101,10)]),
                                            step=None,
                                        ),
                                        html.H5(
                                            "", style={"margin-top": "0px"},
                                             className="one-half column"
                                        )]


                                ),

                                   html.Div(
                                    [
                                       html.Div(
                            children=[
                                html.H4(
                                    [
                                        _("Duration of the infection"),

                                        html.Img(
                                            id="show-duree-modal",
                                            src="assets/question-circle-solid.svg",
                                            n_clicks=0,
                                            className="info-icon",
                                        ),
                                    ],
                                      className="container_title",
                                    style={"margin_bottom" : "0 0 0px"}
                                )],
                            id="duree-div"),

                                       dcc.Slider(
                                            id="duree",

                                            value=5,

                                            min=5,
                                            max=25,
                                            marks=dict([(i,str(i)) for i in range(5,30,5)]),
                                            step=None,
                                        ),
                                        html.H5(
                                            "", style={"margin-top": "0px"},
                                             className="one-half column"
                                        )]


                                ),



                                html.H5(
                                    "", style={"margin-top": "0px"}
                                    ),
                            ],

                            ), #End of map options
                                ]),


                    ],
                    id="right-column-1",
                    style={"flex-grow": 1},
                    className="six columns",
                    )

modals=modals_language()



def build_filtering():
    """
    

    Returns
    -------
    TYPE : Dash html component 
        This function build the html structure of the application input section, to be later injected inside the app for more convenience.

    """
    return html.Div([
        html.Div(
            [
                html.Div(
                    [
                        html.H3( _("The application is running!")),

                    ],
                    id="info-container",
                    className="mini_container three columns",
                    style={"text-align": "center"},
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                 html.H6( _("")),
                                 html.P( _("This application allows the user to quickly see the results of simulation of epidemiology on small-world networks")),
                                 html.P( _("This application provides users the ability to alter different parameter and visualise the impact on those on the propagation of a virus throughout a community"))
                            ],
                            id="description_div",
                        ),
                    ],
                    id="description-container",
                    className="container-display mini_container nine columns",
                ),
            ],
            className="row flex-display twelve columns"
        ),

        html.Div(
            [
                html.H3(
                   id="select-data"
                ),
            ],
            style={"margin-top": "10px", "margin-left": "auto", "margin-right": "auto", "text-align": "center"},
            className="twelve columns"
        ),

        html.Div(
            [ modals,cote_gauche,cote_droit],
            className="row flex-display pretty_container twelve columns",
            style={"justify-content": "space-evenly"}
            ),
    ])





def build_advanced_filtering():
    """
    

    Returns
    -------
    TYPE : Dash html component
        This function builds the layout for the advanced features inputs by the user

    """
    return html.Div([
                html.Details(
                    
                    html.Div([
                        
                           html.H3(_("This panel let you control advanced features. Those features are experimental and I cannot garantee the results")),
                        
                        
                        
                         dcc.Checklist(
        options=[
            {'label': _("     Activate advanced features"), 'value': 'True'},
           
        ],
        id="advanced_feature_switch",
        value=[]
    ),
                         
                      

                      
                        
   html.Div( #contingency measures
                                    [
                                         html.Div(
                            children=[
                                html.H5(
                                    [
                                        _("Vary parameter based on age"),

                                        html.Img(
                                            id="show-age-modal",
                                            src="assets/question-circle-solid.svg",
                                            n_clicks=0,
                                            className="info-icon",
                                        ),
                                    ],
                                      className="container_title",
                                    style={"margin-bottom" : "1em" , "margin-top" : "2em"}
                                )],
                            id="age-div"),
                                        
                 
                                                         dash_table.DataTable(
        id='table-editing-simple',
        columns=(
            [{'id': 'Age', 'name': 'Age'}] +
            [{'id': p, 'name': p} for p in params_table]
        ),
        data=[
            dict(Age=i, **{param: 0 for param in params_table})
            for i in Age_groups
        ],
        editable=True
    ),
    #dcc.Graph(id='table-editing-simple-output')
                         
     
                                      ]


                                ),  #End of contingency measures                                   
                        
                        
   html.H6(id='validation message'),
   html.Div( #contingency measures
                                    [
                                         html.Div(
                            children=[
                                html.H5(
                                    [
                                        _("Apply contingency measures"),

                                        html.Img(
                                            id="show-contingency-modal",
                                            src="assets/question-circle-solid.svg",
                                            n_clicks=0,
                                            className="info-icon",
                                        ),
                                    ],
                                      className="container_title",
                                    style={"margin-bottom" : "1em" , "margin-top" : "2em"}
                                )],
                            id="contingency-div"),
                                        

                                                      dcc.Checklist(
                                                          
        options=[
            {'label': _("Confine sick population"), 'value': 'confine'},
            {'label': _("Restrict movement"), 'value': 'restrict'},
            {'label': _("Mask mandate and other sanitary measures"), 'value': 'masks'},
            {'label': _("Close gathering spots"), 'value': 'lockdown'},
           
        ],
        id="advanced_feature",
        value=[],
        inputStyle={"margin-right": "30px"}
    ),
                                        html.H5(
                                            "", style={"margin-top": "5px"},
                                             className="one-half column"
                                        )]


                                ),  #End of contingency measures
                        
                        
   
     html.Div( #proportion of population
              
                                    [
                                           html.Div(
                            children=[
                                html.H4(
                                    [
                                        _("Population adherence to sanitary measures ( %) "),
                                        html.Img(
                                            id="show-adherence-modal",
                                            src="assets/question-circle-solid.svg",
                                            n_clicks=0,
                                            className="info-icon",
                                        ),
                                    ],
                                     className="container_title",
                                    style={"margin_bottom" : "5px", "margin-top" : "2em"}
                                )],
                            id="adherence-div"),

                                       dcc.Slider(
                                            id="adherence-parameter",

                                            value=50,

                                            min=0,
                                            max=100,
                                            marks=dict([(i,str(i)) for i in range(0,110,10)]),
                                            step=None,
                                        )
                                       ]


                                ), # end of adherence parameter
   
   
                        
                        ])
                    
                    )
            ],
         className="pretty_container")





def build_stats():
    """
    

    Returns
    -------
    TYPE : Dash html component
         This function builds the layout for the graph and conclusion

    """
    return html.Div([
        html.Div([
                html.Div(
                    [
                    html.Div([
                        dcc.Graph(
                            id="viz_chart")
                            ]),

                    html.Div ([
                       html.P( id = "TimeS_description")
                               ]),
                    ],
                    id="vizChartContainer",
                    className="pretty_container",
                    ),
            ]),


         html.Div([
                html.Div(
                    [
                    html.Div([
                        html.P(
                            id="Conclusion")
                            ]),


                    ],
                    id="ConclusionContainer",
                    className="pretty_container",
                    ),
            ]),

        html.Div(id='none', children=[], style={'display': 'none'}), # Placeholder element to trigger translations upon page load
        ])

# Create app layout by merging the predefined layout
app.layout = html.Div(
    [
        #html.Div([""], id='gc-header'),
        html.Div(
            [
                dcc.Store(id="aggregate_data"),
                html.Div(id="output-clientside"),  # empty Div to trigger javascript file for graph resizing

                build_header(),
                build_filtering(),
                build_advanced_filtering(),
                build_stats(),
            ],
            id="mainContainer",
            style={"display": "flex", "flex-direction": "column", "margin": "auto", "width":"75%"},
        ),
        #html.Div([""], id='gc-footer'),
        html.Div(id='none2', children=[], style={'display': 'none'}), # Placeholder element to trigger translations upon page load
    ]
)




#============================================================================
 # Create show/hide callbacks for each info modal
for id in ["model", "connectivity", "connectivity_node", "size", "n_walker","mortality","n_repetition", "infectiosity", "n_sick","duree","adherence","contingency","age"]:

    @app.callback(
        [Output(f"{id}-modal", "style"), Output(f"{id}-div", "style")],
        [Input(f"show-{id}-modal", "n_clicks"), Input(f"close-{id}-modal", "n_clicks")],
    )
    def toggle_modal(n_show, n_close):
        ctx = dash.callback_context
        if ctx.triggered and ctx.triggered[0]["prop_id"].startswith("show-"):
            return {"display": "block"}, {"zIndex": 1003}
        else:
            return {"display": "none"}, {"zIndex": 0}

#=========================================================================


"""
@app.callback(
    Output('table-editing-simple-output', 'figure'),
    Input('table-editing-simple', 'data'),
    Input('table-editing-simple', 'columns'))
def display_output(rows, columns):
   
    df = pd.DataFrame(rows, columns=[c for c in params_table])
    colors=["red","blue","green"]
    return {
        'data': [{
            'type': 'parcoords',
            'dimensions': [{
                'label': col,
                'values': df[col],
                'line' : {'name' : Age_groups[Age_groups_dict[col]],
                'color' : colors[Age_groups_dict[col]]}
            } for col in params_table]
        }]
    }
"""

#=================================================================================


# Selectors -> viz chart (95% CI)
@app.callback(
    Output("viz_chart", "figure"),
    Output("validation message", "children"),
    Output("Conclusion", "children"),
  
    [

        Input("model_list", "value"),
        Input("connectivity-parameter", "value"),
      
        Input("max-connectivity-parameter", "value"),
        Input("network-size", "value"),
        
        Input("infectiosity-parameter", "value"),
        Input("mortality-parameter", "value"),

        Input("n_sick_initial", "value"),
        Input("n_walkers", "value"),
        Input("repetition", "value"),
        Input("duree", "value"),
        
        Input("advanced_feature_switch","value"),
        Input('table-editing-simple', 'data'),
        Input('table-editing-simple', 'columns'),
        Input('advanced_feature','value'),
        Input('adherence-parameter','value')


    ]
)
def make_viz_chart(model,P,C,N,P_infection,P_mortality,n_sick_original,M,repetition,duree,advanced_switch,rows,columns,advanced_feature,adherence):
    """
    

    Parameters
    ----------
    model :  string
        the name of the generator to use for the graph
    P : integer
        The probability (normalize between 0-10) that a given edge randomly changes one of its connection to a node
    C : integer
        An integer between 0 and 10 to control the number of edge each node should have at first
    N : integer
        The size of the network given by the number of node
    P_infection : integer
        the probability of getting infected when encountering a sick individual, from 0 to 10
    P_mortality : integer
        the probability of dying after the disease, from 0 to 10
    n_sick_original : integer
        The number of sick person at iteration 0
    M : integer
        The number of walkers in the network
    repetition : integer
        The number of time the simulation is repeated for statistical analysis (standard deviation and average)
    duree : integer
        The number of iteration a person stay sick before either dying or getting immune
    advanced_switch : array
        An array which will contain "True" if the checkbox is checked
    rows : Array
        An array of dictionnary containing the data for the pandas dataframe from the datatable
    columns : Array
        An array of dictionnary containing the column name for the pandas dataframe from the datatable
    advanced_feature : array
        an arry containing the keywords ["confine","restrict","masks","lockdown"] depending if the checkboxes are checked
    adherence : integer
        An integer from 0 to 100 reflecting the percentage of the population that respect the measures as defined in advanced_feture

    Returns
    -------
    fig : Dash component
        Dash component that includes the plot
        
    message : string
        A string that will be showned under the table to explain if a parameter has an unexpected value
    """

    
    #formatting basic parameter------------------------------
    P/=10
    C=int(0.3*C/10*N)#!!!!!!
    P_infection/=10
    P_mortality/=10
    
    #formatting advanced features------------------------------
    adherence/=100
    message=_("The selected parameters are within their accepted values")# default value
    if "True" in advanced_switch :
        df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
        #df.set_index('Age')
        #df.to_csv('test.csv')
        #----------------------------------------------------------------
        #let's verify the parameter selected are within their accepted value
        for c in params_table :
            
            limites=params_table_limits[c]
            if '%' in limites :
                
                if not df[c].astype(float).sum()==100 :
                    message=_(f"The {c} parameter does not sums to 100")
                    advanced_switch=[]
            else :
                minimum,maximum=limites[0],limites[1]
                for rangee in df[c].values :
                    if not minimum<=float(rangee)<=maximum :
                        message=_(f"The {c} parameter has the value {rangee} outside the permitted range {limites}")
                        advanced_switch=[]
                        
   
        #----------------------------------------------------------------
        
    
  
    
    #selection of the generator-------------------------------
    if model=="watts" :
        G=nx.Graph(nx.watts_strogatz_graph(N,C,P))
        if "lockdown" in advanced_feature :
             for i in range(0,int(N*0.2)) :
                 noeud=max(dict(G.degree()).items(), key = lambda x : x[1])[0]
                 G.remove_node(noeud)
             N-=int(0.2*N)
       

    elif model=="grid" :
        G=nx.Graph(nx.grid_2d_graph(np.sqrt(N),np.sqrt(N)))
        if "lockdown" in advanced_feature :
             for i in range(0,int(N*0.2)) :
                 noeud=max(dict(G.degree()).items(), key = lambda x : x[1])[0]
                 G.remove_node(noeud)
             N-=int(0.2*N)
       

    elif model=="power_law" :
        G=nx.Graph(nx.powerlaw_cluster_graph(N,C,P))
        if "lockdown" in advanced_feature :
             for i in range(0,int(N*0.2)) :
                 noeud=max(dict(G.degree()).items(), key = lambda x : x[1])[0]
                 G.remove_node(noeud)
             N-=int(0.2*N)
        
    else :
        G=nx.Graph(nx.generators.random_graphs.connected_watts_strogatz_graph(N,C,P))
        if "lockdown" in advanced_feature :
             for i in range(0,int(N*0.2)) :
                 noeud=max(dict(G.degree()).items(), key = lambda x : x[1])[0]
                 G.remove_node(noeud)
             N-=int(0.2*N)
        

    N=int(N)
    #we need to relabel the nodes if they were deleted!
    if "lockdown" in advanced_feature :
        dictionnary={}
        for (ex,i) in enumerate(G.nodes) :
            dictionnary.update( { i : ex } )
        
        G=nx.relabel_nodes(G,dictionnary)
        
        
    maps=nx.to_dict_of_lists(G)
    #---------------------------------------------------------
    max_iter=1000 #!!!!!! a remplacer dans le futur si necessaire
   


    
  

    liste_sick,liste_health,liste_dead=np.zeros((repetition,max_iter)),np.zeros((repetition,max_iter)),np.zeros((repetition,max_iter))
    if "True" in advanced_switch :
        r0=epidemic(M,N,n_sick_original,max_iter,duree,maps,repetition,liste_sick,liste_health,liste_dead,P_infection,P_mortality,df,columns,advanced_feature,adherence)
    else :
        r0=epidemic(M,N,n_sick_original,max_iter,duree,maps,repetition,liste_sick,liste_health,liste_dead,P_infection,P_mortality)
    

    #limit the range of iteration-------------------------------------
    try :
        limite=np.where(np.logical_or(liste_sick.mean(axis=0).round(0)<1,liste_dead.mean(axis=0).round(0)>M-1))[0][0]+1
        liste_sick,liste_health,liste_dead=liste_sick[:,0:limite],liste_health[:,0:limite],liste_dead[:,0:limite]


    except :
        limite=max_iter
        liste_sick,liste_health,liste_dead=liste_sick[:,0:limite],liste_health[:,0:limite],liste_dead[:,0:limite]


    if repetition>1 :
        repetition=0.2
    else :
        repetition=0
        
    #graphic setup-------------------------------------------------
    fig = go.Figure()
    fig.add_trace(go.Scatter(

    name="dead",
       type="scatter",

       y=np.mean(liste_dead,axis=0),

       #line_color="rgba(255,255,255,0)",
       fillcolor="rgba(255,255,255,0)",
       line={'color': 'rgb(18,99,168)'},
       connectgaps=True,
       showlegend=True,
    error_y= dict(
        type='data',
        array=np.std(liste_dead,axis=0)*repetition,
        color='purple',
        thickness=1.5,
        width=3,
    ),
    marker=dict(color='purple', size=8)
))

    fig.add_trace(go.Scatter(

    name="healthy",
       type="scatter",

       y=np.mean(liste_health,axis=0),

       #line_color="rgba(255,255,255,0)",
       fillcolor="rgba(255,255,255,0)",
       line={'color': 'rgb(18,99,168)'},
       connectgaps=True,
       showlegend=True,
    error_y=dict(
        type='data',
        array=np.std(liste_health,axis=0)*repetition,
        color='blue',
        thickness=1.5,
        width=3,
    ),
    marker=dict(color='blue', size=8)
))


    fig.add_trace(go.Scatter(

    name="sick",
       type="scatter",

       y=np.mean(liste_sick,axis=0),

       #line_color="rgba(255,255,255,0)",
       fillcolor="rgba(255,255,255,0)",
       line={'color': 'rgb(18,99,168)'},
       connectgaps=True,
       showlegend=True,
    error_y=dict(
        type='data',
        array=np.std(liste_sick,axis=0)*repetition,
        color='red',
        thickness=1.5,
        width=3,
    ),
    marker=dict(color='red', size=8)
))
    dr0 = ""
    if len(r0) > 1:
        dr0 += f"+/- {np.std(r0)}"
        r0 = np.mean(r0)
    for g in model_options :
        if g['value']==model :
            model_label=g['label']

    argument = np.argmin((df_diseases['R0'].values - r0) ** 2 + ((df_diseases['mortality'].values) - P_mortality) ** 2)

    disease_name=df_diseases['Name'].values[argument]
    disease_R0=df_diseases['R0'].values[argument]
    disease_mortality=df_diseases['mortality'].values[argument]




    conclusion=f"Using the {model_label} to generate the network, you have infected {(1-np.mean(liste_health,axis=0)[limite-1]/M)*100}% of the population leaving  {np.mean(liste_dead,axis=0)[limite-1]/M*100}% of the original " \
               f" population dead. This model estimated the R0 factor to be {r0} {dr0}. Your epidemic most closely ressemble {disease_name} which has a {disease_mortality} mortality rate" \
               f" and a r0 factor of {disease_R0} \n" \
               f"\n" \
               f" The R0 factor represent the number of person, in average, one sick person will then infect.  This number is one of the primordial " \
               f" caracteristic of a disease during an outbreak.py \n" \
               f"\n" \
               f" Interesting fact, {disease_name} is a {df_diseases['ty^pe'].values[argument]} that is spreads by {df_diseases['spread'].values[argument]} \n" \
               f"\n" \
               f"\n" \
               f"***The mortality rates for the other diseases are for healthy adults. Source : https://docs.google.com/spreadsheets/d/1kHCEWY-d9HXlWrft9jjRQ2xf6WHQlmwyrXel6wjxkW8/edit#gid=0"

    return fig,message,conclusion





@app.callback(
    [
        Output('language-button', 'children'),
        Output('language-link', 'href'),
        Output("learn-more-link", 'href')
    ],
    [Input('none2', 'children')]
)
def update_language_button(x):
    """Updates the button to switch languages
    """

    language = session['language']
    if language == 'fr':
        return 'EN', prefixe+'/language/en','' #! Le code est bizarre et fait l'inverse. à mettre pour update le lien
    else:
        return 'FR', prefixe+'/language/fr',''


@babel.localeselector
def get_locale():
    # if the user has set up the language manually it will be stored in the session,
    # so we use the locale from the user settings
    try:
        language = session['language']
    except KeyError:
        language = None
    if language is not None:
        return language
    return 'en'


@app.server.route('/language/<language>')
def set_language(language=None):
    """Sets the session language, then refreshes the page
    """
    session['language'] = language

    return redirect(url_for('/'))





if __name__ == '__main__':
     #app.run_server(debug=True)  # For development/testing

     app.run_server(debug=True, host='0.0.0.0', port=5555)  # For the server
