import dash
import dash_bootstrap_components as dbc
# from PIL import Image
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State, callback,  no_update
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output, State
# from dash import dash_table, no_update
# from dash.exceptions import PreventUpdate
# import datetime
import pandas as pd
import numpy as np
import plotly.express as px
import base64
import io
import os
from flask_caching import Cache
# from dash_bootstrap_templates import load_figure_template
import time

app = Dash(__name__,
           suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.DARKLY])

tabs_styles = {
'align-items': 'flex-start',
'margin-top': '0px',
'padding-top': '0px',
'margin-left': '0px',
    # 'float':'right',
    # "position": "fixed",
    'text-align':'left',
    'height': '3px',
    'display':'flex',
    'font-size': '20px',
    'flex-direction':'column',
    'width':'100%',
    # 'marginTop':'80px',
    'border-color':'darkblue',
    'padding': '20px'
    # 'box-sizing': 'border-box',
    # 'align-items':'stretch',
    # 'align-items': 'center'
}
tab_style = {
'align-items': 'flex-start',
'padding-top': '0px',
'margin-top': '0px',
'margin-left': '0px',
# 'float':'right',
'padding': '20px',
'height': '3px',
# "position": "fixed",
'white-space': 'nowrap',
    'flex': '1 1 auto',
# 'borderBottom': '1px solid #d6d6d6',
#     'padding': '12px',
'width':'100%',
    'textposition':'left',
    'background-color': 'darkblue',
    'font_size': '20px',
    'text-align': 'left',
    'border-color':'darkblue'
# 'flex': '1 1 auto',
    # 'border-radius': '15px',
    # 'box-shadow': '4px 4px 4px 4px lightgrey',
}

tab_selected_style = {
'align-items': 'flex-start',
'padding-top': '0px',
'margin-top': '0px',
'margin-left': '0px',
# 'float':'right',
'padding': '20px',
'height': '3px',
'text-align': 'left',
'textposition':'left',
    'font_size': '25px',
'white-space': 'nowrap',
'fontWeight': 'bold',
    'flex': '1 1 auto',
    # 'borderTop': '1px solid #d6d6d6',
    # 'borderBottom': '1px solid #d6d6d6',
'width':'100%',
    'backgroundColor': 'darkslateblue',
    'color': 'white',
    'border-color':'darkblue'
    # 'padding': '12px',
    # 'border-radius': '15px',
}

df_cp_pos = None
df_cp_neg = None
# power_plant = None

cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})

app.layout = dbc.Container([
    html.Div(
    style={'backgroundColor': ' aliceblue',
           # 'color': 'white',
           'height': '100vh', 'padding': '20px'}, children=[

    html.Div([html.H1('Power Plants Energy Generation', style={
            'textAlign': 'center',
            'color': 'white',
            'fontWeight': 'bold'
        }
                     # style={'backgroundColor':'pink'}
                     )], style={
        'backgroundColor': 'darkblue',
        'width': '1250px',
        'height': '100px',
        'position': 'fixed',
        # 'top': '0',
        # 'left': '0',
        # 'zIndex': '1000',
        'margin-bottom':'100px'
    }),

    dbc.Row([
        dbc.Col(dcc.Upload(
            id='upload-data',
            children=html.Div([
                html.A('Select Data Files')
            ]),
            style={
                # 'marginBottom':'1%',
                   'fontSize':'20px',
                'width': '15%',
                'height': '40px',
                'lineHeight': '30px',
                'borderWidth': '1px',
                'borderStyle': 'solid',
                'display': 'inline-block',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '5px',
                'backgroundColor':'white',
                'color':'darkblue',
                'fontWeight': 'bold'
            },
            multiple=True
        ),  width=18
            , style={'marginTop': '10px'}
        )

    ]),

    # dcc.Store(id='df_cp_pos_store', data={}),
    # dcc.Store(id='df_cp_neg_store', data={}),
    # dcc.Store(id='power_plant_store'),
    html.Div(id='output-data-upload'),


# {'white-space': 'nowrap',
#     'flex': '1 1 auto', 'textposition':'left','background-color': 'darkblue','font_size': '200px','text-align': 'center','border-color':'darkblue'}

    # html.Hr(style={'border': '20px solid darkblue', 'margin-bottom':'0' }),



# html.Div([html.Div([dcc.Tabs(id = "tabs-styled-with-inline", value = None, children=[
#         dcc.Tab(label='Home', value='tab-0', style = tab_style, selected_style = tab_selected_style),
#         dcc.Tab(label="Generation", value='tab-01', style = tab_style, selected_style = tab_selected_style, children=[
#             html.Div(id='subtabs-1', style={'display': 'none'}, children=[
#                 dcc.Tabs(id="subtabs-1-tabs", value=None, children=[
#                     dcc.Tab(label="Sub Tab 1.1", value='tab-1', style = tab_style, selected_style = tab_selected_style),
#                     dcc.Tab(label="Sub Tab 1.2", value='tab-2', style = tab_style, selected_style = tab_selected_style),
#                     dcc.Tab(label="Sub Tab 1.3", value='tab-3', style = tab_style, selected_style = tab_selected_style)
#                 ])
#             ])
#         ]),
#         dcc.Tab(label="Load", value='tab-02', style = tab_style, selected_style = tab_selected_style, children=[
#             html.Div(id='subtabs-2', style={'display': 'none'}, children=[
#                 dcc.Tabs(id="subtabs-2-tabs", value=None, children=[
#                     dcc.Tab(label="Sub Tab 2.1", value='tab-4', style = tab_style, selected_style = tab_selected_style),
#                     dcc.Tab(label="Sub Tab 2.2", value='tab-5', style = tab_style, selected_style = tab_selected_style),
#                     dcc.Tab(label="Sub Tab 2.3", value='tab-6', style = tab_style, selected_style = tab_selected_style)
#                 ])
#             ])
#         ])
#     ]),], ),
#
#         html.Div([
#         html.Div(id='tabs-content-inline',
#                  # style={'width': '80%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '20px', 'box-sizing': 'border-box',  'overflow': 'auto'}
#                  ),])
#     ], style={'display': 'flex', 'flex-direction': 'column',
#         'width': '100%',
#         # 'box-sizing': 'border-box',
#         # 'overflow': 'hidden',
#               },
#         # className = "row flex-display"
#     ),


    html.Div([
        html.Div([
            dcc.Tabs(id = "tabs-styled-with-inline", value = 'tab-0', children = [
                dcc.Tab(label = 'Home', value = 'tab-0', style = {
# 'textposition':'left',
'padding': '1px',
# 'margin-bottom':'0px',
'padding-left': '0 auto',
'text-align': 'left',
    'margin-left': '0 auto',
    "fontSize": "24px",
'white-space': 'nowrap',
# 'fontWeight': 'bold',
    # 'flex': '1 1 auto',
    'backgroundColor': 'darkblue',
    'color': 'white',
    'border-color':'darkblue'
}, selected_style = tab_selected_style),
                dcc.Tab(label='Avg Generation Change in', id='tab-01', value='tab-01', style={
# 'textposition':'left',
'padding': '1px',
# 'margin-bottom':'0px',
'padding-left': '0 auto',
'text-align': 'left',
'margin-left': '0 auto',
    "fontSize": "24px",
'white-space': 'nowrap',
# 'fontWeight': 'bold',
    # 'flex': '1 1 auto',
    'backgroundColor': 'darkblue',
    'color': 'white',
    'border-color':'darkblue'
}, selected_style=tab_selected_style),
                dcc.Tab(label = 'Market Areas', value = 'tab-1', style = tab_style, selected_style = tab_selected_style),
                dcc.Tab(label = 'Type of Technologies', value = 'tab-2', style = tab_style, selected_style = tab_selected_style),
                dcc.Tab(label = 'Power Plants', value = 'tab-3', style = tab_style, selected_style = tab_selected_style),
                dcc.Tab(label = 'Avg Load Change in', id='tab-02', value = 'tab-02', style = {
# 'textposition':'left',
'padding': '1px',
'padding-left': '0 auto',
'text-align': 'left',
'margin-left': '0 auto',
"fontSize": "24px",
'white-space': 'nowrap',
# 'fontWeight': 'bold',
    # 'flex': '1 1 auto',
    'backgroundColor': 'darkblue',
    'color': 'white',
    'border-color':'darkblue'
}, selected_style = tab_selected_style),
                dcc.Tab(label = 'Market Areas', value = 'tab-4', style = tab_style, selected_style = tab_selected_style),
                dcc.Tab(label = 'Type of Technologies', value = 'tab-5', style = tab_style, selected_style = tab_selected_style),
                dcc.Tab(label = 'Power Plants', value = 'tab-6', style = tab_style, selected_style = tab_selected_style),
            ], style=tabs_styles,
            ),
        ], style={'width': '10%', 'height': '90vh', 'position': 'fixed', 'backgroundColor': 'darkblue',  'padding': '5px','margin-top': '20px', 'align-items': 'flex-start', 'text-align': 'left', 'padding-top': '0px'}),

        html.Div([
        html.Div(id='tabs-content-inline',
                 # style={'width': '80%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '20px', 'box-sizing': 'border-box',  'overflow': 'auto'}
                 ),])
    ], style={'display': 'flex', 'flex-direction': 'column',
        'width': '100%', 'text-align': 'left', 'padding-top': '0px', 'align-items': 'flex-start',
        # 'box-sizing': 'border-box',
        # 'overflow': 'hidden',
              },
        # className = "row flex-display"
    ),



        #              style = tabs_styles),
        #     html.Div(id = 'tabs-content-inline')
        # ],
        #     # className = "create_container3 eight columns",
        # ),
        # ], className = "row flex-display"),

###########################
    # html.Div([
    #         dcc.Store(id='power-dropdown')
    #     ],
    #             id="hiddendata",
    #             style={"display": "none"},
    #     ),
    # html.H5('Source: TenneT TSO Database', style={'marginLeft': '350px', 'position':'right', 'color': 'darkblue','padding-bottom': '0px', 'marginBottom': '0px'}),
    html.Img(src=app.get_asset_url('Tennet_TSO_logo.png '), style={'width': '7%', 'height': 'auto', 'position': 'fixed', 'backgroundColor': 'white',
                                                                                     # 'position': 'absolute',
'top': '20px', 'right': '875px'})

        ])
], style={
            'textAlign': 'left',
        })


