import pandas as pd


# define a function to generate upc number, input must always be string
def generate_upc_number(last_upc_number):
    # generate new upc number
    # prepare

    pre_number = int(last_upc_number[0:11]) + 1

    new_string = str(pre_number) + last_upc_number[11]

    # step 1, sum odd digit and times 3
    sum_odd = 0

    for x in range(0, 12, 2):
        sum_odd = sum_odd + int(new_string[x])

    step1 = sum_odd * 3

    # step 2, sum even digit
    sum_even = 0

    # for even number, we do not want the last one.
    for x in range(1, 11, 2):
        sum_even = sum_even + int(new_string[x])

    step2 = sum_even

    step2 = step1 + step2

    # step 3, get the last digit of step 2
    last_digit = step2 % 10

    step3 = last_digit

    # step 4, get the difference between 10 and result of step 3
    step4 = (10 - step3)%10

    # step5, get the final result
    new_upc = str(pre_number) + str(step4)

    return new_upc

#last_item_number should always be string except when manipulating
def generate_item_number(last_item_number):

    last_item_number=int(last_item_number)+1

    last_item_number=str(last_item_number)

    return last_item_number


def set_CNU_G_item_number(size, edition, nrl_variation):

    item_number = ''
    # use item_category and size to locate the item_number, now should include edition
    for index, row in nrl_variation.iterrows():
        if row['item_category'] == 'CNU' and row['size'] == size and row['edition'] == edition:
            item_number = str(row['item_number']) + '_G'

    return item_number


def set_PUF_G_item_number(size, edition, nrl_variation):

    item_number=''
    # use item_category and size to locate the item_number, now should include edition
    for index, row in nrl_variation.iterrows():
        if row['item_category'] == 'PUF' and row['size'] == size and row['edition'] == edition:
            item_number = str(row['item_number']) + '_G'

    return item_number


def set_skipped_item_number(size, nrl_variation):

    item_number=''

    for index, row in nrl_variation.iterrows():

        # if row['edition'] == 'AP' or row['edition'] == 'PP' or row['edition'] == 'EP' or row['edition'] == 'ISN' or row['edition'] == 'IAP' or row['edition'] == 'IPP' or row['edition'] == 'IEP':
        if row['edition']== 'SN' and row['size'] == size and row['item_category']=='CGH':
            item_number=str(row['item_number'])

    return item_number


#rules:
#1, item_numbers should be generated consecutively, no gap.
#2, item category:PUF_G and CNU_G share same item_number with PUF and CNU
#3, for item_category CGH, SN, AP, PP, EP, ISN, IAP, IPP, and IEP should share the same item_number
#4, edition:for IGP, IEE, IJE, IDE, they share same item number with GP, EE, JE, DE.

#for CNU
def rule_C(row, nrl_variation, subset_G, local_last_item_no, index, subset_C):
    # if is I
    # print ('subset_D at very beginning')
    # print (subset_D)
    # print ('subset_G at very beginning')
    # print (subset_G)
    # print ('subset_H at very beginning')
    # print (subset_H)
    # find the item_number from D, G, H
    runtime_subset = subset_G
    # print ('runtime subset is ')
    # print (runtime_subset)

    #search in category[CNU or CNU_G] edition in [with I, without I]
    item_category_list = [row['item_category'], row['item_category']+'_G']
    #need to add edition which got rid of I
    input_edition_list = [row['edition'], row['edition'][1:]]

    # print ('input category list', item_category_list)
    # print ('input_edition list', input_edition_list)
    # print ('input size', row['size'])

    #the fetched number will be a string, only size must be the same, others are should be in the lists
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    # print (row['item_category'], row['size'], row['edition'])
    # print ('returned value is:',fetched_number)
    #
    # print ('before set value subset C and H')
    # print (subset_C[subset_C['edition'].isin(['AP','IAP'])])
    # print (subset_H[subset_H['edition'].isin(['AP','IAP'])])
    # print("the fetched number is ", fetched_number)

    if fetched_number == -1:

        # print('did not find the item_number, so creating')
        local_new_item_no = generate_item_number(local_last_item_no)

        # do not need to add "_G" to the local_new_item_no

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)
        # print ('the new item_number is', local_new_item_no)

        # print ('the new item number is :', local_last_item_no)
        # update the current subset
        # print('when set value subset H')
        # print(row['item_category'], row['size'], row['edition'])
        subset_C = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_C)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no

    else:

        # check the last two position in the fetched string, see if it is _G, then get rid of it

        if fetched_number[-2:] == '_G':
            fetched_number = fetched_number[:-2]

        # print ('add _G, so become:', fetched_number)
        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_C = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_C)

    # print ('after set value subset C and H')
    # print (subset_C[subset_C['edition'].isin(['AP','IAP'])])
    # print (subset_H[subset_H['edition'].isin(['AP','IAP'])])
    return subset_C, nrl_variation, local_last_item_no



def rule_D(row, nrl_variation, subset_H, local_last_item_no, index, subset_D):
    # if not I

    # find the item_number from C, G, H
    runtime_subset = subset_H

    #item_category is CNU, so we have to add CNU_G
    item_category_list = [row['item_category'], row['item_category']+'_G']
    #here we should add edition that adds I before it
    input_edition_list = [row['edition'], 'I' + row['edition']]

    #the fetched number will be a string
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    if fetched_number == -1:

        local_new_item_no = generate_item_number(local_last_item_no)

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        # update the current subset
        subset_D = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_D)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no

    else:

        # check the last two position in the fetched string, see if it is _G
        if fetched_number[-2:] == '_G':
            fetched_number = fetched_number[:-2]

        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_D = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_D)

    return subset_D, nrl_variation, local_last_item_no


