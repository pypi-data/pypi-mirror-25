import pandas as pd
from data_load_script.business_logic import *
from data_load_script.patch_remove_duplicates import *
import boto3
from io import StringIO


#this function is just for diagnose purpose
def fetch_item_category(item_number, edition, nrl_variation):

    for index, row in nrl_variation.iterrows():

        if item_number==row['item_number'] and edition==row['edition']:

            return row['item_category']


#this is modifed for output spot check columns
def output_bom_tables(nrl_variation, output_main_cghpps, output_main_cnupuf, output_main_itg12, strechBar):

    #hard-code some cost
    canvas_item_number='79973'
    canvas_unit_cost=0.73
    paper_item_number='44990'
    paper_unit_cost=0.37
    name_plate_cost=0.374

    # output bom tables to same folder
    bom_cghpps = pd.DataFrame(
        columns=['item_number_ex', 'item_number', 'item_member_item', 'item_quantity', 'item_unit_cost', 'line_id'])

    for index, row in output_main_cghpps.iterrows():

        if row['item_category'] == 'CGH':
            bom_cghpps = bom_cghpps.append({'item_number_ex': row['item_number_ex'],
                                            'item_number': row['item_number'],
                                            'item_member_item': canvas_item_number,
                                            'item_quantity': canvas_quantity(row['size']),
                                            'item_unit_cost': canvas_unit_cost,
                                            'line_id': 1}, ignore_index=True)

            # strechBar item number and strechBar cost has been changed
            bom_cghpps = bom_cghpps.append({'item_number_ex': row['item_number_ex'],
                                            'item_number': row['item_number'],
                                            'item_member_item': strechBar_item_number(row['edition'], row['size'], strechBar),
                                            'item_quantity': 1,
                                            'item_unit_cost': strechBar_cost(row['edition'], row['size'],strechBar),
                                            'line_id': 2}, ignore_index=True)
        if row['item_category'] == 'PPS':
            bom_cghpps = bom_cghpps.append({'item_number_ex': row['item_number_ex'],
                                            'item_number': row['item_number'],
                                            'item_member_item': paper_item_number,
                                            'item_quantity': paper_quantity(row['size']),
                                            'item_unit_cost': paper_unit_cost,
                                            'line_id': 1}, ignore_index=True)

    bom_cnupuf = pd.DataFrame(
        columns=['item_number_ex', 'item_number', 'item_member_item', 'item_quantity', 'item_unit_cost', 'line_id', 'size', 'edition', 'item_category'])


    for index, row in output_main_cnupuf.iterrows():
        if row['item_category'] == 'CNU':
            # go to the main cghpps table to get the item_number, key is the size and item_category and edition

            item_number_row = nrl_variation[
                (nrl_variation['size'] == row['size']) & (nrl_variation['item_category'] == 'CGH') & (
                nrl_variation['edition'] == row['edition'])]

            item_number_cnu = item_number_row.iloc[0]['item_number']

            bom_cnupuf = bom_cnupuf.append({'item_number_ex': row['item_number_ex'],
                                            'item_number': row['item_number'],
                                            'item_member_item': item_number_cnu,
                                            'item_quantity': 1,
                                            'item_unit_cost': cgh_cost(row['edition'], row['size'], strechBar),
                                            'line_id': 1,
                                            'size': row['size'],
                                            'edition':row['edition'],
                                            'item_category':fetch_item_category(item_number_cnu, row['edition'], nrl_variation)}, ignore_index=True)
            # go to the main cghpps table to get the item_number, key is the size and item_category
            # all CNU items only share one NPL item number
            item_number_row = nrl_variation[nrl_variation['item_category'] == 'NPL']

            item_number_cnu = item_number_row.iloc[0]['item_number']
            item_edition_cnu= item_number_row.iloc[0]['edition'] # for NPL specifically

            bom_cnupuf = bom_cnupuf.append({'item_number_ex': row['item_number_ex'],
                                            'item_number': row['item_number'],
                                            'item_member_item': item_number_cnu,
                                            'item_quantity': 1,
                                            'item_unit_cost': name_plate_cost,
                                            'line_id': 2,
                                            'size': row['size'],
                                            'edition':row['edition'],
                                            'item_category':fetch_item_category(item_number_cnu, item_edition_cnu, nrl_variation)}, ignore_index=True)
        if row['item_category'] == 'PUF':
            # go to the main cghpps table to get the item_number, key is the size and item_category and edition

            item_number_row = nrl_variation[
                (nrl_variation['size'] == row['size']) & (nrl_variation['item_category'] == 'PPS') & (
                nrl_variation['edition'] == row['edition'])]

            item_number_cnu = item_number_row.iloc[0]['item_number']

            bom_cnupuf = bom_cnupuf.append({'item_number_ex': row['item_number_ex'],
                                            'item_number': row['item_number'],
                                            'item_member_item': item_number_cnu,
                                            'item_quantity': 1,
                                            'item_unit_cost': pps_cost(row['size']),
                                            'line_id': 1,
                                            'size': row['size'],
                                            'edition':row['edition'],
                                            'item_category':fetch_item_category(item_number_cnu, row['edition'], nrl_variation)}, ignore_index=True)


    bom_itg12 = pd.DataFrame(
        columns=['item_number_ex', 'item_number', 'item_member_item', 'item_quantity', 'item_unit_cost', 'line_id', 'size', 'edition', 'item_category'])

    for index, row in output_main_itg12.iterrows():
        if row['item_category'] == 'CNU_G':
            # go to the main nrl_variation table to get the item_number, key is the size and item_category and the edition

            item_number_row = nrl_variation[
                (nrl_variation['size'] == row['size']) & (nrl_variation['item_category'] == 'CNU') & (
                nrl_variation['edition'] == row['edition'])]

            item_number_cnu = item_number_row.iloc[0]['item_number']

            bom_itg12 = bom_itg12.append({'item_number_ex': row['item_number_ex'],
                                          'item_number': row['item_number'],
                                          'item_member_item': item_number_cnu,
                                          'item_quantity': 1,
                                          'item_unit_cost': cnu_cost(row['edition'], row['size'], strechBar),
                                          'line_id': 1,
                                          'size': row['size'],
                                          'edition': row['edition'],
                                          'item_category': fetch_item_category(item_number_cnu, row['edition'], nrl_variation)}, ignore_index=True)

            # go to the main nrl_variation table to get the item_number, key is the size and item_category and the edition
            item_number_row = nrl_variation[
                (nrl_variation['size'] == row['size']) & (nrl_variation['item_category'] == 'CER') & (
                nrl_variation['edition'] == row['edition'])]

            item_number_cnu = item_number_row.iloc[0]['item_number']
            bom_itg12 = bom_itg12.append({'item_number_ex': row['item_number_ex'],
                                          'item_number': row['item_number'],
                                          'item_member_item': item_number_cnu,
                                          'item_quantity': 1,
                                          'item_unit_cost': 0,
                                          'line_id': 2,
                                          'size': row['size'],
                                          'edition': row['edition'],
                                          'item_category': fetch_item_category(item_number_cnu, row['edition'], nrl_variation)}, ignore_index=True)
        if row['item_category'] == 'PUF_G':
            # go to the main cghpps table to get the item_number, key is the size and item_category and edition
            item_number_row = nrl_variation[
                (nrl_variation['size'] == row['size']) & (nrl_variation['item_category'] == 'PUF') & (
                nrl_variation['edition'] == row['edition'])]

            item_number_cnu = item_number_row.iloc[0]['item_number']

            bom_itg12 = bom_itg12.append({'item_number_ex': row['item_number_ex'],
                                          'item_number': row['item_number'],
                                          'item_member_item': item_number_cnu,
                                          'item_quantity': 1,
                                          'item_unit_cost': puf_cost(row['size']),
                                          'line_id': 1,
                                          'size': row['size'],
                                          'edition': row['edition'],
                                          'item_category': fetch_item_category(item_number_cnu, row['edition'], nrl_variation)}, ignore_index=True)

            # go to the main cghpps table to get the item_number, key is the size and item_category
            item_number_row = nrl_variation[
                (nrl_variation['size'] == row['size']) & (nrl_variation['item_category'] == 'ZPC') & (
                nrl_variation['edition'] == row['edition'])]

            item_number_cnu = item_number_row.iloc[0]['item_number']

            bom_itg12=bom_itg12.append({'item_number_ex': row['item_number_ex'],
                              'item_number': row['item_number'],
                              'item_member_item': item_number_cnu,
                              'item_quantity': 1,
                              'item_unit_cost': 0,
                              'line_id': 2,
                              'size': row['size'],
                              'edition': row['edition'],
                              'item_category': fetch_item_category(item_number_cnu, row['edition'], nrl_variation)}, ignore_index=True)


    # write to S3
    csv_buffer = StringIO()
    bom_cghpps.to_csv(csv_buffer, index=False)
    s3_resource = boto3.resource('s3')
    s3_resource.Object('absdata', 'outputdata/ACGHCPN.csv').put(Body=csv_buffer.getvalue())

    # write to S3
    csv_buffer = StringIO()
    bom_cnupuf.to_csv(csv_buffer, index=False)
    s3_resource = boto3.resource('s3')
    s3_resource.Object('absdata', 'outputdata/ACNUCPN.csv').put(Body=csv_buffer.getvalue())

    # write to S3
    csv_buffer = StringIO()
    bom_itg12.to_csv(csv_buffer, index=False)
    s3_resource = boto3.resource('s3')
    s3_resource.Object('absdata', 'outputdata/AITGCPN.csv').put(Body=csv_buffer.getvalue())

    return bom_cghpps,bom_cnupuf,bom_itg12





