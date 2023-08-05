import boto3
import pandas as pd
import pandasql
from data_load_script.input_verification import *
from data_load_script.patch_format import *

#load input data including release info and next upc number and next item number
def load_input_data(bucket, path_nrl, path_nrl_variation, path_nexupc, path_nextitem):
    #nrl.csv
    client = boto3.client('s3') #low-level functional API
    obj = client.get_object(Bucket=bucket, Key=path_nrl)
    lines=obj['Body'].read()

    #write the bytes to csv, then read it back
    ofile  = open('nrl.csv', "wb")
    ofile.write(lines)
    ofile.close()

    #read it back
    nrl_table=pd.read_csv('nrl.csv')

    #nrl_variation.csv
    client = boto3.client('s3') #low-level functional API
    obj = client.get_object(Bucket=bucket, Key=path_nrl_variation)
    lines=obj['Body'].read()

    #write the bytes to csv, then read it back
    ofile  = open('nrl_variation.csv', "wb")
    ofile.write(lines)
    ofile.close()

    nrl_variation=pd.read_csv('nrl_variation.csv')

    nrl_variation['size']=nrl_variation['size'].str.lower()

    #NEXTUPCc.csv
    client = boto3.client('s3') #low-level functional API
    obj = client.get_object(Bucket=bucket, Key=path_nexupc)
    lines=obj['Body'].read()


    #write the bytes to csv, then read it back
    ofile  = open('NEXTUPCc.csv', "wb")
    ofile.write(lines)
    ofile.close()

    last_upc_number=pd.read_csv('NEXTUPCc.csv',header=None)
    last_upc_number=str(last_upc_number.iloc[0,0])


    #NEXTITEMc.csv
    client = boto3.client('s3') #low-level functional API
    obj = client.get_object(Bucket=bucket, Key=path_nextitem)
    lines=obj['Body'].read()


    #write the bytes to csv, then read it back
    ofile  = open('NEXTITEMc.csv', "wb")
    ofile.write(lines)
    ofile.close()

    last_item_number=pd.read_csv('NEXTITEMc.csv', header=None)
    last_item_number=last_item_number.iloc[0,0]


    #add patch_format
    # add a patch, make x in size upper case
    nrl_variation = patch_x_upper(nrl_variation)


    #verify the integrity of input data
    #currently the three lists are hard coded, future will retrieve data from a single data source
    input_edition_list=['SN','ISN','AP','IAP', 'EP', 'IEP', 'GP', 'IGP', 'PP', 'IPP', 'DE', 'IDE', 'EE', 'IEE', 'JE', 'IJE']
    input_size_list=['8X10','9X12','12X16','12X18','12X24','16X20','18X24','18X27','20X24','18X36','24X30','25.5X34','24X36','24X48','28X42','30X40','30X60','40X60']
    input_item_category_list=['CER', 'ZPC']

    nrl_table, nrl_variation, last_item_number, last_upc_number=main_verification(nrl_table, nrl_variation, last_item_number, last_upc_number, input_edition_list, input_size_list, input_item_category_list)

    return nrl_table, nrl_variation, last_upc_number, last_item_number


def load_strech_bar():
    #load strechbar table
    client = boto3.client('s3') #low-level functional API
    obj = client.get_object(Bucket='absdata', Key='inputdata/STRBAR1c.csv')
    lines=obj['Body'].read()

    #write the bytes to csv, then read it back
    ofile  = open('STRBAR1c.csv', "wb")
    ofile.write(lines)
    ofile.close()

    strechBar=pd.read_csv('STRBAR1c.csv')

    #fil NaN values
    strechBar['Code']=strechBar['Code'].fillna('Other')

    #find out duplicates
    duplicates=pandasql.sqldf('''select A.Item item1, B.Item item2, A.Cost
                        from strechBar A, strechBar B
                        where A.size=B.size and A.IMDSC1=B.IMDSC1 and A.Item != B.Item
    '''
                   )

    duplicates=pandasql.sqldf('''select *
                                    from duplicates
                                    limit (select count(*)/2 from duplicates)
    ''')


    #remove duplicates, update new strechBar table
    strechBar=pandasql.sqldf('''select * from strechBar 
                                where strechBar.Item NOT IN (select item2 from duplicates)
    ''')

    #rename Size to size
    strechBar=strechBar.rename(columns={'Size':'size'})

    #add a patch, make x in size upper case
    strechBar=patch_x_upper(strechBar)

    return strechBar