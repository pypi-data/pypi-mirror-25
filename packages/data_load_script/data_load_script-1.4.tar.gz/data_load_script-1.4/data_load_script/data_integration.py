import pandas as pd
from item_upc_generator import assign_item_number, assign_upc_number
from business_logic import *


#add artist_code
def extract_rl_info(nrl_table):
    #NRL table, attributes: image_code, title, release_date
    artist_code=nrl_table.iloc[0,0]
    image_code=nrl_table.iloc[0,1]
    title=nrl_table.iloc[0,2]
    release_date=nrl_table.iloc[0,3]

    return artist_code, image_code, title, release_date


def convert_cnu_puf(input_main_table):
    for index, row in input_main_table.iterrows():
        if row['item_category'] == 'CNU' or row['item_category'] == 'CNU_G':
            input_main_table.set_value(index, 'item_category', 'UFRCAN')

        if row['item_category'] == 'PUF' or row['item_category'] == 'PUF_G':
            input_main_table.set_value(index, 'item_category', 'UFMPAP')

    return input_main_table


#processing data

#generate 3 new frame with different item_category

#the CGH/PPS frame
def update_nrl_variation(nrl_variation,last_item_number,last_upc_number, artist_code, image_code, title, release_date, strechBar):
    cgh_pps=nrl_variation.copy(deep=True)

    #use replace approach
    cgh_pps['item_category']=cgh_pps['item_category'].replace(['CER'],['CGH'])
    cgh_pps['item_category']=cgh_pps['item_category'].replace(['ZPC'],['PPS'])

    #the CNU/PUF frame
    cnu_puf=nrl_variation.copy(deep=True)

    #use replace approach
    cnu_puf['item_category']=cnu_puf['item_category'].replace(['CER'],['CNU'])
    cnu_puf['item_category']=cnu_puf['item_category'].replace(['ZPC'],['PUF'])


    #the ITG1 and ITG2 frame
    itg1_itg2=nrl_variation.copy(deep=True)
    itg1_itg2['item_category']=itg1_itg2['item_category'].replace(['CER'],['CNU_G'])
    itg1_itg2['item_category']=itg1_itg2['item_category'].replace(['ZPC'],['PUF_G'])

    #the NPL frame
    npl=pd.DataFrame(columns=['edition','item_category','size','edition_size'])
    npl=npl.append(nrl_variation.iloc[0])

    npl['item_category']=npl['item_category'].replace(['CER'],['NPL'])

    npl=npl[npl['item_category']=='NPL']

    #modify npl features
    npl.iloc[0]['size']='0X0'
    npl.iloc[0]['edition']='ALL'

    nrl_variation=pd.concat([nrl_variation,cgh_pps,cnu_puf,itg1_itg2,npl])

    nrl_variation=nrl_variation.sort_values('size', ascending=True)

    #re-set the index
    index_range=list(range(0,len(nrl_variation)))
    nrl_variation.index=index_range

    # processing data

    # assign item_number and upc_number to the items

    # add two columns
    nrl_variation['item_number'] = ''  # add item_number
    nrl_variation['upc_number'] = ''
    nrl_variation['item_number'].astype('str')


    # update ITG item_number for regular item_category
    # update CNU_G and PUF_G number

    nrl_variation=assign_item_number(nrl_variation, last_item_number)

    # update upc number
    nrl_variation=assign_upc_number(nrl_variation, last_upc_number)

    # add the index column
    last_variation_index = 0

    start_variation_index = last_variation_index + 1
    nrl_variation['variation_id'] = range(start_variation_index, len(nrl_variation) + start_variation_index)

    # add the title column
    nrl_variation['title'] = title

    # add the image code column
    nrl_variation['image_code'] = image_code

    nrl_variation['artist_code'] = artist_code

    # change the order of columns
    nrl_variation = nrl_variation[
        ['variation_id', 'title', 'edition', 'item_category', 'size', 'edition_size', 'item_number', 'upc_number',
         'image_code', 'artist_code']]

    nrl_variation['description'] = nrl_variation['item_category'] + ' ' + nrl_variation['title'] + ' ' + nrl_variation[
        'size'] + ' ' + nrl_variation['edition'] + ' ED/SIZE ' + nrl_variation['edition_size'].apply(str)
    nrl_variation['image_code_description'] = nrl_variation['image_code'] + ' ' + nrl_variation['title']

    nrl_variation['item_number_ex'] = nrl_variation['item_number']
    nrl_variation['unit_price'] = 0
    nrl_variation['cost'] = ''
    # nrl_variation['image_code']=image_code
    nrl_variation['release_date'] = release_date

    # calculate cost for each row
    for index, row in nrl_variation.iterrows():
        if row[3] == 'CNU':
            nrl_variation.set_value(index, 'cost', cnu_cost(row['edition'], row['size'], strechBar))

        if row[3] == 'CGH':
            nrl_variation.set_value(index, 'cost', cgh_cost(row['edition'], row['size'], strechBar))

        if row[3] == 'CNU_G':
            nrl_variation.set_value(index, 'cost', cnu_g_cost(row['edition'], row['size'], strechBar))

        if row[3] == 'PPS':
            nrl_variation.set_value(index, 'cost', pps_cost(row['size']))

        if row[3] == 'PUF':
            nrl_variation.set_value(index, 'cost', puf_cost(row['size']))

        if row[3] == 'PUF_G':
            nrl_variation.set_value(index, 'cost', puf_g_cost(row['size']))


    return nrl_variation