def output_main_tables(output_main_npl, output_main_cerzpc, output_main_cghpps, output_main_cnupuf, output_main_itg12):
    #output main tables
    #write to S3
    csv_buffer = StringIO()
    output_main_npl.to_csv(csv_buffer, index=False)
    s3_resource = boto3.resource('s3')
    s3_resource.Object('absdata', 'outputdata/ANPLMAN.csv').put(Body=csv_buffer.getvalue())

    #write to S3
    csv_buffer = StringIO()
    output_main_cerzpc.to_csv(csv_buffer, index=False)
    s3_resource = boto3.resource('s3')
    s3_resource.Object('absdata', 'outputdata/ACERMAN.csv').put(Body=csv_buffer.getvalue())

    #write to S3
    csv_buffer = StringIO()

    output_main_cghpps=remove_duplicate_item_number(output_main_cghpps)

    output_main_cghpps.to_csv(csv_buffer, index=False)
    s3_resource = boto3.resource('s3')
    s3_resource.Object('absdata', 'outputdata/ACGHMAN.csv').put(Body=csv_buffer.getvalue())

    #write to S3
    csv_buffer = StringIO()
    output_main_cnupuf.to_csv(csv_buffer, index=False)
    s3_resource = boto3.resource('s3')
    s3_resource.Object('absdata', 'outputdata/ACNUMAN.csv').put(Body=csv_buffer.getvalue())

    #write to S3
    csv_buffer = StringIO()
    output_main_itg12.to_csv(csv_buffer, index=False)
    s3_resource = boto3.resource('s3')
    s3_resource.Object('absdata', 'outputdata/AITGMAN.csv').put(Body=csv_buffer.getvalue())

def output_cer_num_table(cernum):

    csv_buffer = StringIO()
    cernum.to_csv(csv_buffer, index=False)
    s3_resource = boto3.resource('s3')
    s3_resource.Object('absdata', 'outputdata/ACERNUM.csv').put(Body=csv_buffer.getvalue())
