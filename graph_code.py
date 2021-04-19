import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import numpy as np
import pandas as pd
import plotly.express as px
import dash
import plotly.graph_objects as go

params = [
   'Values', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 
]

df = pd.read_csv("dynamic dataset.csv")
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df_temp = pd.DataFrame(df.to_dict('records'))
melted = df_temp.melt('Expenditure', var_name='Months', value_name='Money')
pixg = px.bar(melted, x="Months", y=["Money", "Expenditure"], color="Expenditure", barmode="group")
app.layout = html.Div([

    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        editable=True
    ),

    # html.H6("Change the value in the text box to see callbacks in action!"),
    # html.Div(["Input: ", dcc.Input(id='my-input', value='10', type='number')]),
    # html.Div(["Input: ", dcc.Input(id='my-input2', value='8', type='number')]),
    
    html.Br(),
    dcc.Graph(
        id='graph',
        figure=pixg
    ),
    # html.Div(id='my-output2'),
    # html.Div(id='my-output3'),
    
])

def is_int(string_something):
    try: 
        int(string_something)
        return True
    except ValueError:
        return False

@app.callback(
    Output(component_id='graph', component_property='figure'),
    # Output(component_id='my-output2', component_property='children'),
    # Output(component_id='my-output3', component_property='children'),
    # Input(component_id='my-input', component_property='value'),
    # Input(component_id='my-input2', component_property='value'),
    Input('table', 'data')
)
def update_output_div(a):
    global pixg
    for d in a:
        for k in d.keys():
            if isinstance(d[k], str) and (k != 'Expenditure'):
                if is_int(d[k]):
                    d[k] = int(d[k])
                else:
                    return pixg
    df = pd.DataFrame(a)
    melted = df.melt('Expenditure', var_name='Months', value_name='Money')
    y = px.bar(melted, x="Months", y=["Money", "Expenditure"], color="Expenditure", barmode="group")
    pixg = y
    return y


if __name__ == '__main__':

    app.run_server(debug=True)
