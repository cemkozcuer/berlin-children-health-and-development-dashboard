import pandas as pd
from functools import reduce


def create_merged_dataset():

    df_language_deficit = pd.read_csv(
        'data/kids_data/sprachdefizite_einschulung/2008_2018-sprachdefizite_einschulung.csv',
        dtype={'Prognoseraum': str, 'Bezeichnung': str, 'Anteil': float, 'year': str}
    )
    df_language_deficit.rename(columns={'Anteil': 'have_language_deficit_relative'}, inplace=True)

    df_kita = pd.read_csv(
        'data/kids_data/kita_besuch/2006_2018-kita_besuch.csv',
        dtype={'Prognoseraum': str, 'Bezeichnung': str, 'Anteil': float, 'year': str}
    )
    df_kita.rename(columns={'Anteil': 'attended_kita_more_than_2_years_relative'}, inplace=True)

    df_u8 = pd.read_csv(
        'data/kids_data/u8/2006_2018-u8.csv',
        dtype={'Prognoseraum': str, 'Bezeichnung': str, 'Anteil': float, 'year': str}
    )
    df_u8.rename(columns={'Anteil': 'attended_u8_relative'}, inplace=True)

    df_own_tv = pd.read_csv(
        'data/kids_data/eigener_fernseher/2006_2016-eigener_fernseher.csv',
        dtype={'Prognoseraum': str, 'Bezeichnung': str, 'Anteil': float, 'year': str}
    )
    df_own_tv.rename(columns={'Anteil': 'have_own_tv_relative'}, inplace=True)

    df_visuo_motoric = pd.read_csv(
        'data/kids_data/visuomotorik/2006_2018-visuomotorik.csv',
        dtype={'Prognoseraum': str, 'Bezeichnung': str, 'Anteil': float, 'year': str}
    )
    df_visuo_motoric.rename(columns={'Anteil': 'have_prominent_visuo_motoric_disorder_relative'}, inplace=True)

    merged_df = reduce(
        lambda _merged_df, next_df: pd.merge(_merged_df, next_df, how='outer', on=['year', 'Prognoseraum', 'Bezeichnung']),
        [df_kita, df_u8, df_own_tv, df_visuo_motoric],
        df_language_deficit
    )
    merged_df.to_csv('data/kids_data/all_data_merged/merged_dataset.csv')

    return merged_df


create_merged_dataset()
