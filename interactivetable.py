from dash import Dash, html, dash_table, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import graphs
import ipsossql as ips
import graphs as gr
import pandas as pd

# Color constants from IPSOS graph
DARK_BLUE_LGH = dict(color='rgba(47, 70, 156, 0.6)')  # dark blue (lesbian/gay/homosexual), rgb: 47, 70, 156 , hex: #2f469c
LIGHT_BLUE_BI = dict(color='rgba(190, 219, 255, 0.6)')  # light blue (bisexual), rgb: 190, 219, 255 , hex: #bedbff
# noinspection SpellCheckingInspection
PURPLE_PANOMNI = dict(color='rgba(132, 50, 155, 0.6)')  # purple (pansexual/omnisexual), rgb: 132, 50, 155 , hex: #84329b
PINK_ACE = dict(color='rgba(255, 175, 199, 0.6)')  # pink (asexual), rgb: 255, 175, 199 , hex: #ffafc7


# initialize graph: question 1
# run SQL query for graph metadata
metadatasql = graphs.question_metadata(ips.QUESTION_METADATA)

# run SQL Query for graph
sqlqueryresults = ips.run_query(ips.INTERACTIVETABLE)
# rename the columns to something human friendly
columndisplaynames = ['Country', 'Lesbian/Gay/Homosexual', 'Bisexual', 'Pansexual/Omnisexual', 'Asexual', 'Total LGB+', 'Change Vs. 2021']
# get the dataframe
df = gr.interactive_test(sqlqueryresults, columndisplaynames, 1)

# shortest way to viz the dataframe
# print(df.to_markdown())

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

app.layout = html.Div([
    html.Div(id='datatable-interactivity-container'),
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=50,
    )
])


@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    Input('datatable-interactivity', 'selected_columns')
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('datatable-interactivity-container', "children"),
    Input('datatable-interactivity', "derived_virtual_data"),
    Input('datatable-interactivity', "derived_virtual_selected_rows"))
def update_graphs(rows, derived_virtual_selected_rows):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)
    dff = bars(dff)
    # print('\r\ndff:')
    # print(dff.to_markdown())

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff))]


    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff[column],
                        "y": dff["Country"],
                        "type": "bar",
                        "barmode": "stack",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "title_text": "title of graph",
                    "paper_bgcolor": "white",
                    "plot_bgcolor": "snow",
                    "xaxis_title": "Percentage LGB+ by Identity",
                    "yaxis_title": "Country",
                    "showlegend": True,
                    "xaxis_tickformat": ".0%",
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 500,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        )
        for column in columndisplaynames if column in dff
    ]


if __name__ == '__main__':
    app.run_server(debug=True)