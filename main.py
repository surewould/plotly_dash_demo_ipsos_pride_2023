from dash import Dash, html, dash_table, dcc
import dash_bootstrap_components as dbc
import graphs
import ipsossql as ips
import graphs as gr



# initialize graph: question 1
# run SQL query for graph metadata
metadatasql = graphs.question_metadata(ips.QUESTION_METADATA)
# run SQL Query for graph
sqlqueryresults = ips.run_query(ips.QUESTION_DATA_1)
# rename the columns to something human friendly
columndisplaynames = ['Country', 'Lesbian/Gay/Homosexual', 'Bisexual', 'Pansexual/Omnisexual', 'Asexual', 'Total LGB+',
                      'Change Vs. 2021']
# assign colors to bar graph
columnnamebarcolormap = [[columndisplaynames[1], gr.DARK_BLUE_LGH],
                         [columndisplaynames[2], gr.LIGHT_BLUE_BI],
                         [columndisplaynames[3], gr.PURPLE_PANOMNI],
                         [columndisplaynames[4], gr.PINK_ACE]]
# build and get the graph
fig_question_1 = gr.countrystackedbar(sqlqueryresults, columnnamebarcolormap, columndisplaynames, 0, metadatasql[0], 'Percentage of Population by Identity', 'Country', )


# initialize dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

# configure dash app layout
# app.layout = html.Div([
#     html.Div(children=metadatasql[0]),
#     dcc.Graph(figure=fig_question_1[0], style={'width': '180vh', 'height': '90vh'}),  # TODO fix style trick to do 90% of vertical and horizontal screen space; not quite working
#     dash_table.DataTable(data=fig_question_1[1].to_dict('records'), page_size=50)
# ])
ourgraph = html.Div([dcc.Graph(figure=fig_question_1[0], style={'height': '95vh'})])
menu = html.Div([dropdown])
ourtable = html.Div([dash_table.DataTable(data=fig_question_1[1].to_dict('records'))])
ourdata = [menu, ourgraph, ourtable]
app.layout = dbc.Container(ourdata, fluid=True)



# run the dash app
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)
