"""
This factory is tailored to serve children_data_dashboard.py by loading data
for a plotly choropleth map where the data can be switched via sliders.
"""

import pandas as pd


def create_data_set_dict(df, title, data_key, location_key, hover_name_key, dropdown_label, dropdown_value):
    return {
        'df': df,
        'title': title,
        'data_key': data_key,
        'location_key': location_key,
        'hover_name_key': hover_name_key,
        'dropdown_label': dropdown_label,
        'dropdown_value': dropdown_value
    }


def get_data(dataset_path, start_year, end_year):

    df_all_data = pd.read_csv(
        dataset_path,
        dtype={'Prognoseraum': str, 'Bezeichnung': str, 'Anteil': float, 'year': str}
    )

    data_key_value_pairs = []

    for year in range(start_year, end_year + 1):

        year_as_str = str(year)
        df_by_year = df_all_data[df_all_data['year'] == year_as_str]

        title = year_as_str
        data_key = 'Anteil'
        location_key = 'Prognoseraum'
        hover_name_key = 'Bezeichnung'
        dropdown_label = year_as_str  # title
        dropdown_value = f'dp_value_{year_as_str}'

        data_set_dict = create_data_set_dict(
            df_by_year, title, data_key, location_key, hover_name_key, dropdown_label, dropdown_value
        )

        data_key_value_pairs.append((dropdown_value, data_set_dict))

    return data_key_value_pairs


def get_slider_options(all_dataset_dicts):

    slider_options = {
        dataset_dict['dropdown_label']: dataset_dict['dropdown_label']
        for dataset_dict in all_dataset_dicts.values()
    }

    return slider_options


def load_data_and_slider_options(data_path, start_year, end_year):
    all_data = {}

    dataset_pairs = get_data(data_path, start_year, end_year)

    for dataset_dropdown_value, dataset_dict in dataset_pairs:
        all_data[dataset_dropdown_value] = dataset_dict

    slider_options = get_slider_options(all_data)

    return all_data, slider_options


def load_sprachdefizit_data():
    return load_data_and_slider_options('data/kids_data/sprachdefizite_einschulung/2008_2018-sprachdefizite_einschulung.csv', 2008, 2018)


def load_kita_besuch_data():
    return load_data_and_slider_options('data/kids_data/kita_besuch/2006_2018-kita_besuch.csv', 2006, 2018)


def load_u8_data():
    return load_data_and_slider_options('data/kids_data/u8/2006_2018-u8.csv', 2006, 2018)


def load_own_tv_data():
    return load_data_and_slider_options('data/kids_data/eigener_fernseher/2006_2016-eigener_fernseher.csv', 2006, 2016)


def load_visuo_motoric_data():
    return load_data_and_slider_options('data/kids_data/visuomotorik/2006_2018-visuomotorik.csv', 2006, 2018)
