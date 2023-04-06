# Run this app with `python children_data_dashboard.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import pandas as pd

from dash import html
from dash.dependencies import Input, Output

from children_map_data_factory import load_sprachdefizit_data, load_kita_besuch_data, load_u8_data, load_visuo_motoric_data, load_own_tv_data
from dashboard_utils import *

from data.kids_data.sprachdefizite_einschulung.explanations import explanation

app = dash.Dash(__name__)


# load all data from the factory and slider options accordingly
language_deficit_all_dataset_dicts, language_deficit_slider_options = load_sprachdefizit_data()

kita_besuch_all_dataset_dicts, kita_besuch_slider_options = load_kita_besuch_data()

u8_all_dataset_dicts, u8_slider_options = load_u8_data()

own_tv_all_dataset_dicts, own_tv_slider_options = load_own_tv_data()

visuo_motoric_all_dataset_dicts, visuo_motoric_slider_options = load_visuo_motoric_data()

html_block_configurations = {
    'language-deficit': {
        'block_title': '% Have Language Deficits',
        'text_block_text': explanation,
        'map_id': 'language-deficit-map',
        'dropdown_id': 'year-language-deficit',
        'slider_options': language_deficit_slider_options
    },
    'kita': {
        'block_title': '% Attended more than 2 Years to Kita',
        'text_block_text': explanation,
        'map_id': 'kita-map',
        'dropdown_id': 'year-kita',
        'slider_options': kita_besuch_slider_options
    },
    'u8': {
        'block_title': '% Had U8',
        'text_block_text': explanation,
        'map_id': 'u8-map',
        'dropdown_id': 'year-u8',
        'slider_options': u8_slider_options
    },
    'own-tv': {
        'block_title': '% Have Own TV',
        'text_block_text': explanation,
        'map_id': 'own-tv-map',
        'dropdown_id': 'year-own-tv',
        'slider_options': own_tv_slider_options
    },
    'visuo-motoric': {
        'block_title': '% Have Promiment Visuo-Motoric Disorder',
        'text_block_text': explanation,
        'map_id': 'visuo-motoric-map',
        'dropdown_id': 'year-visuo-motoric',
        'slider_options': visuo_motoric_slider_options
    }
}


merged_dataset = pd.read_csv('data/kids_data/all_data_merged/merged_dataset.csv')

merged_dataset_district_slider = [
    {'label': district, 'value': district}
    for district in merged_dataset['Bezeichnung'].unique()
]

merged_dataset_year_slider = [
    {'label': year, 'value': year}
    for year in merged_dataset['year'].unique()
]

merged_dataset_target_attributes = [
    'have_language_deficit_relative',
    'attended_kita_more_than_2_years_relative',
    'attended_u8_relative', 'have_own_tv_relative',
    'have_prominent_visuo_motoric_disorder_relative'
]

target_options = [
    {'label': var, 'value': var}
    for var in merged_dataset_target_attributes
]

df_with_medians = merged_dataset.copy()

for attribute in merged_dataset_target_attributes:
    df_with_medians[attribute].replace(to_replace=0, value=df_with_medians[attribute].median(), inplace=True)

normalized_dataset = df_with_medians.copy()

# for attribute in merged_dataset_target_attributes:
#     normalized_dataset[attribute].replace(to_replace=0, value=normalized_dataset[attribute].median(), inplace=True)

for attribute in merged_dataset_target_attributes:
    normalized_dataset[attribute] = (normalized_dataset[attribute] - normalized_dataset[attribute].min()) / (normalized_dataset[attribute].max() - normalized_dataset[attribute].min())

target_correlations = normalized_dataset[merged_dataset_target_attributes].corr()

app.layout = html.Div(
    children=[
        html.H1(children='Berlin Children Health & Development Dashboard', id='whatever'),
        html.H2(children='Examining Language Deficits in Berlin LOR-PR districts'),
        html.Div(
            children=[
                html.Div(
                    children=[
                        get_map_html_block(html_block_configurations['language-deficit'], is_large=True),
                        get_map_html_block(html_block_configurations['kita'], is_large=True),
                    ],
                    className='flex-row'
                ),
                html.Div(
                    children=[
                        get_map_html_block(html_block_configurations['u8']),
                        get_map_html_block(html_block_configurations['own-tv']),
                        get_map_html_block(html_block_configurations['visuo-motoric'])
                    ],
                    className='flex-row'
                ),
            ],
            id='maps-flex-container'
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        get_barplot_html_block(2006, 2018),
                        get_barplot_html_block_2(merged_dataset_district_slider)
                    ],
                    className='flex-row'
                )
            ]
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        get_lineplot_html_block(merged_dataset_district_slider, target_options),
                        get_lineplot_html_block_2(target_options, merged_dataset_district_slider)
                    ],
                    className='flex-row'
                )
            ]
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        get_scatter_matrix_html_block(df_with_medians, merged_dataset_target_attributes),
                        get_correlations_html_block(target_correlations)
                    ],
                    className='flex-row'
                )
            ]
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        get_tsne_html_block(merged_dataset, merged_dataset_target_attributes),
                        get_tsne_html_block_2(merged_dataset, merged_dataset_target_attributes, 2006, 2018)
                    ],
                    className='flex-row'
                )
            ]
        ),
    ],
    id='app-body'
)