# @app.callback(
#     [Output('tab-01', 'style'),
#      Output('tab-02', 'style')],
#     [Input('tabs-styled-with-inline', 'value')],
#     [State('tab-01', 'style'),
#      State('tab-02', 'style')]
# )
# def toggle_subtabs(main_tab, subtab1_style, subtab2_style):
#     if main_tab == 'Generation':
#         subtab1_style = {'display': 'block'}
#         subtab2_style = {'display': 'none'}
#     elif main_tab == 'Load':
#         subtab1_style = {'display': 'none'}
#         subtab2_style = {'display': 'block'}
#     else:
#         subtab1_style = {'display': 'none'}
#         subtab2_style = {'display': 'none'}
#
#     return subtab1_style, subtab2_style




# @app.callback(Output('tab-01', 'children'),
#               Input('tabs-styled-with-inline', 'value'))
# def update_tabs(value):
#     # tab_content = None
#     # subtabs = None
#
#     # if value == 'tab-0':
#     #     return html.Div("Generatoin and Load")
#     if value == 'tab-01':
#         return html.Div([dcc.Tabs(id="subtabs1", value='tab-1', vertical=True, children=[
#             dcc.Tab(label='Market Areas', value='tab-1', style=tab_style,
#                     selected_style=tab_selected_style),
#             dcc.Tab(label='Type of Technologies', value='tab-2', style=tab_style,
#                     selected_style=tab_selected_style),
#             dcc.Tab(label='Power Plants', value='tab-3', style=tab_style,
#                     selected_style=tab_selected_style),
#         ], style={'padding': '20px',
#                   # 'margin-top': '80px'
#                   }),
#             html.Div(id='subtabs-content1')])
#
# # @app.callback(Output('tab-02', 'children'),
# #               [Input('tabs-styled-with-inline', 'value')])
# # def update_tabs(value):
#     elif value == 'tab-02':
#         return html.Div([dcc.Tabs(id="subtabs2", value='tab-4', vertical=True, children=[
#             dcc.Tab(label='Market Areas', value='tab-4', style=tab_style, selected_style=tab_selected_style),
#             dcc.Tab(label='Type of Technologies', value='tab-5', style=tab_style,
#                     selected_style=tab_selected_style),
#             dcc.Tab(label='Power Plants', value='tab-6', style=tab_style, selected_style=tab_selected_style),
#         ], style={'padding': '20px',
#                   # 'margin-top': '180px'
#                   }),
#             html.Div(id='subtabs-content2')])


@app.callback(
    # Output('subtabs-content1', 'children'),
    Output('tabs-content-inline', 'children'),
    Input('tabs-styled-with-inline', 'value')
)
@cache.memoize(timeout=1)
def render_content(tab):
    if tab == 'tab-0':
        return html.Div(

    children=[
        html.Img(
            src=app.get_asset_url('Capture2.png'),
            style={
                            'marginTop': '100px',
            'marginBottom': '5px',
            'display': 'block',
            # 'marginLeft': 'auto',
            'marginRight': 'auto',
            'maxWidth': '80%',
            'height': '1250px',
            'padding': '10px',
            'box-shadow': '4px 4px 12px black',
            'marginLeft': '330px',

            }
        ),

        html.Div(html.Div([
            html.Span('A Market Analysis for European Markets:', style={
                'display': 'block',
                'color': 'White',
                'font-size': '40px',
                'font-weight': 'bold',
                'text-align': 'left',
                # 'padding': '10px',
                # 'float': 'left',
        #             # 'marginTop': '100px',
            }),
            html.Span('Avg Change in Generation & Load (2022-2024)', style={
                'display': 'block',
                'color': 'white',
                'font-size': '40px',
                'font-weight': 'bold',
                 'text-align': 'left',
                # 'padding': '20px',
            }),
            html.Span('Mina Hosseini', style={
                'display': 'block',
                'color': 'white',
                'font-size': '30px',
                'font-weight': 'bold',
                'text-align': 'left',
                'marginTop':'20px',
                'marginBottom': '20px',
                # 'padding': '20px',
            }),
            html.Span('TenneT TSO GmbH \ ESP-MA', style={
                'display': 'block',
                'color': 'white',
                'font-size': '20px',
                'font-weight': 'bold',
                 'text-align': 'left',
                # 'padding': '40px',
            }),
            html.Span('*Special thanks to Sascha-Phillipp Salm & Mathias Herrmannsdörfer*', style={
                'display': 'block',
                'color': 'white',
                'font-size': '20px',
                'font-weight': 'bold',
                 'text-align': 'left',
                # 'padding': '20px',
            }),]),
            # 'A Market Analysis for European Market: Generation & Load',
            style={
                # 'position': 'absolute',
                # 'top': '10%',
                # 'left': '50%',
                'float':'Right',
                'width':'70%',
                'marginLeft': '730px',
                'marginTop': '0 auto',
                # 'marginBottom':'0 auto',
                'transform': 'translate(-50%, -50%)',
                'color': 'white',
                # 'fontSize': '20px',
                'fontWeight': 'bold',
                'textAlign': 'left',
                'backgroundColor': 'rgba(0, 0, 0, 0.2)',
                'padding': '0px',
                'borderRadius': '5px',
            }
        )




    ]
)