def rule_E(row, nrl_variation, subset_I, local_last_item_no, index, subset_E):
    # if is I
    # print ('subset_D at very beginning')
    # print (subset_D)
    # print ('subset_G at very beginning')
    # print (subset_G)
    # print ('subset_H at very beginning')
    # print (subset_H)
    # find the item_number from D, G, H
    runtime_subset = subset_I
    # print ('runtime subset is ')
    # print (runtime_subset)

    #search in category[CNU or CNU_G] edition in [with I, without I]
    item_category_list = [row['item_category'], row['item_category']+'_G']
    #need to add edition which got rid of I
    input_edition_list = [row['edition'], row['edition'][1:]]

    # print ('input category list', item_category_list)
    # print ('input_edition list', input_edition_list)
    # print ('input size', row['size'])

    #the fetched number will be a string, only size must be the same, others are should be in the lists
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    # print (row['item_category'], row['size'], row['edition'])
    # print ('returned value is:',fetched_number)
    #
    # print ('before set value subset C and H')
    # print (subset_C[subset_C['edition'].isin(['AP','IAP'])])
    # print (subset_H[subset_H['edition'].isin(['AP','IAP'])])
    # print("the fetched number is ", fetched_number)

    if fetched_number == -1:

        # print('did not find the item_number, so creating')
        local_new_item_no = generate_item_number(local_last_item_no)

        # do not need to add "_G" to the local_new_item_no

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)
        # print ('the new item_number is', local_new_item_no)

        # print ('the new item number is :', local_last_item_no)
        # update the current subset
        # print('when set value subset H')
        # print(row['item_category'], row['size'], row['edition'])
        subset_E = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_E)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no

    else:

        # check the last two position in the fetched string, see if it is _G, then get rid of it

        if fetched_number[-2:] == '_G':
            fetched_number = fetched_number[:-2]

        # print ('add _G, so become:', fetched_number)
        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_E = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_E)

    # print ('after set value subset C and H')
    # print (subset_C[subset_C['edition'].isin(['AP','IAP'])])
    # print (subset_H[subset_H['edition'].isin(['AP','IAP'])])
    return subset_E, nrl_variation, local_last_item_no

def rule_F(row, nrl_variation, subset_J, local_last_item_no, index, subset_F):
    # if not I

    # find the item_number from C, G, H
    runtime_subset = subset_J

    #item_category is CNU, so we have to add CNU_G
    item_category_list = [row['item_category'], row['item_category']+'_G']
    #here we should add edition that adds I before it
    input_edition_list = [row['edition'], 'I' + row['edition']]

    #the fetched number will be a string
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    if fetched_number == -1:

        local_new_item_no = generate_item_number(local_last_item_no)

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        # update the current subset
        subset_F = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_F)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no

    else:

        # check the last two position in the fetched string, see if it is _G
        if fetched_number[-2:] == '_G':
            fetched_number = fetched_number[:-2]

        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_F = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_F)

    return subset_F, nrl_variation, local_last_item_no



#for CNU_G internatinal, problem is H, check out H first
def rule_G(row, nrl_variation, subset_C, local_last_item_no, index, subset_G):
    # if is I
    # print ('subset_G at very beginning')
    # print (subset_G)
    #
    # print ('subset_C at very beginning')
    # print (subset_C)
    # find the item_number from D, G, H
    runtime_subset = subset_C

    item_category_list = [row['item_category'], row['item_category'][:-2]]
    input_edition_list = [row['edition'], row['edition'][1:]]

    #the fetched number will be a string
    # print ('input category list', item_category_list)
    # print ('input_edition list', input_edition_list)
    # print ('input size', row['size'])
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)
    # print (row['item_category'], row['size'], row['edition'])
    # print ('returned value is:',fetched_number)
    #
    # print ('before set value subset G and H')
    # print (subset_G[subset_G['edition'].isin(['AP','IAP'])])
    # print (subset_H[subset_H['edition'].isin(['AP','IAP'])])



    if fetched_number == -1:

        # print('did not find the item_number, so creating')
        local_new_item_no = generate_item_number(local_last_item_no)

        # add '_G' before assign it
        local_new_item_no = str(local_new_item_no) + '_G'
        # print ('the new item_number is', local_new_item_no)
        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        # print ('the new item number is :', local_last_item_no)
        # update the current subset

        # print('when set value subset G')
        # print(row['item_category'], row['size'], row['edition'])
        subset_G = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_G)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no[:-2]

    else:

        # check the last two position in the fetched string, see if it is _G

        if fetched_number[-2:] != '_G':
            fetched_number = fetched_number + '_G'

        # print ('add _G, so become:', fetched_number)
        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset

        subset_G = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_G)

    # print ('before set value subset G and H')
    # print (subset_G[subset_G['edition'].isin(['AP','IAP'])])
    # print (subset_H[subset_H['edition'].isin(['AP','IAP'])])
    return subset_G, nrl_variation, local_last_item_no

#for CNU_G non international
def rule_H(row, nrl_variation,subset_D, local_last_item_no, index, subset_H):
    # if not I
    # print ('subset_H at very beginning')
    # print (subset_H)
    # print ('subset_C at very beginning')
    # print (subset_C)
    # print ('subset_D at very beginning')
    # print (subset_D)

    # find the item_number from C, D, G
    runtime_subset = subset_D

    # do not limit the edition in this search, because it should apply to multiple edition
    # and item_category applies to multiple as well
    # so input item_category and input_edition should be list
    item_category_list = [row['item_category'], row['item_category'][:-2]]
    input_edition_list = [row['edition'], 'I' + row['edition']]

    #the fetched number will be a string
    # print ('input category list', item_category_list)
    # print ('input_edition list', input_edition_list)
    # print ('input size', row['size'])
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    # print (row['item_category'], row['size'], row['edition'])
    # print ('returned value is:',fetched_number)
    #
    # print ('before set value subset G and H')
    # print (subset_G[subset_G['edition'].isin(['AP','IAP'])])
    # print (subset_H[subset_H['edition'].isin(['AP','IAP'])])
    # print("the fetched number is ", fetched_number)

    if fetched_number == -1:

        local_new_item_no = generate_item_number(local_last_item_no)

        # add '_G' before assign it
        local_new_item_no = str(local_new_item_no) + '_G'
        # print ('the new item_number is', local_new_item_no)

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        # update the current subset
        # print('when set value subset H')
        # print(row['item_category'], row['size'], row['edition'])
        subset_H = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_H)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no[:-2]

    else:

        # check the last two position in the fetched string, see if it is _G
        if fetched_number[-2:] != '_G':
            fetched_number = fetched_number + '_G'

        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_H = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_H)

    # print ('before set value subset G and H')
    # print (subset_G[subset_G['edition'].isin(['AP','IAP'])])
    # print (subset_H[subset_H['edition'].isin(['AP','IAP'])])
    return subset_H, nrl_variation, local_last_item_no


