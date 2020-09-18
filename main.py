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


def run(input_file_path):
    if not os.path.exists(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)

    objects_list = objects_from_xml(input_file_path)


    df = pd.DataFrame([parsed_object.get_data() for parsed_object in objects_list], columns=REQUIRED_COLUMNS)

    # del(objects_list)

    reduce_dataframe_size(df)
    try:
        unique_regions = [region[1] for region in df.REGION.unique() if region[1] is not None]
    except:
        import pdb; pdb.set_trace()

    for region in unique_regions:
        # if not region:
        #     continue
        import pdb;
        pdb.set_trace()
        try:
            name = f'{os.path.basename(input_file_path).replace(".", "_").replace(" ","_").replace(".xml", "")}_{region}'
            store_as_excel(df=df.where(df.ADDRESS.str.contains(region)).dropna(), name=f'{SAVE_FOLDER}/{name}')
        except:
            import pdb;
            pdb.set_trace()
            # store_as_excel(df=df[df['ADDRESS'].astype('str').str.contains('Вінницька')], name=f'{SAVE_FOLDER}/{name}')
            # df[df['ADDRESS'].astype('str').str.contains('Вінницька')]
    # import gc
    # gc.collect()


if __name__ == '__main__':
    # files = ["C:\\Users\\anton.desiatnykov\\Desktop\\fop_base\\17.1-EX_XML_EDR_UO_11.09.2020.xml",
    #          "C:\\Users\\anton.desiatnykov\\Desktop\\fop_base\\17.1-EX_XML_EDR_UO_FULL_07.08.2020.xml",
    #          "C:\\Users\\anton.desiatnykov\\Desktop\\fop_base\\17.2-EX_XML_EDR_FOP_FULL_07.08.2020.xml",
    # files=[ "C:\\Users\\anton.desiatnykov\\Desktop\\fop_base\\17.2-EX_XML_EDR_FOP_11.09.2020.xml"]

    # [run(file) for file in files]
    run("C:\\Users\\anton.desiatnykov\\Desktop\\fop_base\\17.1-EX_XML_EDR_UO_11.09.2020.xml")
