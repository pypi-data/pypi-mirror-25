#lowercase protection: if input data has lowercase characters, it will be converted into upper case
#header protection:if header is wrong, pop up warning
#edition protection:if edition is not in edition list, pop up warning
#size protection:if size is not in size list, pop up warning
#item category protection: if item category is not in item category list, pop up warning

def header_variafication(nrl_table, nrl_variation):

    #verify the headers
    headers=nrl_table.columns.values
    correct_headers=['artist_code','image_code','title','release_date']

    difference=(headers!=correct_headers)

    sum_diff=difference.sum()

    if sum_diff>0:

        print ('nrl_table headers do not match correctly, details:')
        print (difference)

        return None

    headers=nrl_variation.columns.values
    correct_headers=['edition','item_category','size','edition_size']

    difference=(headers!=correct_headers)

    sum_diff=difference.sum()

    if sum_diff>0:

        print ('nrl_variation headers do not match correctly, details:')
        print (difference)

        return None


    return nrl_table, nrl_variation


def item_upc_verificatino(last_item_number, last_upc_number):

    try:
        last_item_number = int(last_item_number)

    except:
        print ('last item number is not integer, please input correct item number')
        return None

    try:
        last_upc_number = int(last_upc_number)

    except:
        print('last upc number is not integer, please input correct item number')
        return None

    if len(str(last_upc_number))!=12:
        print ('The length of last upc number is incorrect. please enter correct upc number')
        print (last_upc_number)

        return None

    #make them string and return
    last_item_number=str(last_item_number)
    last_upc_number=str(last_upc_number)

    return last_item_number, last_upc_number

def nrl_detail_verification(nrl_variation, input_edition_list, input_size_list, input_item_category_list):


    #check edition list
    edition_list=nrl_variation['edition'].tolist()
    for element in edition_list:
        if element not in input_edition_list:
            print ('Warning: ', element, ' is not in default edition list, please check it out.')
            return None

    #check size list
    size_list=nrl_variation['size'].tolist()
    for element in size_list:
        if element not in input_size_list:
            print ('Warning: ', element, ' is not in default size list, please check it out.')
            return None

    #check item category list
    item_category_list=nrl_variation['item_category'].tolist()
    for element in item_category_list:
        if element not in input_item_category_list:
            print ('Warning: ', element, ' is not in default item category list, please check it out.')
            return None


    #check duplicates
    if nrl_variation.duplicated().sum()>0:
        print ('There is duplicated rows in nrl_variation table, below rows are duplicated: ')
        print (nrl_variation[nrl_variation.duplicated()])
        return None


    return nrl_variation

def main_verification(nrl_table, nrl_variation, last_item_number, last_upc_number, input_edition_list, input_size_list, input_item_category_list):

    print ('Verifying the input data sets...')
    nrl_table, nrl_variation=header_variafication(nrl_table, nrl_variation)

    last_item_number, last_upc_number=item_upc_verificatino(last_item_number, last_upc_number)

    nrl_variation=nrl_detail_verification(nrl_variation, input_edition_list, input_size_list, input_item_category_list)

    return nrl_table, nrl_variation, last_item_number, last_upc_number