def rule_I(row, nrl_variation, subset_E, local_last_item_no, index, subset_I):

    # if is I
    # print ('subset_G at very beginning')
    # print (subset_G)
    #
    # print ('subset_C at very beginning')
    # print (subset_C)
    # find the item_number from D, G, H
    runtime_subset = subset_E

    item_category_list = [row['item_category'], row['item_category'][:-2]]
    input_edition_list = [row['edition'], row['edition'][1:]]

    #the fetched number will be a string
    # print ('input category list', item_category_list)
    # print ('input_edition list', input_edition_list)
    # print ('input size', row['size'])
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)
    # print (row['item_category'], row['size'], row['edition'])
    # print ('returned value is:',fetched_number)
    #
    # print ('before set value subset G and H')
    # print (subset_G[subset_G['edition'].isin(['AP','IAP'])])
    # print (subset_H[subset_H['edition'].isin(['AP','IAP'])])



    if fetched_number == -1:

        # print('did not find the item_number, so creating')
        local_new_item_no = generate_item_number(local_last_item_no)

        # add '_G' before assign it
        local_new_item_no = str(local_new_item_no) + '_G'
        # print ('the new item_number is', local_new_item_no)
        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        # print ('the new item number is :', local_last_item_no)
        # update the current subset

        # print('when set value subset G')
        # print(row['item_category'], row['size'], row['edition'])
        subset_I = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_I)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no[:-2]

    else:

        # check the last two position in the fetched string, see if it is _G

        if fetched_number[-2:] != '_G':
            fetched_number = fetched_number + '_G'

        # print ('add _G, so become:', fetched_number)
        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset

        subset_I = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_I)

    # print ('before set value subset G and H')
    # print (subset_G[subset_G['edition'].isin(['AP','IAP'])])
    # print (subset_H[subset_H['edition'].isin(['AP','IAP'])])
    return subset_I, nrl_variation, local_last_item_no


def rule_J(row, nrl_variation, subset_F, local_last_item_no, index, subset_J):
    # if not I

    # find the item_number from C, D, G
    runtime_subset = subset_F

    # do not limit the edition in this search, because it should apply to multiple edition
    # and item_category applies to multiple as well
    # so input item_category and input_edition should be list
    item_category_list = [row['item_category'], row['item_category'][:-2]]
    input_edition_list = [row['edition'], 'I' + row['edition']]

    #the fetched number will be a string

    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    if fetched_number == -1:

        local_new_item_no = generate_item_number(local_last_item_no)

        # add '_G' before assign it
        local_new_item_no = str(local_new_item_no) + '_G'

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        subset_J = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_J)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no[:-2]

    else:

        # check the last two position in the fetched string, see if it is _G
        if fetched_number[-2:] != '_G':
            fetched_number = fetched_number + '_G'

        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_J = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_J)

    return subset_J, nrl_variation, local_last_item_no

def rule_K(row, nrl_variation, subset_L, subset_M, subset_P, subset_Q, subset_R, subset_S, subset_T, local_last_item_no, index, subset_K, input_edition_list):

    # if is I

    # find the item_number from D, G, H
    runtime_subset = pd.concat([subset_L, subset_M, subset_P, subset_Q, subset_R, subset_S, subset_T])

    #search in category[CNU or CNU_G] edition in [with I, without I]
    item_category_list = [row['item_category']]

    #the fetched number will be a string, only size must be the same, others are should be in the lists
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)


    if fetched_number == -1:

        local_new_item_no = generate_item_number(local_last_item_no)

        # do not need to add "_G" to the local_new_item_no

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        subset_K = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_K)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no

    else:
        # print ('add _G, so become:', fetched_number)
        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_K = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_K)

    return subset_K, nrl_variation, local_last_item_no

def rule_L(row, nrl_variation, subset_K, subset_M, subset_P, subset_Q, subset_R, subset_S, subset_T, local_last_item_no, index, subset_L, input_edition_list):

    # if is I

    # find the item_number from D, G, H
    runtime_subset = pd.concat([subset_K, subset_M, subset_P, subset_Q, subset_R, subset_S, subset_T])

    #search in category[CNU or CNU_G] edition in [with I, without I]
    item_category_list = [row['item_category']]

    #the fetched number will be a string, only size must be the same, others are should be in the lists
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    if fetched_number == -1:

        local_new_item_no = generate_item_number(local_last_item_no)

        # do not need to add "_G" to the local_new_item_no

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        subset_L = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_L)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no

    else:
        # print ('add _G, so become:', fetched_number)
        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_L = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_L)

    return subset_L, nrl_variation, local_last_item_no

def rule_M(row, nrl_variation, subset_K, subset_L, subset_P, subset_Q, subset_R, subset_S, subset_T, local_last_item_no, index, subset_M, input_edition_list):

    # if is I

    # find the item_number from D, G, H
    runtime_subset = pd.concat([subset_K, subset_L, subset_P, subset_Q, subset_R, subset_S, subset_T])

    #search in category[CNU or CNU_G] edition in [with I, without I]
    item_category_list = [row['item_category']]

    #the fetched number will be a string, only size must be the same, others are should be in the lists
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    if fetched_number == -1:

        local_new_item_no = generate_item_number(local_last_item_no)

        # do not need to add "_G" to the local_new_item_no

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        subset_M = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_M)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no

    else:
        # print ('add _G, so become:', fetched_number)
        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_M = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_M)

    return subset_M, nrl_variation, local_last_item_no


def rule_N(row, nrl_variation, subset_O, local_last_item_no, index, subset_N):
    # if not I

    # find the item_number from C, G, H
    runtime_subset = subset_O

    #item_category is CNU, so we have to add CNU_G
    item_category_list = [row['item_category']]
    #here we should add edition that adds I before it
    input_edition_list = [row['edition'], 'I' + row['edition']]

    #the fetched number will be a string
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    if fetched_number == -1:

        local_new_item_no = generate_item_number(local_last_item_no)

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        # update the current subset
        subset_N = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_N)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no

    else:

        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_N = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_N)

    return subset_N, nrl_variation, local_last_item_no


def rule_O(row, nrl_variation, subset_N, local_last_item_no, index, subset_O):
    # if is I

    runtime_subset = subset_N

    #item_category is CNU, so we have to add CNU_G
    item_category_list = [row['item_category']]
    #need to add edition which got rid of I
    input_edition_list = [row['edition'], row['edition'][1:]]

    #the fetched number will be a string, only size must be the same, others are should be in the lists
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    if fetched_number == -1:

        local_new_item_no = generate_item_number(local_last_item_no)

        # do not need to add "_G" to the local_new_item_no

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        subset_O = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_O)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no

    else:

        # print ('add _G, so become:', fetched_number)
        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_O = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_O)

    return subset_O, nrl_variation, local_last_item_no

