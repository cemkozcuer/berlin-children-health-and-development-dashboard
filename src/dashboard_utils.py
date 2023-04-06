import json
import plotly.express as px
from dash import html
from dash import dcc
from sklearn.manifold import TSNE


def get_choropleth_map(all_dataset_dicts, dataset_dropdown_value, reverse_colors):

    selected_dataset = all_dataset_dicts[f'dp_value_{dataset_dropdown_value}']

    fig = px.choropleth(
        selected_dataset['df'],
        locations=selected_dataset['location_key'],
        # if not "featureidkey" is used plotly uses automatically "id" in "properties" of geojson obj
        featureidkey='properties.SCHLUESSEL',
        geojson=berlin_lor_prognoseraume_geojson,
        color=selected_dataset['data_key'],
        hover_name=selected_dataset['hover_name_key'],
        hover_data=[selected_dataset['data_key']],
        title=selected_dataset['title'],
        template='none',
        color_continuous_scale=f'RdYlGn{("_r" if reverse_colors else "")}',
        range_color=(0, 100)
    )

    # remove margins of map
    fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
    # zoom map to existing data
    fig.update_geos(fitbounds='locations', visible=False)

    return fig


def get_map_html_block(configuration_dict, class_name='map-block', is_large=False):
    return html.Div(
        children=[
            html.Div(children=configuration_dict['block_title'], className='plot-title'),
            # html.Div(children=configuration_dict['text_block_text'], className='text-block'),

            html.Div(
                children=[
                    # visual adjustments for the graph
                    dcc.Graph(
                        id=configuration_dict['map_id'],
                        className=f'{"map-large" if is_large else "map"}',
                        # config={'displayModeBar': False}
                    ),

                    dcc.Slider(
                        id=configuration_dict['dropdown_id'],
                        min=int(min(configuration_dict['slider_options'].values())),
                        max=int(max(configuration_dict['slider_options'].values())),
                        value=int(max(configuration_dict['slider_options'].values())),
                        marks=configuration_dict['slider_options'],
                        step=None,
                        included=False,  # for being a discrete value
                        vertical=True,
                        className='slider-element'
                    ),
                ],
                className='map-module'
            ),
        ],
        className=class_name
    )


def get_barplot(df, title):

    fig = px.bar(
        df,
        y='Bezeichnung',
        x=[
            'have_language_deficit_relative',
            'attended_kita_more_than_2_years_relative',
            'attended_u8_relative', 'have_own_tv_relative',
            'have_prominent_visuo_motoric_disorder_relative'
        ],
        title=title,
        orientation='h',
        labels={
            'have_language_deficit_relative': '% Have Language Deficits',
            'attended_kita_more_than_2_years_relative': '% >2 Years Kita',
            'attended_u8_relative': '% Had U8',
            'have_own_tv_relative': '% Have Own TV',
            'have_prominent_visuo_motoric_disorder_relative': '% Visuo-Motoric Disorder'
        }
    )

    fig.update_layout(barmode='relative')

    return fig


def get_barplot_html_block(min_year, max_year, class_name='barplot-block'):
    return html.Div(
        children=[
            # html.Div(children='Barplots of all variables', className='plot-title'),
            # html.Div(children=configuration_dict['text_block_text'], className='text-block'),

            html.Div(
                children=[
                    # visual adjustments for the graph
                    dcc.Graph(
                        id='barplot-1',
                        className='barplot',
                        config={'displayModeBar': False}
                    ),

                    dcc.Slider(
                        id='barplot-year-slider',
                        min=min_year,
                        max=max_year,
                        value=max_year,
                        marks={str(year): str(year) for year in range(min_year, max_year + 1)},
                        step=None,
                        included=False,  # for being a discrete value
                        # vertical=True
                    )
                ],
                className='barplot-module'
            ),
        ],
        className=class_name
    )


def get_barplot_2(df, title):

    fig = px.bar(
        df,
        y='year',
        x=[
            'have_language_deficit_relative',
            'attended_kita_more_than_2_years_relative',
            'attended_u8_relative', 'have_own_tv_relative',
            'have_prominent_visuo_motoric_disorder_relative'
        ],
        title=title,
        orientation='h',
        labels={
            'have_language_deficit_relative': '% Have Language Deficits',
            'attended_kita_more_than_2_years_relative': '% >2 Years Kita',
            'attended_u8_relative': '% Had U8',
            'have_own_tv_relative': '% Have Own TV',
            'have_prominent_visuo_motoric_disorder_relative': '% Visuo-Motoric Disorder'
        }
    )

    fig.update_layout(barmode='relative')

    return fig


