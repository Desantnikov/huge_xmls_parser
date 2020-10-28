import os

import pandas as pd

from classes import REQUIRED_COLUMNS
from functions import objects_from_xml, reduce_dataframe_size, store_as_excel

SAVE_FOLDER = './output_files'


def parse_tov():
    """ Task was to parse, concatenate, filter and aggregate a sequence of ~9GB xml files
        then data should be divided by regions and saved to corresponding excel files
        max 100k of rows in each
    """

    first_objects_list = objects_from_xml("./17.2-EX_XML_EDR_FOP_11.09.2020.xml")
    first_df = pd.DataFrame([parsed_object.get_data() for parsed_object in first_objects_list],
                            columns=REQUIRED_COLUMNS)
    reduce_dataframe_size(first_df)
    print('first xml loaded')

    second_objects_list = objects_from_xml("./17.2-EX_XML_EDR_FOP_FULL_07.08.2020.xml")
    second_df = pd.DataFrame([parsed_object.get_data() for parsed_object in second_objects_list],
                             columns=REQUIRED_COLUMNS)

    reduce_dataframe_size(second_df)
    print('second xml loaded')

    df = pd.concat([first_df, second_df]).groupby('NAME', sort=False).sum(min_count=1)
    print('Dataframes concatenated')

    del first_df, second_df
    print('Initial dataframes deleted')

    df = df[df.CONTACTS.notna()][df.CONTACTS != 0]
    print('Dataframe filtered')

    output_file = 'FOP_LIST'
    for region in df.REGION.unique():
        name = f'{os.path.basename(output_file).replace(".", "_").replace(" ", "_").replace(".xml", "")}_{region}'
        store_as_excel(df=df[df.REGION == region], name=f'{SAVE_FOLDER}/{name}')


if __name__ == '__main__':
    parse_tov()


