
def remove_duplicate_item_number(cghpps_main):

    #remove all unneccesary rows: AP, PP, EP, ISN, IAP, IPP, IEP
    cghpps_main=cghpps_main[(cghpps_main['edition']!='AP') & (cghpps_main['edition']!='PP') & (cghpps_main['edition']!='EP') &
                            (cghpps_main['edition']!='ISN') & (cghpps_main['edition']!='IAP') & (cghpps_main['edition']!='IPP') &
                            (cghpps_main['edition']!='IEP')]

    cghpps_main=cghpps_main[(~cghpps_main['edition'].isin(['IDE'])) & (~cghpps_main['edition'].isin(['IEE'])) & (~cghpps_main['edition'].isin(['IGP'])) & (~cghpps_main['edition'].isin(['IJE']))]

    #update edition to 999, and edition size to 0
    for index, row in cghpps_main.iterrows():

        if row['edition']=='SN':
            cghpps_main.set_value(index, 'edition', 999)
            cghpps_main.set_value(index, 'edition_size', 0)

    return cghpps_main