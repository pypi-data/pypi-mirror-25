def patch_x_upper(input_table):

    for column in input_table:

        if input_table[column].dtype=='object':
            input_table[column]=input_table[column].str.upper()

    return input_table