def get_barplot_html_block_2(dropdown_options, class_name='barplot-block'):

    return html.Div(
        children=[
            # html.Div(children='Some Barplot', className='plot-title'),
            # html.Div(children=configuration_dict['text_block_text'], className='text-block'),

            html.Div(
                children=[
                    # visual adjustments for the graph
                    dcc.Graph(
                        id='barplot-2',
                        className='barplot',
                        config={'displayModeBar': False}
                    ),

                    dcc.Dropdown(
                        id='barplot-district-dropdown',
                        options=dropdown_options,
                        value='Zentrum'
                    )
                ],
                className='barplot-module'
            ),
        ],
        className=class_name
    )


def get_lineplot(df, vars_checklist_options):

    fig = px.line(
        df.sort_values(by='year', ascending=False),
        x='year',
        y=vars_checklist_options,
        # color='Bezeichnung',
        title='Variables for single district',
        labels={
            'have_language_deficit_relative': '% Have Language Deficits',
            'attended_kita_more_than_2_years_relative': '% >2 Years Kita',
            'attended_u8_relative': '% Had U8',
            'have_own_tv_relative': '% Have Own TV',
            'have_prominent_visuo_motoric_disorder_relative': '% Visuo-Motoric Disorder'
        }
    )

    return fig


def get_lineplot_html_block(dropdown_district_options, checkbox_vars_options, class_name='lineplot-block'):
    return html.Div(
        children=[
            # html.Div(children='Some Lineplot', className='plot-title'),
            # html.Div(children=configuration_dict['text_block_text'], className='text-block'),

            html.Div(
                children=[
                    # visual adjustments for the graph
                    dcc.Graph(
                        id='lineplot-1',
                        className='lineplot',
                        config={'displayModeBar': False}
                    ),

                    dcc.Dropdown(
                        id='lineplot-1-district-dropdown',
                        options=dropdown_district_options,
                        value='Zentrum',
                        className='dropdown'
                    ),

                    dcc.Checklist(
                        id='lineplot-1-vars-checklist',
                        options=checkbox_vars_options,
                        value=['have_language_deficit_relative']
                    )
                ],
                className='lineplot-module'
            ),
        ],
        className=class_name
    )


def get_lineplot_2(df, vars_option):

    fig = px.line(
        df.sort_values(by='year', ascending=False),
        x='year',
        y=vars_option,
        color='Bezeichnung',
        title='Single variable for districts',
        labels={
            'have_language_deficit_relative': '% Have Language Deficits',
            'attended_kita_more_than_2_years_relative': '% >2 Years Kita',
            'attended_u8_relative': '% Had U8',
            'have_own_tv_relative': '% Have Own TV',
            'have_prominent_visuo_motoric_disorder_relative': '% Visuo-Motoric Disorder'
        }
    )

    return fig


def get_lineplot_html_block_2(dropdown_vars_options, checkbox_district_options, class_name='lineplot-block'):
    return html.Div(
        children=[
            # html.Div(children='Some Lineplot', className='plot-title'),
            # html.Div(children=configuration_dict['text_block_text'], className='text-block'),

            html.Div(
                children=[
                    # visual adjustments for the graph
                    dcc.Graph(
                        id='lineplot-2',
                        className='lineplot',
                        config={'displayModeBar': False}
                    ),

                    dcc.Dropdown(
                        id='lineplot-2-vars-dropdown',
                        options=dropdown_vars_options,
                        value='have_language_deficit_relative',
                        className='dropdown'
                    ),

                    dcc.Checklist(
                        id='lineplot-2-district-checklist',
                        options=checkbox_district_options,
                        value=['Zentrum']
                    )
                ],
                className='lineplot-module'
            ),
        ],
        className=class_name
    )


def get_correlation_plot(df):

    fig = px.imshow(
        df,
        text_auto=True,
        labels={
            'have_language_deficit_relative': '% Have Language Deficits',
            'attended_kita_more_than_2_years_relative': '% >2 Years Kita',
            'attended_u8_relative': '% Had U8',
            'have_own_tv_relative': '% Have Own TV',
            'have_prominent_visuo_motoric_disorder_relative': '% Visuo-Motoric Disorder'
        },
        range_color=(-1, 1),
        color_continuous_scale='RdBu'
    )

    return fig


def get_correlations_html_block(df, class_name='correlation-plot-block'):
    return html.Div(
        children=[
            html.Div(children='Correlation Map of Variables', className='plot-title'),
            # html.Div(children=configuration_dict['text_block_text'], className='text-block'),

            html.Div(
                children=[
                    # visual adjustments for the graph
                    dcc.Graph(
                        figure=get_correlation_plot(df),
                        id='correlation-plot',
                        className='correlation-plot',
                        config={'displayModeBar': False}
                    )
                ],
                className='correlation-module'
            ),
        ],
        className=class_name
    )