def rule_P(row, nrl_variation, subset_K, subset_L, subset_M, subset_Q, subset_R, subset_S, subset_T, local_last_item_no, index, subset_P, input_edition_list):
    # if is I

    # find the item_number from D, G, H
    runtime_subset = pd.concat([subset_K, subset_L, subset_M, subset_Q, subset_R, subset_S, subset_T])


    #search in category[CNU or CNU_G] edition in [with I, without I]
    item_category_list = [row['item_category']]

    #the fetched number will be a string, only size must be the same, others are should be in the lists
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    if fetched_number == -1:

        local_new_item_no = generate_item_number(local_last_item_no)

        # do not need to add "_G" to the local_new_item_no

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        subset_P = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_P)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no

    else:
        # print ('add _G, so become:', fetched_number)
        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_P = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_P)

    return subset_P, nrl_variation, local_last_item_no

def rule_Q(row, nrl_variation, subset_K, subset_L, subset_M, subset_P, subset_R, subset_S, subset_T, local_last_item_no, index, subset_Q, input_edition_list):
    # if is I

    # find the item_number from D, G, H
    runtime_subset = pd.concat([subset_K, subset_L, subset_M, subset_P, subset_R, subset_S, subset_T])

    #search in category[CNU or CNU_G] edition in [with I, without I]
    item_category_list = [row['item_category']]

    #the fetched number will be a string, only size must be the same, others are should be in the lists
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    if fetched_number == -1:

        local_new_item_no = generate_item_number(local_last_item_no)

        # do not need to add "_G" to the local_new_item_no

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        subset_Q = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_Q)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no

    else:
        # print ('add _G, so become:', fetched_number)
        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_Q = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_Q)

    return subset_Q, nrl_variation, local_last_item_no

def rule_R(row, nrl_variation, subset_K, subset_L, subset_M, subset_P, subset_Q, subset_S, subset_T, local_last_item_no, index, subset_R, input_edition_list):
    # if is I

    # find the item_number from D, G, H
    runtime_subset = pd.concat([subset_K, subset_L, subset_M, subset_P, subset_Q, subset_S, subset_T])

    #search in category[CNU or CNU_G] edition in [with I, without I]
    item_category_list = [row['item_category']]

    #the fetched number will be a string, only size must be the same, others are should be in the lists
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    if fetched_number == -1:

        local_new_item_no = generate_item_number(local_last_item_no)

        # do not need to add "_G" to the local_new_item_no

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        subset_R = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_R)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no

    else:
        # print ('add _G, so become:', fetched_number)
        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_R = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_R)

    return subset_R, nrl_variation, local_last_item_no

def rule_S(row, nrl_variation, subset_K, subset_L, subset_M, subset_P, subset_Q, subset_R, subset_T, local_last_item_no, index, subset_S, input_edition_list):
    # if is I

    # find the item_number from D, G, H
    runtime_subset = pd.concat([subset_K, subset_L, subset_M, subset_P, subset_Q, subset_R, subset_T])

    #search in category[CNU or CNU_G] edition in [with I, without I]
    item_category_list = [row['item_category']]

    #the fetched number will be a string, only size must be the same, others are should be in the lists
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    if fetched_number == -1:

        local_new_item_no = generate_item_number(local_last_item_no)

        # do not need to add "_G" to the local_new_item_no

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        subset_S = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_S)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no

    else:
        # print ('add _G, so become:', fetched_number)
        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_S = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_S)

    return subset_S, nrl_variation, local_last_item_no

def rule_T(row, nrl_variation, subset_K, subset_L, subset_M, subset_P, subset_Q, subset_R, subset_S, local_last_item_no, index, subset_T, input_edition_list):
    # if is I

    # find the item_number from D, G, H
    runtime_subset = pd.concat([subset_K, subset_L, subset_M, subset_P, subset_Q, subset_R, subset_S])

    #search in category[CNU or CNU_G] edition in [with I, without I]
    item_category_list = [row['item_category']]

    #the fetched number will be a string, only size must be the same, others are should be in the lists
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    if fetched_number == -1:

        local_new_item_no = generate_item_number(local_last_item_no)

        # do not need to add "_G" to the local_new_item_no

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        subset_T = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_T)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no

    else:
        # print ('add _G, so become:', fetched_number)
        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_T = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_T)

    return subset_T, nrl_variation, local_last_item_no


def rule_U(row, nrl_variation, subset_V, subset_W, subset_Z, subset_AA, subset_BB, subset_CC, subset_DD, local_last_item_no, index, subset_U, input_edition_list):

    # if is I

    # find the item_number from D, G, H
    runtime_subset = pd.concat([subset_V, subset_W, subset_Z, subset_AA, subset_BB, subset_CC, subset_DD])

    #search in category[CNU or CNU_G] edition in [with I, without I]
    item_category_list = [row['item_category']]

    #the fetched number will be a string, only size must be the same, others are should be in the lists
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    if fetched_number == -1:

        # print('did not find the item_number, so creating')
        local_new_item_no = generate_item_number(local_last_item_no)

        # do not need to add "_G" to the local_new_item_no

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        subset_U = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_U)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no

    else:
        # print ('add _G, so become:', fetched_number)
        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_U = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_U)


    return subset_U, nrl_variation, local_last_item_no

def rule_V(row, nrl_variation, subset_U, subset_W, subset_Z, subset_AA, subset_BB, subset_CC, subset_DD, local_last_item_no, index, subset_V, input_edition_list):

    # if is I

    # find the item_number from D, G, H
    runtime_subset = pd.concat([subset_U, subset_W, subset_Z, subset_AA, subset_BB, subset_CC, subset_DD])

    #search in category[CNU or CNU_G] edition in [with I, without I]
    item_category_list = [row['item_category']]

    #the fetched number will be a string, only size must be the same, others are should be in the lists
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    if fetched_number == -1:

        # print('did not find the item_number, so creating')
        local_new_item_no = generate_item_number(local_last_item_no)

        # do not need to add "_G" to the local_new_item_no

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        subset_V = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_V)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no

    else:
        # print ('add _G, so become:', fetched_number)
        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_V = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_V)

    return subset_V, nrl_variation, local_last_item_no