# html.Div([
#     html.Img(
#         src=app.get_asset_url('Capture2.png'),
#         style={
#             'marginTop': '100px',  # Space from the top
#             'marginBottom': '5px',  # Space from the bottom
#             'display': 'block',  # Block display to allow margin auto to work
#             # 'marginLeft': 'auto',  # Centering the image
#             'marginRight': 'auto',  # Centering the image
#             'maxWidth': '80%',  # Set a max width to avoid overflow
#             'height': '1250px',
#             'padding': '10px',
#             'box-shadow': '4px 4px 12px black',
#             'marginLeft': '330px',
#
#             # 'float': 'right',
#             # 'backgroundColor': 'lavender',
#             # 'marginTop': '100px',
#             # 'marginBottom': '5px',
#             # # 'textAlign': 'left',
#             # # 'color': colors['text'],
#             # 'border': '2px solid white',
#             # 'box-shadow': '4px 4px 12px black',
#         }
#     )
# ])
            # html.Div([
            # html.H3('This is the content for Tab 1')])
    elif tab == 'tab-1':
        return html.Div([dbc.Row([

            html.Div([
                html.Div([
                    html.Span('7K', style={
                        'display': 'block',
                        'color': 'black',
                        'font-size': '50px',
                        'font-weight': 'bold',
                        'text-align': 'center'
                    }),
                    html.Span('Deutchland', style={
                        'display': 'block',
                        'color': 'black',
                        'font-size': '40px',
                        'font-weight': 'bold',
                        'text-align':'center'
                    }),
                ], style={
                    'margin-right': '20px',
                }),

                dcc.Graph(id='bar-graph-market',
                          style={'float': 'right',
                                 'margin-bottom': '100px',
                                 'marginTop': '50px',
                                 'height': '500px',
                                 # 'textAlign': 'left',
                                 # 'color': colors['text'],
                                 'border': '2px solid black',
                                 'border-radius': '10px',
                                 'padding': '10px',
                                 'box-shadow': '4px 4px 12px black',
                                 'width': '70%',
                                 'backgroundColor': 'white',
                                 'display': 'inline-block',  'border-radius':  '10px',
                                 }, figure={'layout': {
                        'plot_bgcolor': 'white',
                        'paper_bgcolor': 'white',
                        'font': 'darkblue',

                        # "border":{"width":"2px", "color":"black"}
                    }}
                    )], style={
            'display': 'flex',
            'align-items': 'center',
            'justify-content': 'space-between',
        }),
            dcc.Dropdown(id='power-dropdown', multi=True,
                                 value=['DE00_GT02', 'DE00_GT01', 'DE00_GOTN', 'DE00_GOTO', 'DE00_GCO2', 'DE00_HCNW',
                                        'DE00_LGO1']
                                 , style={
                            'display': 'none',
                            # # 'textAlign': 'left',
                            # 'width': '70%',
                            # 'float': 'right',
                            # # 'height': '30px',
                            # # 'lineHeight': '30px',
                            # 'borderWidth': '1px',
                            # # 'borderStyle': 'dashed',
                            # 'borderRadius': '5px',
                            # 'display': 'inline-block',
                            # # 'margin': '10px',
                            # 'color': 'darkgray',
                            # 'backgroundColor': 'white'
            },

                                 ),
                dcc.Graph(id='bar-graph-market_trend',
                          style={
                              'height': '500px',
                              'width': '96%',
                              'border': '2px solid black',
                              'border-radius': '10px',
                              'box-shadow': '4px 4px 12px black',
                              'backgroundColor': 'white',
                              'display': 'block',
                              'margin': '0 auto',
                          },
                          figure={'layout': {
                              'plot_bgcolor': 'white',
                              'paper_bgcolor': 'white',
                              'font': 'darkblue',
                          }}

                          ), html.Div('Source: TenneT TSO \ ESP-MA Database', style={
                'color': 'darkblue',
                'text-align': 'left',
                'margin-top': '40px',
                'font-size': '16px'
            })
                # ]
                # )
                # ]
                # )

            ]),
        ], style={
            'float': 'right',
            'backgroundColor': 'alieceblue',
                                 'marginTop': '100px',
                                 'marginBottom': '5px',
                                 'marginLeft': '330px',
                                 'height': '1250px',
                                 # 'textAlign': 'left',
                                 # 'color': colors['text'],
                                 'border': '2px solid white',
                                 # 'border-radius': '10px',
                                 'padding': '10px',
                                 'box-shadow': '4px 4px 12px black',
    })
    elif tab == 'tab-2':
        return html.Div([dbc.Row([

            html.Div([
                html.Div([
                    html.Span('8.74K', style={
                        'display': 'block',
                        'color': 'black',
                        'font-size': '50px',
                        'font-weight': 'bold',
                        'text-align': 'center'
                    }),
                    html.Span('Combined Cycle', style={
                        'display': 'block',
                        'color': 'black',
                        'font-size': '30px',
                        'font-weight': 'bold',
                        'text-align':'center'
                    }),
                ], style={
                    'margin-right': '20px',
                }),

                dcc.Graph(id='bar-graph-market',
                          style={'float': 'right',
                                 'margin-bottom': '100px',
                                 'marginTop': '50px',
                                 'height': '500px',
                                 # 'textAlign': 'left',
                                 # 'color': colors['text'],
                                 'border': '2px solid black',
                                 'border-radius': '10px',
                                 'padding': '10px',
                                 'box-shadow': '4px 4px 12px black',
                                 'width': '70%',
                                 'backgroundColor': 'white',
                                 'display': 'inline-block',  'border-radius':  '10px',
                                 }, figure={'layout': {
                        'plot_bgcolor': 'white',
                        'paper_bgcolor': 'white',
                        'font': 'darkblue',

                        # "border":{"width":"2px", "color":"black"}
                    }}
                    )], style={
            'display': 'flex',
            'align-items': 'center',
            'justify-content': 'space-between',
        }),
            dcc.Dropdown(id='power-dropdown', multi=True,
                                 value=['DE00_GT02', 'DE00_GT01', 'DE00_GOTN', 'DE00_GOTO', 'DE00_GCO2', 'DE00_HCNW',
                                        'DE00_LGO1']
                                 , style={
                            'display': 'none',
                            # # 'textAlign': 'left',
                            # 'width': '70%',
                            # 'float': 'right',
                            # # 'height': '30px',
                            # # 'lineHeight': '30px',
                            # 'borderWidth': '1px',
                            # # 'borderStyle': 'dashed',
                            # 'borderRadius': '5px',
                            # 'display': 'inline-block',
                            # # 'margin': '10px',
                            # 'color': 'darkgray',
                            # 'backgroundColor': 'white'
            },

                                 ),
                dcc.Graph(id='bar-graph-market_trend',
                          style={
                              'height': '500px',
                              'width': '96%',
                              'border': '2px solid black',
                              'border-radius': '10px',
                              'box-shadow': '4px 4px 12px black',
                              'backgroundColor': 'white',
                              'display': 'block',
                              'margin': '0 auto',
                          },
                          figure={'layout': {
                              'plot_bgcolor': 'white',
                              'paper_bgcolor': 'white',
                              'font': 'darkblue',
                          }}

                          ), html.Div('Source: TenneT TSO \ ESP-MA Database', style={
                'color': 'darkblue',
                'text-align': 'left',
                'margin-top': '40px',
                'font-size': '16px'
            })
                # ]
                # )
                # ]
                # )

            ]),
        ], style={
            'float': 'right',
            'backgroundColor': 'alieceblue',
                                 'marginTop': '100px',
                                 'marginBottom': '5px',
                                 'marginLeft': '330px',
                                 'height': '1250px',
                                 # 'textAlign': 'left',
                                 # 'color': colors['text'],
                                 'border': '2px solid white',
                                 # 'border-radius': '10px',
                                 'padding': '10px',
                                 'box-shadow': '4px 4px 12px black',
    })
    elif tab == 'tab-3':
        return html.Div([dbc.Row([

            html.Div([
                html.Div([
                    html.Span('4.94K', style={
                        'display': 'block',
                        'color': 'black',
                        'font-size': '50px',
                        'font-weight': 'bold',
                        'text-align': 'center'
                    }),
                    html.Span('FR00_NUCL', style={
                        'display': 'block',
                        'color': 'black',
                        'font-size': '30px',
                        'font-weight': 'bold',
                        'text-align':'center'
                    }),
                ], style={
                    'margin-right': '20px',
                }),

                dcc.Graph(id='bar-graph-market',
                          style={'float': 'right',
                                 'margin-bottom': '40px',
                                 'marginTop': '20px',
                                 'height': '500px',
                                 # 'textAlign': 'left',
                                 # 'color': colors['text'],
                                 'border': '2px solid black',
                                 'border-radius': '10px',
                                 'padding': '10px',
                                 'box-shadow': '4px 4px 12px black',
                                 'width': '70%',
                                 'backgroundColor': 'white',
                                 'display': 'inline-block',  'border-radius':  '10px',
                                 }, figure={'layout': {
                        'plot_bgcolor': 'white',
                        'paper_bgcolor': 'white',
                        'font': 'darkblue',

                        # "border":{"width":"2px", "color":"black"}
                    }}
                    )], style={
            'display': 'flex',
            'align-items': 'center',
            'justify-content': 'space-between',
        }),
            dcc.Dropdown(id='power-dropdown', multi=True,
                                                           value=['DE00_GT02', 'DE00_GT01', 'DE00_GOTN', 'DE00_GOTO', 'DE00_GCO2', 'DE00_HCNW',
                                                                  'DE00_LGO1']
                         , style={
                    'margin-bottom': '2px',
                    'marginTop': '0 auto',
                    'marginLeft': '50px',
                    'padding': '10px',
                    # 'margin': '0',
                    'border': '2px solid lightblue',
                    'textAlign': 'left',
                    'width': '80%',
                    # 'float': 'right',
                    # 'height': '30px',
                    # 'lineHeight': '30px',
                    'borderWidth': '1px',
                    # # 'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    # 'display': 'inline-block',
                    # # 'margin': '10px',
                    # 'color': 'darkgray',
                    'backgroundColor': 'white'
                }),
                dcc.Graph(id='bar-graph-market_trend',
                          style={
                              'height': '500px',
                              'width': '96%',
                              'border': '2px solid black',
                              'border-radius': '10px',
                              'box-shadow': '4px 4px 12px black',
                              'backgroundColor': 'white',
                              'display': 'block',
                              'margin': '0 auto',
                          },
                          figure={'layout': {
                              'plot_bgcolor': 'white',
                              'paper_bgcolor': 'white',
                              'font': 'darkblue',
                          }}

                          ), html.Div('Source: TenneT TSO \ ESP-MA Database', style={
                'color': 'darkblue',
                'text-align': 'left',
                'margin-top': '40px',
                'font-size': '16px'
            })
                # ]
                # )
                # ]
                # )

            ]),
        ], style={
            'float': 'right',
            'backgroundColor': 'alieceblue',
                                 'marginTop': '100px',
                                 'marginBottom': '5px',
                                 'marginLeft': '330px',
                                 'height': '1250px',
                                 # 'textAlign': 'left',
                                 # 'color': colors['text'],
                                 'border': '2px solid white',
                                 # 'border-radius': '10px',
                                 'padding': '10px',
                                 'box-shadow': '4px 4px 12px black',
    })
