import os

import xml.etree.ElementTree as etree
import pandas as pd
import xlsxwriter

REQUIRED_COLUMNS = ("NAME", "CONTACTS", "SIGNERS", "PRIMARY ACTIVITY", "AUTHORIZED_CAPITAL", "EDRPOU", "STAN",
                    "REGISTRATION", "ADDRESS")


def dataframe_from_xml(path):
    print('Creating dataframe from xml ')

    xml_tree = etree.parse(path)
    xml_root = xml_tree.getroot()

    return pd.DataFrame({elem.tag: elem.text for elem in node} for node in xml_root)


def regions_from_dataframe(df):
    print('Dividing by regions')
    # Filter unique regions from dataframe by ' обл.' string and strips them
    # TODO: Add Crimea, Kyiv and so on!!!

    unique_regions = pd.Series(pd.unique(df['ADDRESS'].str.split(',', expand=True)[2].str.strip()))

    return unique_regions.where(unique_regions.str.contains(' обл.')).dropna(inplace=False)


def store_as_excel(df, name, rows_per_file=100000):
    for i in range(1, len(df) // rows_per_file):
        # save files storing X rows in each\

        with pd.ExcelWriter(f'{name}_part_{i}.xlsx', engine='xlsxwriter') as writer:
            print(f'Trying to save: "{name}_part_{i}.xlsx"')
            df[:i*rows_per_file].to_excel(writer, engine='xlsxwriter')
            print(f'File {name}_part_{i} saved')

    # save file with remaining rows
    with pd.ExcelWriter(f'./{name}_part_last.xlsx', engine='xlsxwriter') as writer:
        df[:-len(df) % rows_per_file].to_excel(writer)
        print(f'./{name}_part_last.xlsx')


# 17.2-EX_XML_EDR_FOP_11.09.2020.xml
# ['FIO', 'ADDRESS', 'KVED', 'STAN'] df[pd.unique(df['ADDRESS'].str.split(',', expand=True)[2]).notnull()]

# 17.1-EX_XML_EDR_UO_11.09.2020.xml
# ['NAME', 'SHORT_NAME', 'EDRPOU', 'ADDRESS', 'KVED', 'BOSS', 'BENEFICIARIES', 'FOUNDERS', 'STAN']

# 17.1-EX_XML_EDR_UO_FULL_07.08.2020.xml
#

# 17.2-EX_XML_EDR_FOP_FULL_07.08.2020.xml
#

input_file_path = "C:\\Users\\anton.desiatnykov\\Desktop\\fop_base\\17.2-EX_XML_EDR_FOP_11.09.2020.xml"

df = dataframe_from_xml(input_file_path)

import pdb; pdb.set_trace()

regions = regions_from_dataframe(df)


for region in regions:
    name = f'{os.path.basename(input_file_path).replace(" ","_").replace(".xml", "")}_{region}'
    store_as_excel(df=df.where(df['ADDRESS'].str.contains(region)).dropna(), name=name)



import pdb; pdb.set_trace()
# -------------