def rule_W(row, nrl_variation, subset_U, subset_V, subset_Z, subset_AA, subset_BB, subset_CC, subset_DD, local_last_item_no, index, subset_W, input_edition_list):


    # if is I

    # find the item_number from D, G, H
    runtime_subset = pd.concat([subset_U, subset_V, subset_Z, subset_AA, subset_BB, subset_CC, subset_DD])

    #search in category[CNU or CNU_G] edition in [with I, without I]
    item_category_list = [row['item_category']]

    #the fetched number will be a string, only size must be the same, others are should be in the lists
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    if fetched_number == -1:

        # print('did not find the item_number, so creating')
        local_new_item_no = generate_item_number(local_last_item_no)

        # do not need to add "_G" to the local_new_item_no

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        subset_W = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_W)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no

    else:
        # print ('add _G, so become:', fetched_number)
        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_W = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_W)

    return subset_W, nrl_variation, local_last_item_no


def rule_X(row, nrl_variation, subset_Y, local_last_item_no, index, subset_X):
    # if not I

    # find the item_number from C, G, H
    runtime_subset = subset_Y

    #item_category is CNU, so we have to add CNU_G
    item_category_list = [row['item_category']]
    #here we should add edition that adds I before it
    input_edition_list = [row['edition'], 'I' + row['edition']]

    #the fetched number will be a string
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    if fetched_number == -1:

        local_new_item_no = generate_item_number(local_last_item_no)

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        # update the current subset
        subset_X = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_X)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no

    else:

        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_X = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_X)

    return subset_X, nrl_variation, local_last_item_no


def rule_Y(row, nrl_variation, subset_X, local_last_item_no, index, subset_Y):
    # if is I

    runtime_subset = subset_X

    #item_category is CNU, so we have to add CNU_G
    item_category_list = [row['item_category']]
    #need to add edition which got rid of I
    input_edition_list = [row['edition'], row['edition'][1:]]


    #the fetched number will be a string, only size must be the same, others are should be in the lists
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    if fetched_number == -1:

        # print('did not find the item_number, so creating')
        local_new_item_no = generate_item_number(local_last_item_no)

        # do not need to add "_G" to the local_new_item_no

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        subset_Y = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_Y)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no

    else:

        # print ('add _G, so become:', fetched_number)
        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_Y = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_Y)


    return subset_Y, nrl_variation, local_last_item_no

def rule_Z(row, nrl_variation, subset_U, subset_V, subset_W, subset_AA, subset_BB, subset_CC, subset_DD, local_last_item_no, index, subset_Z, input_edition_list):
    # if is I

    # find the item_number from D, G, H
    runtime_subset = pd.concat([subset_U, subset_V, subset_W, subset_AA, subset_BB, subset_CC, subset_DD])

    #search in category[CNU or CNU_G] edition in [with I, without I]
    item_category_list = [row['item_category']]

    #the fetched number will be a string, only size must be the same, others are should be in the lists
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    if fetched_number == -1:

        # print('did not find the item_number, so creating')
        local_new_item_no = generate_item_number(local_last_item_no)

        # do not need to add "_G" to the local_new_item_no

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        subset_Z = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_Z)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no

    else:
        # print ('add _G, so become:', fetched_number)
        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_Z = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_Z)


    return subset_Z, nrl_variation, local_last_item_no

def rule_AA(row, nrl_variation, subset_U, subset_V, subset_W, subset_Z, subset_BB, subset_CC, subset_DD, local_last_item_no, index, subset_AA, input_edition_list):
    # if is I

    # find the item_number from D, G, H
    runtime_subset = pd.concat([subset_U, subset_V, subset_W, subset_Z, subset_BB, subset_CC, subset_DD])

    #search in category[CNU or CNU_G] edition in [with I, without I]
    item_category_list = [row['item_category']]

    #the fetched number will be a string, only size must be the same, others are should be in the lists
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    if fetched_number == -1:

        local_new_item_no = generate_item_number(local_last_item_no)

        # do not need to add "_G" to the local_new_item_no

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        subset_AA = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_AA)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no

    else:
        # print ('add _G, so become:', fetched_number)
        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_AA = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_AA)

    return subset_AA, nrl_variation, local_last_item_no

def rule_BB(row, nrl_variation, subset_U, subset_V, subset_W, subset_Z, subset_AA, subset_CC, subset_DD, local_last_item_no, index, subset_BB, input_edition_list):
    # if is I

    # find the item_number from D, G, H
    runtime_subset = pd.concat([subset_U, subset_V, subset_W, subset_Z, subset_AA, subset_CC, subset_DD])

    #search in category[CNU or CNU_G] edition in [with I, without I]
    item_category_list = [row['item_category']]

    #the fetched number will be a string, only size must be the same, others are should be in the lists
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    if fetched_number == -1:

        local_new_item_no = generate_item_number(local_last_item_no)

        # do not need to add "_G" to the local_new_item_no

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        subset_BB = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_BB)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no

    else:
        # print ('add _G, so become:', fetched_number)
        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_BB = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_BB)

    return subset_BB, nrl_variation, local_last_item_no

def rule_CC(row, nrl_variation, subset_U, subset_V, subset_W, subset_Z, subset_AA, subset_BB, subset_DD, local_last_item_no, index, subset_CC, input_edition_list):
    # if is I
    # find the item_number from D, G, H
    runtime_subset = pd.concat([subset_U, subset_V, subset_W, subset_Z, subset_AA, subset_BB, subset_DD])

    #search in category[CNU or CNU_G] edition in [with I, without I]
    item_category_list = [row['item_category']]

    #the fetched number will be a string, only size must be the same, others are should be in the lists
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    if fetched_number == -1:

        local_new_item_no = generate_item_number(local_last_item_no)

        # do not need to add "_G" to the local_new_item_no

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        subset_CC = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_CC)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no

    else:
        # print ('add _G, so become:', fetched_number)
        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_CC = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_CC)

    return subset_CC, nrl_variation, local_last_item_no