def generate_main_tables(nrl_variation):
    # output main tables
    output_main_table = nrl_variation[
        ['item_number_ex', 'item_number', 'upc_number', 'description', 'artist_code', 'image_code', 'edition',
         'release_date', 'edition_size', 'size', 'item_category', 'image_code_description', 'unit_price', 'cost']]

    # generate NPL
    output_main_npl = output_main_table[output_main_table['item_category'] == 'NPL']
    output_main_npl = output_main_npl.iloc[[0]]


    # generate CER/ZPC
    output_main_cerzpc = output_main_table[output_main_table['item_category'].isin(['CER', 'ZPC'])]

    # generate CGH/PPS
    output_main_cghpps = output_main_table[output_main_table['item_category'].isin(['CGH', 'PPS'])]

    # generate CNU/PUF
    output_main_cnupuf = output_main_table[output_main_table['item_category'].isin(['CNU', 'PUF'])]


    # generate ITG1/ITG2
    output_main_itg12 = output_main_table[output_main_table['item_category'].isin(['CNU_G', 'PUF_G'])]

    return output_main_npl, output_main_cerzpc, output_main_cghpps, output_main_cnupuf, output_main_itg12



def modify_naming_main_table(output_main_cnupuf, output_main_itg12):
    # modify main table

    for index, row in output_main_cnupuf.iterrows():
        if row['item_category'] == 'CNU' or row['item_category'] == 'CNU_G':
            output_main_cnupuf.set_value(index, 'item_category', 'UFRCAN')

        if row['item_category'] == 'PUF' or row['item_category'] == 'PUF_G':
            output_main_cnupuf.set_value(index, 'item_category', 'UFMPAP')

        if row['description'][0:5] == 'CNU_G':
            to_be_modified = row['description']
            modified = to_be_modified.replace('CNU_G', 'CNU', 1)
            output_main_cnupuf.set_value(index, 'description', modified)

        if row['description'][0:5] == 'PUF_G':
            to_be_modified = row['description']
            modified = to_be_modified.replace('PUF_G', 'PUF', 1)
            output_main_cnupuf.set_value(index, 'description', modified)

    for index, row in output_main_itg12.iterrows():
        if row['item_category'] == 'CNU' or row['item_category'] == 'CNU_G':
            output_main_itg12.set_value(index, 'item_category', 'UFRCAN')

        if row['item_category'] == 'PUF' or row['item_category'] == 'PUF_G':
            output_main_itg12.set_value(index, 'item_category', 'UFMPAP')

        if row['description'][0:5] == 'CNU_G':
            to_be_modified = row['description']
            modified = to_be_modified.replace('CNU_G', 'CNU', 1)
            output_main_itg12.set_value(index, 'description', modified)

        if row['description'][0:5] == 'PUF_G':
            to_be_modified = row['description']
            modified = to_be_modified.replace('PUF_G', 'PUF', 1)
            output_main_itg12.set_value(index, 'description', modified)

    return output_main_cnupuf, output_main_itg12