# @app.callback(
#     Output('tabs-content-inline', 'children', allow_duplicate=True ),
#     Input('tabs-styled-with-inline', 'value'), prevent_initial_call='initial_duplicate'
# )
# def render_content1(tab):
    elif tab == 'tab-4':
        return html.Div([dbc.Row([

            html.Div([
                html.Div([
                    html.Span('10.06K', style={
                        'display': 'block',
                        'color': 'black',
                        'font-size': '50px',
                        'font-weight': 'bold',
                        'text-align': 'center'
                    }),
                    html.Span('Deutchland', style={
                        'display': 'block',
                        'color': 'black',
                        'font-size': '30px',
                        'font-weight': 'bold',
                        'text-align':'center'
                    }),
                ], style={
                    'margin-right': '20px',
                }),

                dcc.Graph(id='bar-graph-market',
                          style={'float': 'right',
                                 'margin-bottom': '100px',
                                 'marginTop': '50px',
                                 'height': '500px',
                                 # 'textAlign': 'left',
                                 # 'color': colors['text'],
                                 'border': '2px solid black',
                                 'border-radius': '10px',
                                 'padding': '10px',
                                 'box-shadow': '4px 4px 12px black',
                                 'width': '70%',
                                 'backgroundColor': 'white',
                                 'display': 'inline-block',  'border-radius':  '10px',
                                 }, figure={'layout': {
                        'plot_bgcolor': 'white',
                        'paper_bgcolor': 'white',
                        'font': 'darkblue',

                        # "border":{"width":"2px", "color":"black"}
                    }}
                    )], style={
            'display': 'flex',
            'align-items': 'center',
            'justify-content': 'space-between',
        }),
            dcc.Dropdown(id='power-dropdown', multi=True,
                                 value=['DE00_GT02', 'DE00_GT01', 'DE00_GOTN', 'DE00_GOTO', 'DE00_GCO2', 'DE00_HCNW',
                                        'DE00_LGO1']
                                 , style={
                            'display': 'none',
                            # # 'textAlign': 'left',
                            # 'width': '70%',
                            # 'float': 'right',
                            # # 'height': '30px',
                            # # 'lineHeight': '30px',
                            # 'borderWidth': '1px',
                            # # 'borderStyle': 'dashed',
                            # 'borderRadius': '5px',
                            # 'display': 'inline-block',
                            # # 'margin': '10px',
                            # 'color': 'darkgray',
                            # 'backgroundColor': 'white'
            },

                                 ),
                dcc.Graph(id='bar-graph-market_trend',
                          style={
                              'height': '500px',
                              'width': '96%',
                              'border': '2px solid black',
                              'border-radius': '10px',
                              'box-shadow': '4px 4px 12px black',
                              'backgroundColor': 'white',
                              'display': 'block',
                              'margin': '0 auto',
                          },
                          figure={'layout': {
                              'plot_bgcolor': 'white',
                              'paper_bgcolor': 'white',
                              'font': 'darkblue',
                          }}

                          ), html.Div('Source: TenneT TSO \ ESP-MA Database', style={
                'color': 'darkblue',
                'text-align': 'left',
                'margin-top': '40px',
                'font-size': '16px'
            })
                # ]
                # )
                # ]
                # )

            ]),
        ], style={
            'float': 'right',
            'backgroundColor': 'alieceblue',
                                 'marginTop': '100px',
                                 'marginBottom': '5px',
                                 'marginLeft': '330px',
                                 'height': '1250px',
                                 # 'textAlign': 'left',
                                 # 'color': colors['text'],
                                 'border': '2px solid white',
                                 # 'border-radius': '10px',
                                 'padding': '10px',
                                 'box-shadow': '4px 4px 12px black',
    })

    elif tab == 'tab-5':
        return html.Div([dbc.Row([

            html.Div([
                html.Div([
                    html.Span('8.99K', style={
                        'display': 'block',
                        'color': 'black',
                        'font-size': '50px',
                        'font-weight': 'bold',
                        'text-align': 'center'
                    }),
                    html.Span('Wind Turbine', style={
                        'display': 'block',
                        'color': 'black',
                        'font-size': '30px',
                        'font-weight': 'bold',
                        'text-align':'center'
                    }),
                ], style={
                    'margin-right': '20px',
                }),

                dcc.Graph(id='bar-graph-market',
                          style={'float': 'right',
                                 'margin-bottom': '100px',
                                 'marginTop': '50px',
                                 'height': '500px',
                                 # 'textAlign': 'left',
                                 # 'color': colors['text'],
                                 'border': '2px solid black',
                                 'border-radius': '10px',
                                 'padding': '10px',
                                 'box-shadow': '4px 4px 12px black',
                                 'width': '70%',
                                 'backgroundColor': 'white',
                                 'display': 'inline-block',  'border-radius':  '10px',
                                 }, figure={'layout': {
                        'plot_bgcolor': 'white',
                        'paper_bgcolor': 'white',
                        'font': 'darkblue',

                        # "border":{"width":"2px", "color":"black"}
                    }}
                    )], style={
            'display': 'flex',
            'align-items': 'center',
            'justify-content': 'space-between',
        }),
            dcc.Dropdown(id='power-dropdown', multi=True,
                                 value=['DE00_GT02', 'DE00_GT01', 'DE00_GOTN', 'DE00_GOTO', 'DE00_GCO2', 'DE00_HCNW',
                                        'DE00_LGO1']
                                 , style={
                            'display': 'none',
                            # # 'textAlign': 'left',
                            # 'width': '70%',
                            # 'float': 'right',
                            # # 'height': '30px',
                            # # 'lineHeight': '30px',
                            # 'borderWidth': '1px',
                            # # 'borderStyle': 'dashed',
                            # 'borderRadius': '5px',
                            # 'display': 'inline-block',
                            # # 'margin': '10px',
                            # 'color': 'darkgray',
                            # 'backgroundColor': 'white'
            },

                                 ),
                dcc.Graph(id='bar-graph-market_trend',
                          style={
                              'height': '500px',
                              'width': '96%',
                              'border': '2px solid black',
                              'border-radius': '10px',
                              'box-shadow': '4px 4px 12px black',
                              'backgroundColor': 'white',
                              'display': 'block',
                              'margin': '0 auto',
                          },
                          figure={'layout': {
                              'plot_bgcolor': 'white',
                              'paper_bgcolor': 'white',
                              'font': 'darkblue',
                          }}

                          ), html.Div('Source: TenneT TSO \ ESP-MA Database', style={
                'color': 'darkblue',
                'text-align': 'left',
                'margin-top': '40px',
                'font-size': '16px'
            })
                # ]
                # )
                # ]
                # )

            ]),
        ], style={
            'float': 'right',
            'backgroundColor': 'alieceblue',
                                 'marginTop': '100px',
                                 'marginBottom': '5px',
                                 'marginLeft': '330px',
                                 'height': '1250px',
                                 # 'textAlign': 'left',
                                 # 'color': colors['text'],
                                 'border': '2px solid white',
                                 # 'border-radius': '10px',
                                 'padding': '10px',
                                 'box-shadow': '4px 4px 12px black',
    })
    elif tab == 'tab-6':
        return html.Div([dbc.Row([

            html.Div([
                html.Div([
                    html.Span('4.94K', style={
                        'display': 'block',
                        'color': 'black',
                        'font-size': '50px',
                        'font-weight': 'bold',
                        'text-align': 'center'
                    }),
                    html.Span('FR00_NUCL', style={
                        'display': 'block',
                        'color': 'black',
                        'font-size': '30px',
                        'font-weight': 'bold',
                        'text-align':'center'
                    }),
                ], style={
                    'margin-right': '20px',
                }),

                dcc.Graph(id='bar-graph-market',
                          style={'float': 'right',
                                 'margin-bottom': '40px',
                                 'marginTop': '20px',
                                 'height': '500px',
                                 # 'textAlign': 'left',
                                 # 'color': colors['text'],
                                 'border': '2px solid black',
                                 'border-radius': '10px',
                                 'padding': '10px',
                                 'box-shadow': '4px 4px 12px black',
                                 'width': '70%',
                                 'backgroundColor': 'white',
                                 'display': 'inline-block',  'border-radius':  '10px',
                                 }, figure={'layout': {
                        'plot_bgcolor': 'white',
                        'paper_bgcolor': 'white',
                        'font': 'darkblue',

                        # "border":{"width":"2px", "color":"black"}
                    }}
                    )], style={
            'display': 'flex',
            'align-items': 'center',
            'justify-content': 'space-between',
        }),
            dcc.Dropdown(id='power-dropdown', multi=True,
                                                           value=['DE00_GT02', 'DE00_GT01', 'DE00_GOTN', 'DE00_GOTO', 'DE00_GCO2', 'DE00_HCNW',
                                                                  'DE00_LGO1']
                                                           , style={
                                          'margin-bottom': '6px',
                                          'marginTop': '0 auto',
                                          'marginLeft': '50px',
                                          'padding': '10px',
                                          # 'margin': '0',
                                  'border': '2px solid lightblue',
                                  'textAlign': 'left',
                                  'width': '80%',
                                  # 'float': 'right',
                                  # 'height': '30px',
                                  # 'lineHeight': '30px',
                                  'borderWidth': '1px',
                                  # # 'borderStyle': 'dashed',
                                  'borderRadius': '5px',
                                  # 'display': 'inline-block',
                                  # # 'margin': '10px',
                                  # 'color': 'darkgray',
                                  'backgroundColor': 'white'
                                      },),
                dcc.Graph(id='bar-graph-market_trend',
                          style={
                              'height': '500px',
                              'width': '96%',
                              'border': '2px solid black',
                              'border-radius': '10px',
                              'box-shadow': '4px 4px 12px black',
                              'backgroundColor': 'white',
                              'display': 'block',
                              'margin': '0 auto',
                          },
                          figure={'layout': {
                              'plot_bgcolor': 'white',
                              'paper_bgcolor': 'white',
                              'font': 'darkblue',
                          }}

                          ), html.Div('Source: TenneT TSO \ ESP-MA Database', style={
                'color': 'darkblue',
                'text-align': 'left',
                'margin-top': '40px',
                'font-size': '16px'
            })
                # ]
                # )
                # ]
                # )

            ]),
        ], style={
            'float': 'right',
            'backgroundColor': 'alieceblue',
                                 'marginTop': '100px',
                                 'marginBottom': '5px',
                                 'marginLeft': '330px',
                                 'height': '1250px',
                                 # 'textAlign': 'left',
                                 # 'color': colors['text'],
                                 'border': '2px solid white',
                                 # 'border-radius': '10px',
                                 'padding': '10px',
                                 'box-shadow': '4px 4px 12px black',
    })



        #     html.Div([html.Div([dcc.Graph(id='bar-graph-market',
        #                            style={'float': 'right',
        #                                   'marginTop': '100px',
        #                                   'margin-bottom': '30px',
        #                                   'height': '400px',
        #                                   # 'textAlign': 'left',
        #                                   # 'color': colors['text'],
        #                                   'border': '2px solid black',
        #                                   'border-radius': '10px',
        #                                   'padding': '10px',
        #                                   'box-shadow': '4px 4px 12px black',
        #                                   'width': '50%',
        #                                   'backgroundColor': 'white',
        #                                   'display': 'inline-block', 'border-radius':  '10px',
        #                                   }, figure={'layout': {
        #         'plot_bgcolor': 'white',
        #         'paper_bgcolor': 'white',
        #         'font': 'darkblue',
        #
        #         # "border":{"width":"2px", "color":"black"}
        #     }}
        #             ), dcc.Dropdown(id='power-dropdown', multi=True,
        #                          value=['DE00_GT02', 'DE00_GT01', 'DE00_GOTN', 'DE00_GOTO', 'DE00_GCO2', 'DE00_HCNW',
        #                                 'DE00_LGO1']
        #                          , style={
        #         'margin - bottom': '12px',
        #         'padding': '0',
        #         'margin': '0',
        # 'border': '2px solid lightblue',
        # 'textAlign': 'left',
        # 'width': '80%',
        # 'float': 'right',
        # # 'height': '30px',
        # # 'lineHeight': '30px',
        # 'borderWidth': '1px',
        # # # 'borderStyle': 'dashed',
        # 'borderRadius': '5px',
        # # 'display': 'inline-block',
        # # # 'margin': '10px',
        # # 'color': 'darkgray',
        # 'backgroundColor': 'white'
        #     },), dcc.Graph(id='bar-graph-market_trend',
        #                                       style={'float': 'right',
        #                                              # 'textAlign': 'left',
        #                                              # 'color': colors['text'],
        #                                              'border': '2px solid black',
        #                                              'border-radius': '10px',
        #                                              'padding': '10px',
        #                                              'box-shadow': '4px 4px 12px black',
        #                                              'width': '80%',
        #                                              'backgroundColor': 'white',
        #                                              'display': 'inline-block', 'border-radius':  '10px',
        #                                              }, figure={'layout': {
        #         'plot_bgcolor': 'white',
        #         'paper_bgcolor': 'white',
        #         'font': 'darkblue',
        #         # "border":{"width":"2px", "color":"black"}
        #     }} ),
        #         # ]
        #         # )
        #         # ]
        #         # )
        #
        #      ]),], style={
        #     'float': 'right',
        #     'backgroundColor': 'lavender',
        #                          'marginTop': '100px',
        #                          'marginBottom': '5px',
        #                          'marginLeft': '330px',
        #     'height': '1250px',
        #                          # 'height': '400px',
        #                          # 'textAlign': 'left',
        #                          # 'color': colors['text'],
        #                          'border': '2px solid white',
        #                          # 'border-radius': '10px',
        #                          'padding': '10px',
        #                          'box-shadow': '4px 4px 12px black',})
