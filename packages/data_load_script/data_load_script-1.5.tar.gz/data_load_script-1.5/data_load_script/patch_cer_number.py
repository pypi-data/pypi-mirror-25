import pandas as pd


def generate_cer_num_table(acerman_table):

    cernum=pd.DataFrame(columns=['item_number_ex', 'item_number', 'sequential_num', 'quantity', 'item_category', 'size', 'edition'])

    # sequantial_num = 1

    for index, row in acerman_table.iterrows():

        item_number_ex=row['item_number_ex']
        item_number=row['item_number']
        quantity=row['edition_size']
        item_category=row['item_category']
        size=row['size']
        edition=row['edition']

        # for x in range(0,quantity):
        #
        #     cernum=cernum.append({'item_number_ex':item_number_ex, 'item_number':item_number, 'sequantial_number':sequantial_num, 'item_category':item_category, 'size':size, 'edition':edition}, ignore_index=True)
        #     sequantial_num=sequantial_num+1

        temp=pd.DataFrame({'item_number_ex':item_number_ex, 'item_number':item_number, 'sequential_num':range(1,quantity+1,1), 'quantity':quantity, 'item_category':item_category, 'size':size, 'edition':edition})

        cernum=cernum.append(temp)

    #re-arange the order of the columns
    cernum=cernum[['item_number_ex', 'item_number', 'sequential_num', 'quantity', 'item_category', 'size', 'edition']]

    return cernum