def rule_DD(row, nrl_variation, subset_U, subset_V, subset_W, subset_Z, subset_AA, subset_BB, subset_CC, local_last_item_no, index, subset_DD, input_edition_list):
    # if is I
    # find the item_number from D, G, H
    runtime_subset = pd.concat([subset_U, subset_V, subset_W, subset_Z, subset_AA, subset_BB, subset_CC])

    #search in category[CNU or CNU_G] edition in [with I, without I]
    item_category_list = [row['item_category']]

    #the fetched number will be a string, only size must be the same, others are should be in the lists
    fetched_number = fetch_item_number_list(item_category_list, input_edition_list, row['size'], runtime_subset)

    if fetched_number == -1:

        local_new_item_no = generate_item_number(local_last_item_no)

        # do not need to add "_G" to the local_new_item_no

        # set the main table
        nrl_variation.set_value(index, 'item_number', local_new_item_no)

        subset_DD = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                          local_new_item_no, subset_DD)

        # get rid of '_G' before push it to the last item number
        local_last_item_no = local_new_item_no

    else:
        # print ('add _G, so become:', fetched_number)
        nrl_variation.set_value(index, 'item_number', fetched_number)
        # update the current subset
        subset_DD = set_subset_item_number(row['edition'], row['size'], row['item_category'], fetched_number, subset_DD)

    return subset_DD, nrl_variation, local_last_item_no


def rule_A(row, nrl_variation, local_last_item_no, index, subset_A):

    # if is I


    local_new_item_no = generate_item_number(local_last_item_no)

    nrl_variation.set_value(index, 'item_number', local_new_item_no)

    subset_A = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                      local_new_item_no, subset_A)

    # get rid of '_G' before push it to the last item number
    local_last_item_no = local_new_item_no



    return subset_A, nrl_variation, local_last_item_no


def rule_B(row, nrl_variation, local_last_item_no, index, subset_B):
    # if not I


    local_new_item_no = generate_item_number(local_last_item_no)

    # set the main table
    nrl_variation.set_value(index, 'item_number', local_new_item_no)

    # update the current subset
    subset_B = set_subset_item_number(row['edition'], row['size'], row['item_category'],
                                      local_new_item_no, subset_B)

    # get rid of '_G' before push it to the last item number
    local_last_item_no = local_new_item_no


    return subset_B, nrl_variation, local_last_item_no