##############################################################
    #         html.Div([dbc.Row([
    #
    #         html.Div([
    #             html.Div([
    #                 html.Span('7.38K', style={
    #                     'display': 'block',
    #                     'color': 'black',
    #                     'font-size': '50px',
    #                     'font-weight': 'bold',
    #                     'text-align': 'center'
    #                 }),
    #                 html.Span('DE00_WONS', style={
    #                     'display': 'block',
    #                     'color': 'black',
    #                     'font-size': '30px',
    #                     'font-weight': 'bold',
    #                     'text-align':'center'
    #                 }),
    #             ], style={
    #                 'margin-right': '20px',
    #             }),
    #
    #             dcc.Graph(id='bar-graph-market',
    #                       style={'float': 'right',
    #                              'margin-bottom': '100px',
    #                              'marginTop': '50px',
    #                              'height': '500px',
    #                              # 'textAlign': 'left',
    #                              # 'color': colors['text'],
    #                              'border': '2px solid black',
    #                              'border-radius': '10px',
    #                              'padding': '10px',
    #                              'box-shadow': '4px 4px 12px black',
    #                              'width': '70%',
    #                              'backgroundColor': 'white',
    #                              'display': 'inline-block',  'border-radius':  '10px',
    #                              }, figure={'layout': {
    #                     'plot_bgcolor': 'white',
    #                     'paper_bgcolor': 'white',
    #                     'font': 'darkblue',
    #
    #                     # "border":{"width":"2px", "color":"black"}
    #                 }}
    #                 )], style={
    #         'display': 'flex',
    #         'align-items': 'center',
    #         'justify-content': 'space-between',
    #     }),
    #         dcc.Dropdown(id='power-dropdown', multi=True,
    #                                          value=['DE00_GT02', 'DE00_GT01', 'DE00_GOTN', 'DE00_GOTO', 'DE00_GCO2', 'DE00_HCNW',
    #                                                 'DE00_LGO1']
    #                                          , style={
    #                         'margin - bottom': '12px',
    #                         'padding': '0',
    #                         'margin': '0',
    #                 'border': '2px solid lightblue',
    #                 'textAlign': 'left',
    #                 'width': '80%',
    #                 'float': 'right',
    #                 # 'height': '30px',
    #                 # 'lineHeight': '30px',
    #                 'borderWidth': '1px',
    #                 # # 'borderStyle': 'dashed',
    #                 'borderRadius': '5px',
    #                 # 'display': 'inline-block',
    #                 # # 'margin': '10px',
    #                 # 'color': 'darkgray',
    #                 'backgroundColor': 'white'
    #                     },),
    #             dcc.Graph(id='bar-graph-market_trend',
    #                                           style={'float': 'right',
    #                                                  # 'textAlign': 'left',
    #                                                  # 'color': colors['text'],
    #                                                  'border': '2px solid black',
    #                                                  'border-radius': '10px',
    #                                                  'padding': '10px',
    #                                                  'box-shadow': '4px 4px 12px black',
    #                                                  'width': '80%',
    #                                                  'backgroundColor': 'white',
    #                                                  'display': 'inline-block', 'border-radius':  '10px',
    #                                                  }, figure={'layout': {
    #             'plot_bgcolor': 'white',
    #             'paper_bgcolor': 'white',
    #             'font': 'darkblue',
    #             # "border":{"width":"2px", "color":"black"}
    #         }}
    #
    #                       ), html.Div('Source: TenneT TSO \ ESP-MA Database', style={
    #             'color': 'darkblue',
    #             'text-align': 'left',
    #             'margin-top': '40px',
    #             'font-size': '16px'
    #         })
    #             # ]
    #             # )
    #             # ]
    #             # )
    #
    #         ]),
    #     ], style={
    #         'float': 'right',
    #         'backgroundColor': 'lavender',
    #                              'marginTop': '100px',
    #                              'marginBottom': '5px',
    #                              'marginLeft': '330px',
    #                              'height': '1250px',
    #                              # 'textAlign': 'left',
    #                              # 'color': colors['text'],
    #                              'border': '2px solid white',
    #                              # 'border-radius': '10px',
    #                              'padding': '10px',
    #                              'box-shadow': '4px 4px 12px black',
    # })

 # #############################################################################################################################################
 #############################################################################################################################################
