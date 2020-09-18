import os

import pandas as pd

from functions import objects_from_xml, reduce_dataframe_size, store_as_excel
from classes import REQUIRED_COLUMNS

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


# KVED category - 2.6 GB
# KVED and STAN category - 2GB
# KVED, STAN and FIO category - 2.2GB


if not os.path.exists(SAVE_FOLDER):
    os.mkdir(SAVE_FOLDER)

files = ["C:\\Users\\anton.desiatnykov\\Desktop\\fop_base\\17.1-EX_XML_EDR_UO_11.09.2020.xml",
         "C:\\Users\\anton.desiatnykov\\Desktop\\fop_base\\17.1-EX_XML_EDR_UO_FULL_07.08.2020.xml",
         "C:\\Users\\anton.desiatnykov\\Desktop\\fop_base\\17.2-EX_XML_EDR_FOP_FULL_07.08.2020.xml",
         "C:\\Users\\anton.desiatnykov\\Desktop\\fop_base\\17.2-EX_XML_EDR_FOP_11.09.2020.xml"]

input_file_path = files[0]

objects_list = objects_from_xml(input_file_path)


df = pd.DataFrame([parsed_object.get_data() for parsed_object in objects_list], columns=REQUIRED_COLUMNS)

reduce_dataframe_size(df)
unique_regions = [region[1] for region in df.REGION.unique().dropna() if region[1] is not None]

for region in unique_regions:
    if not region:
        continue
    name = f'{os.path.basename(input_file_path).replace(".", "_").replace(" ","_").replace(".xml", "")}_{region}'
    store_as_excel(df=df.where(df.REGION.str.contains(region)).dropna(), name=f'{SAVE_FOLDER}/{name}')
    # gc.collect()




# if __name__ == '__main__':
#     run()

