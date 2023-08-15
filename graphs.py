import pandas as pd
import plotly.graph_objects as go
import ipsossql as ips

# Color constants from IPSOS graph
DARK_BLUE_LGH = dict(color='rgba(47, 70, 156, 0.6)')  # dark blue (lesbian/gay/homosexual), rgb: 47, 70, 156 , hex: #2f469c
LIGHT_BLUE_BI = dict(color='rgba(190, 219, 255, 0.6)')  # light blue (bisexual), rgb: 190, 219, 255 , hex: #bedbff
# noinspection SpellCheckingInspection
PURPLE_PANOMNI = dict(color='rgba(132, 50, 155, 0.6)')  # purple (pansexual/omnisexual), rgb: 132, 50, 155 , hex: #84329b
PINK_ACE = dict(color='rgba(255, 175, 199, 0.6)')  # pink (asexual), rgb: 255, 175, 199 , hex: #ffafc7


def countrystackedbar(sqlqueryresults, columnnamebarcolormap, columndisplaynames, columndisplaysortindex, graphtitle, xaxistitle, yaxistitle, yaxis='Country'):
    # initializing pandas data frame and renaming columns to be pretty
    df = pd.DataFrame([[ij for ij in i] for i in sqlqueryresults])
    renamed = {}
    iterator = 0
    for x in columndisplaynames:
        renamed[df.columns[iterator]] = x
        iterator += 1
    df.rename(columns=renamed, inplace=True)
    df = df.sort_values([columndisplaynames[0]], ascending=[columndisplaysortindex])

    # create the stacked bars
    bars = []
    for index, row in df.iterrows():
        for x in columnnamebarcolormap:
            bar = go.Bar(name=x[0], y=[row[yaxis]], x=[row[x[0]]], orientation='h', marker=x[1], legendgroup=x[0],
                         hoverlabel=dict(namelength=-1), text=str(row[x[0]]))
            bars.append(bar)

    # create our figure
    figure = go.Figure(data=bars)
    # TODO pull title from sql database
    figure.update_layout(barmode='stack',
                         title_text=graphtitle,
                         paper_bgcolor='white',
                         plot_bgcolor='snow',
                         xaxis_title=xaxistitle,  #"Percentage LGB+ by Identity",
                         yaxis_title=yaxistitle,  #"Country",
                         showlegend=True, xaxis_tickformat='.0%')
    # show text labels as percentages in bars, positioned forced to the inside of the bars, center (middle) text
    figure.update_traces(texttemplate='%{text:.0%}', textposition='inside', insidetextanchor="middle")
    removelegenddupes(figure)
    return figure, df


def removelegenddupes(figure):
    # widget to remove duplicates in legend entries
    names = set()
    figure.for_each_trace(
        lambda trace:
        trace.update(showlegend=False)
        if (trace.name in names) else names.add(trace.name)
    )
    return figure


def question_metadata(question_metadata):
    metadatasql = ips.run_query(question_metadata)
    title = metadatasql[0][0]
    question = metadatasql[0][1]
    pages = page_numbers(metadatasql[0][2], metadatasql[0][3])
    title_pages = metadatasql[0][0] + pages
    title_pages_question = metadatasql[0][0] + pages + '<br><i>' + question + '</i><br>'
    return title_pages_question, title_pages, question, title, pages

def page_numbers(start, end):

    if end is None:
        pagenumbers = " - From Page " + str(start) + ' in <a href="https://www.ipsos.com/en/pride-month-2023-9-of-adults-identify-as-lgbt">Original Ipsos Report</a>'
    else:
        pagenumbers = " - From Pages " + str(start) + " to " + str(end) + ' in <a href="https://www.ipsos.com/en/pride-month-2023-9-of-adults-identify-as-lgbt">Original Ipsos Report</a>'
    return pagenumbers