@app.callback(
    # [Output('df_cp_pos_store', 'data'),
    # Output('df_cp_neg_store', 'data'),
    #     Output('power_plant_store', 'data')
    Output('power-dropdown', 'options'),
# ],

    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('output-data-upload', 'children'),
    prevent_initial_call=True)

@cache.memoize(timeout=1)
def update_output(contents, filename, children):
    start_time = time.time()
    print('hello')
    if contents is not None:
        df = None
        rao_planzs = None
        market_areas = None
        for i, (c, n) in enumerate(zip(contents, filename)):
            content_type, content_string = contents[i].split(',')
            decoded = base64.b64decode(content_string)
            if 'csv' in filename[i]:
                dff = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep=';', decimal=',')
                if 'generation_per_plant_change' in filename[i]:
                    df = dff
                elif 'rao_plants' in filename[i]:
                    rao_planzs = dff
                else:
                    market_areas = dff
            else:
                raise ValueError("Unsupported file format")
##############################################
    global df_cp_pos
    global df_cp_neg
    # global power_plant

    df = df.iloc[2:, :]
    df_c = pd.merge(df, market_areas[['ID', 'name']], left_on='market_area_ID', right_on='ID', how='left')
    df_cp = pd.merge(df_c, rao_planzs[['ID', 'name']], left_on='plant_ID', right_on='ID', how='left')
    df_cp.drop(['market_area_ID', 'plant_ID', 'ID_x', 'ID_y'], axis=1, inplace=True)

    df_cp_pos = df_cp.copy()
    df_cp_pos.iloc[:, 1:-2] = df_cp_pos.iloc[:, 1:-2].mask(df_cp_pos.iloc[:, 1:-2] < 0, 0)

    df_cp_neg = df_cp.copy()
    df_cp_neg.iloc[:, 1:-2] = df_cp_neg.iloc[:, 1:-2].mask(df_cp_neg.iloc[:, 1:-2] > 0, 0)

    mapping_dict = dict(zip(rao_planzs['type_ID'], rao_planzs['mover']))
    df_cp_pos['pemmdb_type_ID'] = df_cp_pos['pemmdb_type_ID'].map(mapping_dict).fillna(
        df_cp_pos['pemmdb_type_ID'])
    df_cp_neg['pemmdb_type_ID'] = df_cp_neg['pemmdb_type_ID'].map(mapping_dict).fillna(
        df_cp_neg['pemmdb_type_ID'])

    power_plant=df_cp_neg['name_y'].str[:-8].unique().tolist()

    # df_cp_pos= df_cp_pos.to_json(date_format='iso', orient='split')
    # df_cp_neg = df_cp_neg.to_json(date_format='iso', orient='split')
    # print(df_cp_pos)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time1: {execution_time:.4f} seconds")
    return power_plant
    # return df_cp_pos, df_cp_neg, power_plant

