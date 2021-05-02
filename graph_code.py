import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import numpy as np
import pandas as pd
import plotly.express as px
import dash
import plotly.graph_objects as go

df = pd.read_csv("dynamic dataset.csv")
print(df)
app = dash.Dash(__name__)

df_temp = pd.DataFrame(df.to_dict('records'))
melted = df_temp.melt('Expenditure', var_name='Months', value_name='Money')
pixg = px.bar(melted, x="Months", y=["Money", "Expenditure"], color="Expenditure", barmode="group")
app.layout = html.Div(
    [
    html.Div("Expense Plotter", className="name"),
    dash_table.DataTable(
        id='table',
        columns=[{
            "name": i, 
            "id": i,
            'deletable':True,
            'renamable': True,
        } for i in df.columns],
        data=df.to_dict('records'),
        editable=True,
        row_deletable=True,
        export_format='csv',
        export_headers='display',
        merge_duplicate_headers=True
    ),
    html.Div([
            dcc.Input(
                id='adding-rows-name',
                placeholder='Enter a column name...',
                value='',
                style={'padding': 10}
            ),
            html.Button('Add Column', id='ColumnButton', n_clicks=0),
            dcc.Input(
                id='adding-columns-name',
                placeholder='Enter row name...',
                value='',
                style={'padding': 10}
            ),
            html.Button('Add Row', id='rowButton', n_clicks=0),
        ],
        style={'height': 50},
        className="left",
    ),
    # html.Div(["Input: ", dcc.Input(id='my-input', value='10', type='number')]),
    # html.Div(["Input: ", dcc.Input(id='my-input2', value='8', type='number')]),
    
    html.Br(),
    dcc.Graph(
        id='graph',
        figure=pixg
    ),
    # html.Div(id='my-output2'),
    # html.Div(id='my-output3'),
    
    ],
    className = "contain"
)

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


@app.callback(
    Output('table', 'columns'),
    Input('ColumnButton', 'n_clicks'),
    State('adding-rows-name', 'value'),
    State('table', 'columns'))
def update_columns(n_clicks, value, existing_columns):
    if n_clicks > 0:
        existing_columns.append({
            'id': value, 'name': value,
            'renamable': True, 'deletable': True
        })
    return existing_columns
    

@app.callback(
    Output('table', 'data'),
    Input('rowButton', 'n_clicks'),
    State('table', 'data'),
    State('adding-columns-name', 'value'),
    State('table', 'columns'))
def add_row(n_clicks, rows, value, columns):
    if n_clicks > 0: rows.append({'Expenditure': value, 'Jan': 0, 'Feb': 0, 'Mar': 0, 'Apr': 0, 'May': 0, 'Jun': 0, 'Jul': 0, 'Aug': 0})
    return rows


if __name__ == '__main__':

    app.run_server(debug=True)