def assign_item_number(nrl_variation, last_item_number):

    local_last_item_no=last_item_number

    #create subset in advance
    subset_C=nrl_variation[(nrl_variation['edition'].isin(['ISN','IAP','IPP','IEP', 'IGP', 'IDE', 'IEE', 'IJE'])) & (nrl_variation['item_category']=='CNU')]
    subset_D=nrl_variation[(nrl_variation['edition'].isin(['SN','AP','PP','EP', 'GP', 'DE', 'EE', 'JE'])) & (nrl_variation['item_category']=='CNU')]
    subset_E=nrl_variation[(nrl_variation['edition'].isin(['ISN','IAP','IPP','IEP', 'IGP', 'IDE', 'IEE', 'IJE'])) & (nrl_variation['item_category']=='PUF')]
    subset_F=nrl_variation[(nrl_variation['edition'].isin(['SN', 'AP', 'PP', 'EP', 'GP', 'DE', 'EE', 'JE'])) & (nrl_variation['item_category'] == 'PUF')]
    subset_G=nrl_variation[(nrl_variation['edition'].isin(['ISN','IAP','IPP','IEP', 'IGP', 'IDE', 'IEE', 'IJE'])) & (nrl_variation['item_category']=='CNU_G')]
    subset_H=nrl_variation[(nrl_variation['edition'].isin(['SN', 'AP', 'PP', 'EP', 'GP', 'DE', 'EE', 'JE'])) & (nrl_variation['item_category'] == 'CNU_G')]
    subset_I=nrl_variation[(nrl_variation['edition'].isin(['ISN','IAP','IPP','IEP', 'IGP', 'IDE', 'IEE', 'IJE'])) & (nrl_variation['item_category']=='PUF_G')]
    subset_J=nrl_variation[(nrl_variation['edition'].isin(['SN', 'AP', 'PP', 'EP', 'GP', 'DE', 'EE', 'JE'])) & (nrl_variation['item_category'] == 'PUF_G')]
    subset_K=nrl_variation[(nrl_variation['edition'].isin(['ISN'])) & (nrl_variation['item_category']=='CGH')]
    subset_L=nrl_variation[(nrl_variation['edition'].isin(['SN'])) & (nrl_variation['item_category']=='CGH')]
    subset_M=nrl_variation[(nrl_variation['edition'].isin(['AP'])) & (nrl_variation['item_category']=='CGH')]
    subset_N=nrl_variation[(nrl_variation['edition'].isin(['GP', 'DE', 'EE', 'JE'])) & (nrl_variation['item_category'] == 'CGH')]
    subset_O=nrl_variation[(nrl_variation['edition'].isin(['IGP', 'IDE', 'IEE', 'IJE'])) & (nrl_variation['item_category']=='CGH')]
    subset_P=nrl_variation[(nrl_variation['edition'].isin(['IAP'])) & (nrl_variation['item_category']=='CGH')]
    subset_Q=nrl_variation[(nrl_variation['edition'].isin(['IPP'])) & (nrl_variation['item_category']=='CGH')]
    subset_R=nrl_variation[(nrl_variation['edition'].isin(['IEP'])) & (nrl_variation['item_category']=='CGH')]
    subset_S=nrl_variation[(nrl_variation['edition'].isin(['PP'])) & (nrl_variation['item_category']=='CGH')]
    subset_T=nrl_variation[(nrl_variation['edition'].isin(['EP'])) & (nrl_variation['item_category']=='CGH')]
    subset_U=nrl_variation[(nrl_variation['edition'].isin(['ISN'])) & (nrl_variation['item_category']=='PPS')]
    subset_V=nrl_variation[(nrl_variation['edition'].isin(['SN'])) & (nrl_variation['item_category']=='PPS')]
    subset_W=nrl_variation[(nrl_variation['edition'].isin(['AP'])) & (nrl_variation['item_category']=='PPS')]
    subset_X=nrl_variation[(nrl_variation['edition'].isin(['GP', 'DE', 'EE', 'JE'])) & (nrl_variation['item_category'] == 'PPS')]
    subset_Y=nrl_variation[(nrl_variation['edition'].isin(['IGP', 'IDE', 'IEE', 'IJE'])) & (nrl_variation['item_category']=='PPS')]
    subset_Z=nrl_variation[(nrl_variation['edition'].isin(['IAP'])) & (nrl_variation['item_category']=='PPS')]
    subset_AA=nrl_variation[(nrl_variation['edition'].isin(['IPP'])) & (nrl_variation['item_category']=='PPS')]
    subset_BB=nrl_variation[(nrl_variation['edition'].isin(['IEP'])) & (nrl_variation['item_category']=='PPS')]
    subset_CC=nrl_variation[(nrl_variation['edition'].isin(['PP'])) & (nrl_variation['item_category']=='PPS')]
    subset_DD=nrl_variation[(nrl_variation['edition'].isin(['EP'])) & (nrl_variation['item_category']=='PPS')]

    other=nrl_variation[nrl_variation['item_category'].isin(['CER','NPL','ZPC'])]

    subset_A=other[other['edition'].isin(['ISN','IAP','IPP','IEP', 'IGP', 'IDE', 'IEE', 'IJE'])]
    subset_B=other[other['edition'].isin(['SN','AP','PP','EP', 'GP', 'DE', 'EE', 'JE'])]

    # subset_list=[subset_A, subset_B, subset_C, subset_D, subset_E, subset_F, subset_G, subset_H, subset_I, subset_J, \
    #              subset_K, subset_L, subset_M, subset_N, subset_O, subset_P, subset_Q, subset_R, subset_S, subset_T, \
    #              subset_U, subset_V, subset_W, subset_X, subset_Y, subset_Z, subset_AA, subset_BB, subset_CC, subset_DD, other]

    # other=nrl_variation[(~nrl_variation.isin(subset_C)) & (~nrl_variation.isin(subset_D)) & (~nrl_variation.isin(subset_E)) & (~nrl_variation.isin(subset_F)) \
    #                     & (~nrl_variation.isin(subset_G)) & (~nrl_variation.isin(subset_H)) & (~nrl_variation.isin(subset_I)) & (~nrl_variation.isin(subset_J)) \
    #                     & (~nrl_variation.isin(subset_K)) & (~nrl_variation.isin(subset_L)) & (~nrl_variation.isin(subset_M)) & (~nrl_variation.isin(subset_N)) \
    #                     & (~nrl_variation.isin(subset_O)) & (~nrl_variation.isin(subset_P)) & (~nrl_variation.isin(subset_Q)) & (~nrl_variation.isin(subset_R)) \
    #                     & (~nrl_variation.isin(subset_S)) & (~nrl_variation.isin(subset_T)) & (~nrl_variation.isin(subset_U)) & (~nrl_variation.isin(subset_V)) \
    #                     & (~nrl_variation.isin(subset_W)) & (~nrl_variation.isin(subset_X)) & (~nrl_variation.isin(subset_Y)) & (~nrl_variation.isin(subset_Z)) \
    #                     & (~nrl_variation.isin(subset_AA)) & (~nrl_variation.isin(subset_BB)) & (~nrl_variation.isin(subset_CC)) & (~nrl_variation.isin(subset_DD))]


    #for each row, verify all the rules and issue a new item number to it
    for index, row in nrl_variation.iterrows():

        #CNU is good now
        if row['item_category']=='CNU':

            if check_intelnational(row['edition'])==1:

                subset_C, nrl_variation, local_last_item_no=rule_C(row, nrl_variation, subset_G, local_last_item_no, index, subset_C)

            else:
                subset_D, nrl_variation, local_last_item_no=rule_D(row, nrl_variation, subset_H, local_last_item_no, index, subset_D)


        elif row['item_category']=='PUF':

            if check_intelnational(row['edition'])==1:
                subset_E,nrl_variation,local_last_item_no=rule_E(row, nrl_variation, subset_I, local_last_item_no, index, subset_E)


            else:
                #if not I
                subset_F, nrl_variation, local_last_item_no=rule_F(row, nrl_variation, subset_J, local_last_item_no, index, subset_F)


        elif row['item_category'] == 'CNU_G':


            # print('this is CNU_G diagnose')
            if check_intelnational(row['edition'])==1:

                subset_G, nrl_variation, local_last_item_no = rule_G(row, nrl_variation, subset_C, local_last_item_no, index, subset_G)


            else:

                subset_H, nrl_variation, local_last_item_no = rule_H(row, nrl_variation, subset_D, local_last_item_no, index, subset_H)


        elif row['item_category'] == 'PUF_G':

            if check_intelnational(row['edition'])==1:
            # if is I
                subset_I, nrl_variation, local_last_item_no=rule_I(row, nrl_variation, subset_E, local_last_item_no, index, subset_I)

            else:
            # if not I
                subset_J, nrl_variation, local_last_item_no=rule_J(row, nrl_variation, subset_F, local_last_item_no, index, subset_J)


        elif row['item_category'] == 'CGH':

            input_edition_list=['ISN', 'SN', 'AP', 'IAP', 'PP', 'IPP', 'EP', 'IEP']

            if row['edition']=='ISN':

                subset_K, nrl_variation, local_last_item_no=rule_K(row, nrl_variation, subset_L, subset_M, subset_P, subset_Q, subset_R, subset_S, subset_T, local_last_item_no, index, subset_K, input_edition_list)

            elif row['edition']=='SN':

                subset_L, nrl_variation, local_last_item_no=rule_L(row, nrl_variation, subset_K, subset_M, subset_P, subset_Q, subset_R, subset_S, subset_T, local_last_item_no, index, subset_L, input_edition_list)


            elif row['edition']=='AP':

                subset_M, nrl_variation, local_last_item_no=rule_M(row, nrl_variation, subset_K, subset_L, subset_P, subset_Q, subset_R, subset_S, subset_T, local_last_item_no, index, subset_M, input_edition_list)

            elif row['edition']=='GP' or row['edition']=='DE' or row['edition']=='EE' or row['edition']=='JE':

                subset_N, nrl_variation, local_last_item_no=rule_N(row, nrl_variation, subset_O, local_last_item_no, index, subset_N)


            elif row['edition']=='IGP' or row['edition']=='IDE' or row['edition']=='IEE' or row['edition']=='IJE':

                subset_O, nrl_variation, local_last_item_no=rule_O(row, nrl_variation, subset_N, local_last_item_no, index, subset_O)

            elif row['edition']=='IAP':

                subset_P, nrl_variation, local_last_item_no=rule_P(row, nrl_variation, subset_K, subset_L, subset_M, subset_Q, subset_R, subset_S, subset_T, local_last_item_no, index, subset_P, input_edition_list)

            elif row['edition']=='IPP':

                subset_Q, nrl_variation, local_last_item_no=rule_Q(row, nrl_variation, subset_K, subset_L, subset_M, subset_P, subset_R, subset_S, subset_T, local_last_item_no, index, subset_Q, input_edition_list)


            elif row['edition']=='IEP':

                subset_R, nrl_variation, local_last_item_no=rule_R(row, nrl_variation, subset_K, subset_L, subset_M, subset_P, subset_Q, subset_S, subset_T, local_last_item_no, index, subset_R, input_edition_list)

            elif row['edition']=='PP':

                subset_S, nrl_variation, local_last_item_no=rule_S(row, nrl_variation, subset_K, subset_L, subset_M, subset_P, subset_Q, subset_R, subset_T, local_last_item_no, index, subset_S, input_edition_list)

            elif row['edition']=='EP':

                subset_T, nrl_variation, local_last_item_no=rule_T(row, nrl_variation, subset_K, subset_L, subset_M, subset_P, subset_Q, subset_R, subset_S, local_last_item_no, index, subset_T, input_edition_list)

        elif row['item_category'] == 'PPS':

            input_edition_list=['ISN', 'SN', 'AP', 'IAP', 'PP', 'IPP', 'EP', 'IEP']

            if row['edition']=='ISN':

                subset_U, nrl_variation, local_last_item_no=rule_U(row, nrl_variation, subset_V, subset_W, subset_Z, subset_AA, subset_BB, subset_CC, subset_DD, local_last_item_no, index, subset_U, input_edition_list)

            elif row['edition']=='SN':

                subset_V, nrl_variation, local_last_item_no=rule_V(row, nrl_variation, subset_U, subset_W, subset_Z, subset_AA, subset_BB, subset_CC, subset_DD, local_last_item_no, index, subset_V, input_edition_list)

            elif row['edition']=='AP':

                subset_W, nrl_variation, local_last_item_no=rule_W(row, nrl_variation, subset_U, subset_V, subset_Z, subset_AA, subset_BB, subset_CC, subset_DD, local_last_item_no, index, subset_W, input_edition_list)


            elif row['edition']=='GP' or row['edition']=='DE' or row['edition']=='EE' or row['edition']=='JE':

                subset_X, nrl_variation, local_last_item_no=rule_X(row, nrl_variation, subset_Y, local_last_item_no, index, subset_X)

            elif row['edition']=='IGP' or row['edition']=='IDE' or row['edition']=='IEE' or row['edition']=='IJE':

                subset_Y, nrl_variation, local_last_item_no=rule_Y(row, nrl_variation, subset_X, local_last_item_no, index, subset_Y)

            elif row['edition']=='IAP':

                subset_Z, nrl_variation, local_last_item_no=rule_Z(row, nrl_variation, subset_U, subset_V, subset_W, subset_AA, subset_BB, subset_CC, subset_DD, local_last_item_no, index, subset_Z, input_edition_list)

            elif row['edition']=='IPP':

                subset_AA, nrl_variation, local_last_item_no=rule_AA(row, nrl_variation, subset_U, subset_V, subset_W, subset_Z, subset_BB, subset_CC, subset_DD, local_last_item_no, index, subset_AA, input_edition_list)

            elif row['edition']=='IEP':

                subset_BB, nrl_variation, local_last_item_no=rule_BB(row, nrl_variation, subset_U, subset_V, subset_W, subset_Z, subset_AA, subset_CC, subset_DD, local_last_item_no, index, subset_BB, input_edition_list)

            elif row['edition']=='PP':

                subset_CC, nrl_variation, local_last_item_no=rule_CC(row, nrl_variation, subset_U, subset_V, subset_W, subset_Z, subset_AA, subset_BB, subset_DD, local_last_item_no, index, subset_CC, input_edition_list)

            elif row['edition']=='EP':

                subset_DD, nrl_variation, local_last_item_no=rule_DD(row, nrl_variation, subset_U, subset_V, subset_W, subset_Z, subset_AA, subset_BB, subset_CC, local_last_item_no, index, subset_DD, input_edition_list)

        #for CER, NPL, and ZPC:
        else:

            if check_intelnational(row['edition'])==1:

                subset_A, nrl_variation, local_last_item_no=rule_A(row, nrl_variation, local_last_item_no, index, subset_A)

            else:

                subset_B, nrl_variation, local_last_item_no=rule_B(row, nrl_variation, local_last_item_no, index, subset_B)


    return nrl_variation