# start_time = time.time()
# end_time = time.time()
# execution_time = end_time - start_time
# print(f"Execution time: {execution_time:.4f} seconds")

@app.callback(
    # Output('tabs-content-inline', 'children'),
    [
    Output('bar-graph-market_trend', 'figure', allow_duplicate=True),
    Output('bar-graph-market', 'figure', allow_duplicate=True),
    # Output('subtabs1', 'children', allow_duplicate=True),
    ],
     [
      # Input('df_cp_pos_store', 'data'),
      # Input('df_cp_neg_store', 'data'),
      # Input('power_plant_store', 'data'),
    Input('tabs-styled-with-inline', 'value'),
    Input('power-dropdown', 'value'),
 ], prevent_initial_call=True)
@cache.memoize(timeout=1)
def graph_creation(
        # df_cp_pos, df_cp_neg,
        tab, power_plant):
    start_time = time.time()
    global df_cp_pos
    global df_cp_neg
    # global power_plant
    # if tab != 'tab-3' and tab != 'tab-6':
    #     return no_update, no_update
    if power_plant is None or len(power_plant) == 0:
        return no_update, no_update
    #     raise PreventUpdate

    # print('hello')
    # print(power_plant)
    # if df_cp_pos is None:
    #     break
    # df_cp_pos_copy = df_cp_pos.copy()
    # if df_cp_neg is None:
    #     break
    # df_cp_neg_copy = df_cp_neg.copy()

    # df_cp_pos = pd.read_json(df_cp_pos, orient='split')
    # df_cp_neg = pd.read_json(df_cp_neg, orient='split')

    # print(f'this is the datframe{df_cp_neg}')
    df_cp_pos_copy= df_cp_pos.copy()
    df_cp_neg_copy = df_cp_neg.copy()

    df_cp_pos_copy['name_y'] = df_cp_pos['name_y'].str[:-8]
    df_cp_neg_copy['name_y'] = df_cp_neg['name_y'].str[:-8]

    df_cp_pos_c = df_cp_pos_copy.drop(['name_x', 'pemmdb_type_ID'], axis=1)
    df_cp_neg_c = df_cp_neg_copy.drop(['name_x', 'pemmdb_type_ID'], axis=1)
    value_columns = df_cp_pos_copy.columns[1:-2]


    if tab=='tab-0':
        return html.Div([
            html.Img(src=app.get_asset_url('Capture1.png'),
                     style={'width': '100%', 'height': 'auto', 'position': 'fixed',
                            })
        ])
    elif tab=='tab-1':
        df_cp_pos_copy= df_cp_pos.copy()

        market_group_pos = df_cp_pos_copy.groupby(['name_x'])[value_columns].sum().reset_index()
        market_group_pos['Max'] = market_group_pos.iloc[:, 1:-1].max(axis=1)
        market_group_pos['Hour'] = market_group_pos[value_columns].idxmax(axis=1)
        market_group_pos1 = market_group_pos[['name_x', 'Max', 'Hour']].sort_values(by='Max', ascending=False)
        fig1 = px.bar(market_group_pos1, x='name_x', y='Max', color_discrete_sequence=['blue'])
        fig1.update_layout(
            # title='Maximum Energy Production per Power Plants',
                          xaxis_title='Market Area',
                          yaxis_title='Max Number of Hours',  plot_bgcolor='white',
paper_bgcolor='white',
font_color='darkblue', font=dict(
        family="Courier New, monospace",
        size=18,
        color="darkblue",
        variant="small-caps", ))

        market_group_pos1['Max'] = market_group_pos1['Max'].abs()
        fig2 = px.pie(market_group_pos1, values='Max', names='name_x',
                      # title='Population of European continent'
                      )
        fig2.update_layout(plot_bgcolor='white',
                              paper_bgcolor='white',
                              font_color='darkblue', font=dict(
                family="Courier New, monospace",
                size=18,
                color="darkblue",
                variant="small-caps", ))
        return fig1, fig2

    elif  tab=='tab-2':
        df_cp_pos_copy = df_cp_pos.copy()
        group_types_pos = df_cp_pos_copy.groupby(['pemmdb_type_ID'])[value_columns].sum().reset_index()
        group_types_pos['Max'] = group_types_pos.iloc[:, 1:-1].max(axis=1)
        group_types_pos['Hour'] = group_types_pos[value_columns].idxmax(axis=1)
        group_types_pos = group_types_pos.sort_values(by='Max', ascending=False)
        fig1 = px.bar(group_types_pos, x='pemmdb_type_ID', y='Max', color_discrete_sequence=['blue'])
        fig1.update_layout(
            # title='Maximum Energy Production per Power Plants',
                          xaxis_title='Type of Technology',
                          yaxis_title='Max Number of Hours',  plot_bgcolor='white',
paper_bgcolor='white',
font_color='darkblue', font=dict(
        family="Courier New, monospace",
        size=18,
        color="darkblue",
        variant="small-caps", ))

        fig2 = px.pie(group_types_pos, values='Max', names='pemmdb_type_ID',
                      # title='Population of European continent'
                      )
        fig2.update_layout(plot_bgcolor='white',
                              paper_bgcolor='white',
                              font_color='darkblue', font=dict(
                family="Courier New, monospace",
                size=18,
                color="darkblue",
                variant="small-caps", ))
        return fig1, fig2

    elif tab=='tab-3':
        if not power_plant:
            return no_update
        else:

            mask = df_cp_pos_c[(df_cp_pos_c['name_y']).isin(power_plant)]
            mask = mask.groupby(['name_y'])[value_columns].sum().reset_index()
            mask = mask.transpose().reset_index()
            mask = mask.rename(columns=mask.iloc[0]).loc[1:]
            fig1 = px.line(mask, x='name_y', y=mask.columns[1:])
            fig1.update_layout(
                # title='Maximum Energy Production per Power Plants',
                               xaxis_title='Power Plant',
                               yaxis_title='Max Number of Hours', plot_bgcolor='white',
                               paper_bgcolor='white',
                               font_color='darkblue', font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="darkblue",
                    variant="small-caps", ), legend_title=None,
                               legend=dict(x=0, y=1, orientation="h", font=dict(family="Courier", size=12)))

            mask = df_cp_pos_copy[(df_cp_pos_copy['name_y']).isin(power_plant)].groupby(['name_y'])[value_columns].sum().reset_index()
            mask['Max'] = mask.iloc[:, 1:].max(axis=1)
            group_plants_columns = mask.columns[1:-1]
            mask['Hour'] = mask[group_plants_columns].idxmax(axis=1)
            mask1 = mask[['name_y', 'Max', 'Hour']]
            fig2 = px.bar(mask1, x='name_y', y='Max', color_discrete_sequence=['blue'])
            fig2.update_layout(
                # title='Maximum Energy Production per Power Plants',
                               xaxis_title='Power Plant',
                               yaxis_title='Max Number of Hours', plot_bgcolor='white',
                               paper_bgcolor='white',
                               font_color='darkblue', font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="darkblue",
                    variant="small-caps", ))

            # mask = df_cp_pos_copy[(df_cp_pos_copy['name_y']).isin(power_plant)].groupby(['name_y'])[value_columns].sum().reset_index()
            # mask['Max'] = mask.iloc[:, 1:].max(axis=1)
            # group_plants_columns = mask.columns[1:-1]
            # mask['Hour'] = mask[group_plants_columns].idxmax(axis=1)
            # mask1 = mask[['name_y', 'Max', 'Hour']]
            # fig2 = px.pie(mask1, values='Max', names='name_y', title='Population of European continent')
            return fig1, fig2

    elif tab=='tab-4':
        market_group_neg = df_cp_neg_copy.groupby(['name_x'])[value_columns].sum().reset_index()
        market_group_neg['Max'] = market_group_neg.iloc[:, 1:-1].min(axis=1)
        market_group_neg['Hour'] = market_group_neg[value_columns].idxmax(axis=1)
        market_group_neg1 = market_group_neg[['name_x', 'Max', 'Hour']].sort_values(by='Max', ascending=True)
        fig1 = px.bar(market_group_neg1, x='name_x', y='Max', color_discrete_sequence=['red'])
        fig1.update_layout(
            # title='Maximum Energy Load per Power Plants',
                          xaxis_title='Market Area',
                          yaxis_title='Max Number of Hours', plot_bgcolor='white',
paper_bgcolor='white',
font_color='darkblue', font=dict(
        family="Courier New, monospace",
        size=18,
        color="darkblue",
        variant="small-caps",))

        market_group_neg1['Max'] = market_group_neg1['Max'].abs()
        fig2 = px.pie(market_group_neg1, values='Max', names='name_x',
                      # title='Population of European continent'
                      )
        fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                           font_color='darkblue', font=dict(
                family="Courier New, monospace",
                size=18,
                color="darkblue",
                variant="small-caps", ))
        return fig1, fig2

    elif tab=='tab-5':
        group_types_neg = df_cp_neg_copy.groupby(['pemmdb_type_ID'])[value_columns].sum().reset_index()
        group_types_neg['Max'] = group_types_neg.iloc[:, 1:-1].min(axis=1)
        group_types_neg['Hour'] = group_types_neg[value_columns].idxmax(axis=1)
        # group_types_neg = group_types_neg.sort_values(by='Max')
        fig1 = px.bar(group_types_neg, x='pemmdb_type_ID', y='Max', color_discrete_sequence=['red'])
        fig1.update_layout(
            # title='Maximum Energy Load per Power Plants',
                          xaxis_title='Market Area',
                          yaxis_title='Max Number of Hours', plot_bgcolor='white',
paper_bgcolor='white',
font_color='darkblue', font=dict(
        family="Courier New, monospace",
        size=18,
        color="darkblue",
        variant="small-caps", ))

        group_types_neg['Max'] = group_types_neg['Max'].abs()
        fig2 = px.pie(group_types_neg, values='Max', names='pemmdb_type_ID',
                      # title='Population of European continent'
                      )
        fig2.update_layout(plot_bgcolor='white',
                              paper_bgcolor='white',
                              font_color='darkblue', font=dict(
                family="Courier New, monospace",
                size=18,
                color="darkblue",
                variant="small-caps", ))
        return fig1, fig2

    elif tab=='tab-6':
        if not power_plant:
            return no_update
        else:

            mask = df_cp_neg_c[(df_cp_neg_c['name_y']).isin(power_plant)]
            mask = mask.groupby(['name_y'])[value_columns].sum().reset_index()
            mask = mask.transpose().reset_index()
            mask = mask.rename(columns=mask.iloc[0]).loc[1:]
            fig1 = px.line(mask, x='name_y', y=mask.columns[1:])
            fig1.update_layout(
                # title='Maximum Energy Production per Power Plants',
                               xaxis_title='Power Plant',
                               yaxis_title='Max Number of Hours', plot_bgcolor='white',
                               paper_bgcolor='white',
                               font_color='darkblue', font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="darkblue",
                    variant="small-caps", ), legend_title=None,
                               legend=dict(x=0, y=1, orientation="h", font=dict(family="Courier", size=12)))

            mask = df_cp_neg_copy[(df_cp_neg_copy['name_y']).isin(power_plant)].groupby(['name_y'])[value_columns].sum().reset_index()
            mask['Max'] = mask.iloc[:, 1:].min(axis=1)
            group_plants_columns = mask.columns[1:-1]
            mask['Hour'] = mask[group_plants_columns].idxmax(axis=1)
            mask1 = mask[['name_y', 'Max', 'Hour']]
            fig2 = px.bar(mask1, x='name_y', y='Max', color_discrete_sequence=['red'])
            fig2.update_layout(
                # title='Maximum Energy Load per Power Plants',
                               xaxis_title='Power Plant',
                               yaxis_title='Max Number of Hours', plot_bgcolor='white',
                               paper_bgcolor='white',
                               font_color='darkblue')

            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Execution time2: {execution_time:.4f} seconds")
            return fig1, fig2


if __name__ == '__main__':
    app.run_server(debug=True)