def get_scatter_matrix(df, attributes):

    fig = px.scatter_matrix(
        df,
        dimensions=attributes,
        color='year',
        labels={
            'have_language_deficit_relative': '% Have Language Deficits',
            'attended_kita_more_than_2_years_relative': '% >2 Years Kita',
            'attended_u8_relative': '% Had U8',
            'have_own_tv_relative': '% Have Own TV',
            'have_prominent_visuo_motoric_disorder_relative': '% Visuo-Motoric Disorder'
        }
    )

    fig.update_layout(font={'size': 9})

    return fig


def get_scatter_matrix_html_block(df, attributes, class_name='scatter-matrix-block'):
    return html.Div(
        children=[
            html.Div(children='Scatter Matrix of Variables', className='plot-title'),
            # html.Div(children=configuration_dict['text_block_text'], className='text-block'),

            html.Div(
                children=[
                    # visual adjustments for the graph
                    dcc.Graph(
                        figure=get_scatter_matrix(df, attributes),
                        id='scatter-matrix',
                        className='scatter-matrix',
                        config={'displayModeBar': False}
                    )
                ],
                className='scatter-matrix-module'
            ),
        ],
        className=class_name
    )


def get_tsne_plot_2(df, attributes, year):

    # selected_data = df[attributes]
    selected_data = df[df['year'] == year]
    selected_data_2 = selected_data[attributes]

    tsne = TSNE(n_components=3, random_state=0)
    projections = tsne.fit_transform(selected_data_2)

    # tsne = TSNE(n_components=3, random_state=0)
    # projections = tsne.fit_transform(features, )

    # fig = px.scatter_3d(
    #     projections, x=0, y=1, z=2,
    #     color=df.species, labels={'color': 'species'}
    # )
    # fig.update_traces(marker_size=8)

    fig = px.scatter_3d(
        projections,
        x=0,
        y=1,
        z=2,
        # color=df.year, labels={'color': 'year'}
        color=selected_data['Bezeichnung'], labels={'color': 'Bezeichnung'}
    )
    # fig.update_traces(marker_size=8)

    return fig


def get_tsne_html_block_2(df, attributes, min_year, max_year, class_name='tsne-plot-block'):
    return html.Div(
        children=[
            html.Div(children='t-SNE plot for one year, colored by district', className='plot-title'),
            # html.Div(children=configuration_dict['text_block_text'], className='text-block'),

            html.Div(
                children=[
                    # visual adjustments for the graph
                    dcc.Graph(
                        id='tsne-plot',
                        className='tsne-plot',
                        config={'displayModeBar': False}
                    )
                ],
                className='tsne-plot-module'
            ),

            dcc.Slider(
                id='tsne-year-slider',
                min=min_year,
                max=max_year,
                value=max_year,
                marks={str(year): str(year) for year in range(min_year, max_year + 1)},
                step=None,
                included=False,  # for being a discrete value
                # vertical=True
            )
        ],
        className=class_name
    )


def get_tsne_plot(df, attributes):

    selected_data = df[attributes]
    # selected_data = df[df['year'] == 2018]
    # selected_data_2 = selected_data[attributes]

    tsne = TSNE(n_components=3, random_state=0)
    projections = tsne.fit_transform(selected_data)

    # tsne = TSNE(n_components=3, random_state=0)
    # projections = tsne.fit_transform(features, )

    # fig = px.scatter_3d(
    #     projections, x=0, y=1, z=2,
    #     color=df.species, labels={'color': 'species'}
    # )
    # fig.update_traces(marker_size=8)

    fig = px.scatter_3d(
        projections,
        x=0,
        y=1,
        z=2,
        # color=df.year, labels={'color': 'year'}
        color=df.year, labels={'color': 'year'}
    )
    # fig.update_traces(marker_size=8)

    return fig


def get_tsne_html_block(df, attributes, class_name='tsne-plot-block'):
    return html.Div(
        children=[
            html.Div(children='t-SNE all data, colored by year', className='plot-title'),
            # html.Div(children=configuration_dict['text_block_text'], className='text-block'),

            html.Div(
                children=[
                    # visual adjustments for the graph
                    dcc.Graph(
                        figure=get_tsne_plot(df, attributes),
                        id='tsne-plot-2',
                        className='tsne-plot',
                        config={'displayModeBar': False}
                    )
                ],
                className='tsne-plot-module'
            ),
        ],
        className=class_name
    )


berlin_lor_prognoseraume_geojson = json.load(open('data/geojson/berlin-lor.prognoseraeume.geojson', 'r', encoding='utf-8'))
