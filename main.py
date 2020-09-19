import os

import pandas as pd

from classes import REQUIRED_COLUMNS
from functions import objects_from_xml, reduce_dataframe_size, store_as_excel

SAVE_FOLDER = './output_files'


# 17.2-EX_XML_EDR_FOP_11.09.2020.xml
# ['FIO', 'ADDRESS', 'KVED', 'STAN'] df[pd.unique(df['ADDRESS'].str.split(',', expand=True)[2]).notnull()]

# 17.1-EX_XML_EDR_UO_11.09.2020.xml
# ['NAME', 'SHORT_NAME', 'EDRPOU', 'ADDRESS', 'KVED', 'BOSS', 'BENEFICIARIES', 'FOUNDERS', 'STAN']

# 17.1-EX_XML_EDR_UO_FULL_07.08.2020.xml

# 17.2-EX_XML_EDR_FOP_FULL_07.08.2020.xml
#
# df.memory_usage(index=True).sum() / 1024 * 2
# df.info(memory_usage='deep')

def parse_tov():
    first_objects_list = objects_from_xml(
        "C:\\Users\\anton.desiatnykov\\Desktop\\fop_base\\17.1-EX_XML_EDR_UO_11.09.2020.xml")
    first_df = pd.DataFrame([parsed_object.get_data() for parsed_object in first_objects_list],
                            columns=REQUIRED_COLUMNS)
    reduce_dataframe_size(first_df)
    # print('first df done')

    second_objects_list = objects_from_xml(
        "C:\\Users\\anton.desiatnykov\\Desktop\\fop_base\\17.1-EX_XML_EDR_UO_FULL_07.08.2020.xml")
    second_df = pd.DataFrame([parsed_object.get_data() for parsed_object in second_objects_list],
                             columns=REQUIRED_COLUMNS)

    reduce_dataframe_size(second_df)

    print('second df done')
    # first_df[first_df.CONTACTS.notna()]

    df = pd.concat([first_df, second_df]).groupby('NAME', sort=False).sum(min_count=1)

    del first_df, second_df

    df = df[df.CONTACTS.notna()][df.CONTACTS != 0]
    if 'STAN' in df.columns:
        df = df[df.STAN != 'припинено']

    # import pdb; pdb.set_trace()

    input_file_path = '17.1-EX_XML_EDR_FOP_'
    for region in df.REGION.unique():
        name = f'{os.path.basename(input_file_path).replace(".", "_").replace(" ", "_").replace(".xml", "")}_{region}'
        store_as_excel(df=df[df.REGION == region], name=f'{SAVE_FOLDER}/{name}')


if __name__ == '__main__':
    # files = ["C:\\Users\\anton.desiatnykov\\Desktop\\fop_base\\17.1-EX_XML_EDR_UO_11.09.2020.xml",
    #          "C:\\Users\\anton.desiatnykov\\Desktop\\fop_base\\17.1-EX_XML_EDR_UO_FULL_07.08.2020.xml",
    #          "C:\\Users\\anton.desiatnykov\\Desktop\\fop_base\\17.2-EX_XML_EDR_FOP_FULL_07.08.2020.xml",
    # files=[ "C:\\Users\\anton.desiatnykov\\Desktop\\fop_base\\17.2-EX_XML_EDR_FOP_11.09.2020.xml"]



    parse_tov()


