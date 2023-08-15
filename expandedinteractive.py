from dash import Dash, html, dash_table, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import ipsossql as ips
import graphs as gr
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.offline as poff

# Color constants from IPSOS graph
DARK_BLUE_LGH = dict(color='rgba(47, 70, 156, 0.6)')  # dark blue (lesbian/gay/homosexual), rgb: 47, 70, 156 , hex: #2f469c
LIGHT_BLUE_BI = dict(color='rgba(190, 219, 255, 0.6)')  # light blue (bisexual), rgb: 190, 219, 255 , hex: #bedbff
PURPLE_PANOMNI = dict(color='rgba(132, 50, 155, 0.6)')  # purple (pansexual/omnisexual), rgb: 132, 50, 155 , hex: #84329b
PINK_ACE = dict(color='rgba(255, 175, 199, 0.6)')  # pink (asexual), rgb: 255, 175, 199 , hex: #ffafc7


def removelegenddupes(figure):
    # removes duplicates in bar graph legend entries
    names = set()
    figure.for_each_trace(
        lambda trace:
        trace.update(showlegend=False)
        if (trace.name in names) else names.add(trace.name)
    )
    return figure


# get metadata from db
query = ('''select distinct question.title, question.question, question.page_number_start, 
question.page_number_end, question_id from question_data_1 inner join question
on question_data_1.question_id = question.id;''')
metadatasql = ips.run_query(query)
title = metadatasql[0][0]
question = metadatasql[0][1]


# get table and graph data from db
sqlqueryresults = ips.run_query('''select country.country_name, lesbian_gay_homosexual, bisexual, pansexual_omnisexual, asexual, 
`total_lgb+`, change_vs_2021 from question_data_1 inner join country on question_data_1.country_id = country.id;''')


# create dataframe
df = pd.DataFrame([[ij for ij in i] for i in sqlqueryresults])

# rename columns in dataframe to friendly names
columndisplaynames = ['Country', 'Lesbian/Gay/Homosexual', 'Bisexual', 'Pansexual/Omnisexual', 'Asexual', 'Total LGB+',
                      'Change Vs. 2021']
renamed = {}
iterator = 0
for x in columndisplaynames:
    renamed[df.columns[iterator]] = x
    iterator += 1
df.rename(columns=renamed, inplace=True)

# associate bar graph colors to friendly names
# assign colors to bar graph
columnnamebarcolormap = [[columndisplaynames[1], DARK_BLUE_LGH],
                         [columndisplaynames[2], LIGHT_BLUE_BI],
                         [columndisplaynames[3], PURPLE_PANOMNI],
                         [columndisplaynames[4], PINK_ACE]]


def updatefigure(dfo):
    bars = []
    for index, row in dfo.iterrows():
        for col_color in columnnamebarcolormap:
            try:
                bar = go.Bar(name=col_color[0], y=[row['Country']], x=[row[col_color[0]]], orientation='h', marker=col_color[1], legendgroup=col_color[0],
                             hoverlabel=dict(namelength=-1), text=str(row[col_color[0]]))
                bars.append(bar)
            except:
                pass

    # create our figure
    figure = go.Figure(data=bars)
    figure.update_layout(barmode='stack',
                         paper_bgcolor='white',
                         plot_bgcolor='snow',
                         xaxis_title="Percentage LGB+ by Identity",
                         yaxis_title="Country",
                         showlegend=True,
                         xaxis_tickformat='.0%',
                         yaxis=dict(autorange="reversed")
                         )
    # show text labels as percentages in bars, positioned forced to the inside of the bars, center (middle) text
    figure.update_traces(texttemplate='%{text:.0%}', textposition='inside', insidetextanchor="middle")
    # remove legend dupes
    figure = removelegenddupes(figure)
    return figure


# build dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

ourgraph = html.Div(id='datatable-interactivity-container')
ourtable = html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": False} for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable=False,
        row_deletable=True,
        page_action="native",
        page_current=0,
        page_size=50
    )
])
ourdata = [ourgraph, ourtable]
app.layout = dbc.Container(ourdata, style={'width': '98%', 'padding-bottom': '30px'}, fluid=True)


@app.callback(
    Output('datatable-interactivity-container', "children"),
    Input('datatable-interactivity', "derived_virtual_data")
)
def update_graphs(rows):
    dff = df if rows is None else pd.DataFrame(rows)

    # print('\r\ndf:')
    # print(df.to_markdown())
    #
    # print('\r\ndff:')
    # print(dff.to_markdown())

    return [
        dcc.Graph(
            figure=updatefigure(dff),
            style={'height': '90vh'}
        )
    ]


if __name__ == '__main__':
    app.run(debug=False)

