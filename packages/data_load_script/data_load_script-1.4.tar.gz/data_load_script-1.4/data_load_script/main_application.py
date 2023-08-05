from input_data_handle import load_input_data,load_strech_bar
from data_integration import *
from output_data_handle import output_bom_tables, output_main_tables, output_cer_num_table
from patch_cer_number import generate_cer_num_table


# load input data

def main():
    print('loading input data from Amazon S3...')
    nrl_table, nrl_variation, last_upc_number, last_item_number = load_input_data('absdata', 'inputdata/nrl.csv',
                                                                                  'inputdata/nrl_variation.csv',
                                                                                  'inputdata/NEXTUPCc.csv',
                                                                                  'inputdata/NEXTITEMc.csv')

    if nrl_table is not None and nrl_variation is not None and last_upc_number is not None and last_item_number is not None:
        print ('input data has been verified')

    else:
        print ('Input data is not qualified, please check corresponding data set and re-launch the program')
        return

    # load strech bar data
    print('loading strech bar data...')
    strechBar = load_strech_bar()

    # extract release info
    print('extract release information...')
    artist_code, image_code, title, release_date = extract_rl_info(nrl_table)



    # generate new nrl_variation
    print('integrating data...')
    nrl_variation = update_nrl_variation(nrl_variation, last_item_number, last_upc_number, artist_code, image_code, title, release_date,
                                         strechBar)

    print('creating master data file for spot check')
    nrl_variation.to_csv('master_data.csv', index=False)  # for diagnose use

    # generate main tables
    print('preparing main tables...')
    output_main_npl, output_main_cerzpc, output_main_cghpps, output_main_cnupuf, output_main_itg12 = generate_main_tables(
        nrl_variation)

    # output bom tables
    print('uploading bom tables to Amazon S3...')
    bom_cghpps, bom_cnupuf, bom_itg12 = output_bom_tables(nrl_variation, output_main_cghpps, output_main_cnupuf,
                                                          output_main_itg12, strechBar)

    # modify the naming of output main tables, regarding CNU/PUF and Item Group
    output_main_cnupuf, output_main_itg12 = modify_naming_main_table(output_main_cnupuf, output_main_itg12)

    # output main tables to S3
    print('uploading main tables to Amazon S3...')
    output_main_tables(output_main_npl, output_main_cerzpc, output_main_cghpps, output_main_cnupuf, output_main_itg12)

    # add patch 'patch_cer_number.py'
    print ('adding patch "patch_cer_num"...')
    output_cer_num=generate_cer_num_table(output_main_cerzpc)

    print('uploading ACERNUM table')
    output_cer_num_table(output_cer_num)

    print('successfully finished.')


#run the main function
main()