def assign_upc_number(nrl_variation, last_upc_number):

    # update upc number
    for index, row in nrl_variation.iterrows():

        if row[1] == 'CNU' or row[1] == 'PUF':
            new_upc_number = generate_upc_number(last_upc_number)
            last_upc_number = new_upc_number
            nrl_variation.set_value(index, 'upc_number', new_upc_number)

    return nrl_variation


def check_intelnational(edition):


    if edition.find('I',0)==0:

        return 1

    else:
        return 0

def convert_intl_dome(edition):

    return edition[1:]

def fetch_item_number(item_category, edition, size, nrl_variation):

    item_number=-1

    for index, row in nrl_variation.iterrows():

        if row['item_category']==item_category and row['edition']==edition and row['size']==size:

            item_number=str(row['item_number'])

    if item_number=='':
        return -1

    else:
        return item_number

def fetch_item_number_bylist(item_category, edition, size, subset_list):

    for list_index, x in enumerate(subset_list):

        item_number = -1

        for index, row in x.iterrows():

            if row['item_category'] == item_category and row['edition'] == edition and row['size'] == size:
                item_number = str(row['item_number'])

        if item_number == '':
            return -1, list_index,x

        else:
            return item_number, list_index, x

def set_subset_item_number(edition, size, item_category, item_number, subset):

    for index, row in subset.iterrows():

        if row['edition']==edition and row['size']==size and row['item_category']==item_category:

            subset.set_value(index, 'item_number', item_number)


    return subset


#this method would return string type for item_number
#the problem of this function is, when it sees the first value
#1, if it is '', it'll return, it won't keep going to next value, however there might be another value which is not ''
#so the logic should be revised to:
#find first none '' value, if no, return -1
def fetch_item_number_list(item_category_list, edition_list, size, subset):

    for index, row in subset.iterrows():

        if (row['item_category'] in item_category_list) and (row['edition'] in edition_list) and row['size']==size and row['item_number']!='':

                return str(row['item_number'])

    return -1



