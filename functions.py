import gc
import types

import pandas as pd
import xml.etree.ElementTree as etree

from classes import SlotDict


REPORTING_FREQUENCY = 500000  # report every X lines
COLUMNS_TYPES = {'PRIMARY_ACTIVITY': 'category',
                 'STAN': 'category',
                 # 'AUTHORIZED_CAPITAL': 'int16',
                 'KVED': 'category',
                 'CODE': 'category',}
                 # 'REGION': 'category'}
                 # 'EDRPOU': 'int16'}


def reduce_dataframe_size(df):
    # import pdb;
    # pdb.set_trace()
    print(f'Memory used before reducing:')
    df.info(memory_usage="deep")
    for column, type_ in COLUMNS_TYPES.items():
        if column in df.columns:
            # print(f'{column}')
            df[column] = df[column].astype(type_)
    print('After reducing:')
    df.info(memory_usage="deep")


def objects_from_xml(path):
    print('Creating list with objects from xml ')

    previous_elem = types.SimpleNamespace()
    previous_elem.tag = None
    activity = ''
    objects_list = []

    for counter, (event, elem) in enumerate(etree.iterparse(path, events=['start'])):
        # if counter > 1000:
        #     break
        # import pdb; pdb.set_trace()
        if not counter % REPORTING_FREQUENCY:
            print(f'Processing {counter}"th element')
            # print(f'Elem: {elem.tag} \r\nText: {elem.text or None}')

        if all((previous_elem.tag in ['SUBJECT', 'RECORD'], elem.tag == 'NAME')):
            # Several 'NAME' fields may be inside one organization's data, so need to be sure that we process
            # exactly organization's name that is usually the first in the SUBJECT block
            objects_list.append(SlotDict(name=elem.text))

        elif elem.tag in ('DATA', 'SUBJECT'):
            # Skip useless tags
            previous_elem = elem
            continue

        elif all((previous_elem.tag == 'ACTIVITY_KIND', elem.tag == 'CODE')):
            # Store code (KVED) in case current activity will turn out to be primary
            activity = f'{elem.text}'

        elif all((previous_elem.tag == 'CODE', elem.tag == 'NAME')):
            # Store also name in case this activity will turn out to be primary
            activity = f'{activity} {elem.text}'

        elif all((previous_elem.tag == 'NAME', elem.tag == 'PRIMARY', elem.text == 'так')):
            # Set primary activity in case it is it
            objects_list[-1].PRIMARY_ACTIVITY = activity

        elif elem.tag == 'SIGNER':
            # Add signer to SIGNERS
            objects_list[-1].add_signer(elem.text)

        elif objects_list and elem.tag in objects_list[-1].__slots__:
            # Set attributes (if it's not empty) where they match slot's names and not set yet
            setattr(objects_list[-1], elem.tag, elem.text)

            if 'ADDRESS' in elem.tag:
                objects_list[-1].set_region()

        previous_elem = elem

    return objects_list


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