@app.callback(
    Output(html_block_configurations['language-deficit']['map_id'], 'figure'),
    Input(html_block_configurations['language-deficit']['dropdown_id'], 'value'),
)
def update_language_deficit_map(dataset_dropdown_value):

    fig = get_choropleth_map(language_deficit_all_dataset_dicts, dataset_dropdown_value, reverse_colors=True)
    return fig


@app.callback(
    Output(html_block_configurations['kita']['map_id'], 'figure'),
    Input(html_block_configurations['kita']['dropdown_id'], 'value'),
)
def update_kita_map(dataset_dropdown_value):

    fig = get_choropleth_map(kita_besuch_all_dataset_dicts, dataset_dropdown_value, reverse_colors=False)
    return fig


@app.callback(
    Output(html_block_configurations['u8']['map_id'], 'figure'),
    Input(html_block_configurations['u8']['dropdown_id'], 'value'),
)
def update_u8_map(dataset_dropdown_value):

    fig = get_choropleth_map(u8_all_dataset_dicts, dataset_dropdown_value, reverse_colors=False)
    return fig


@app.callback(
    Output(html_block_configurations['own-tv']['map_id'], 'figure'),
    Input(html_block_configurations['own-tv']['dropdown_id'], 'value'),
)
def update_own_tv_map(dataset_dropdown_value):

    fig = get_choropleth_map(own_tv_all_dataset_dicts, dataset_dropdown_value, reverse_colors=True)
    return fig


@app.callback(
    Output(html_block_configurations['visuo-motoric']['map_id'], 'figure'),
    Input(html_block_configurations['visuo-motoric']['dropdown_id'], 'value'),
)
def update_visuo_motoric_map(dataset_dropdown_value):

    fig = get_choropleth_map(visuo_motoric_all_dataset_dicts, dataset_dropdown_value, reverse_colors=True)
    return fig


@app.callback(
    Output('barplot-1', 'figure'),
    Input('barplot-year-slider', 'value'),
)
def update_barplot(slider_year_value):

    selected_data_by_year = merged_dataset[merged_dataset['year'] == slider_year_value]

    fig = get_barplot(selected_data_by_year, 'All districts by year')
    return fig


@app.callback(
    Output('barplot-2', 'figure'),
    Input('barplot-district-dropdown', 'value'),
)
def update_barplot_2(dropdown_district_value):

    selected_data_by_district = merged_dataset[merged_dataset['Bezeichnung'] == dropdown_district_value]

    fig = get_barplot_2(selected_data_by_district, 'All years by district')
    return fig


@app.callback(
    Output('lineplot-1', 'figure'),
    Input('lineplot-1-vars-checklist', 'value'),
    Input('lineplot-1-district-dropdown', 'value'),
)
def update_lineplot(vars_checklist_options, district_option):

    # selected_data_by_district = merged_dataset[merged_dataset['Bezeichnung'].isin(dropdown_district_value)]
    selected_data_by_district = merged_dataset[merged_dataset['Bezeichnung'] == district_option]
    fig = get_lineplot(selected_data_by_district, vars_checklist_options)
    return fig


@app.callback(
    Output('lineplot-2', 'figure'),
    Input('lineplot-2-district-checklist', 'value'),
    Input('lineplot-2-vars-dropdown', 'value'),
)
def update_lineplot_2(district_checklist_options, vars_dropdown_option):

    selected_data_by_district = merged_dataset[merged_dataset['Bezeichnung'].isin(district_checklist_options)]
    # selected_data_by_district = merged_dataset[merged_dataset['Bezeichnung'] == district_option]
    fig = get_lineplot_2(selected_data_by_district, vars_dropdown_option)
    return fig



@app.callback(
    Output('tsne-plot', 'figure'),
    Input('tsne-year-slider', 'value'),
)
def update_tsne_2(slider_year_value):

    fig = get_tsne_plot_2(merged_dataset, merged_dataset_target_attributes, slider_year_value)

    return fig


if __name__ == '__main__':
    app.run_server(debug=False)
