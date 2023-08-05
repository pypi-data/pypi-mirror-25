# define the cost functions

# for CGH

# unit_cost is fixed at 0.73 for canvas, and we assume we need only 1 strech bar
# this part of program will be modified once I get the cost table of strech bar
# for now, just assume all strech bar cost 1.7
def canvas_quantity(size):

    if 'x' in size:
        length, width = size.split('x')
    else:
        length, width = size.split('X')

    quantity = (float(length) + 3 * 2) * (float(width) + 3 * 2) / 144 / 0.95

    return quantity


def paper_quantity(size):

    if 'x' in size:
        length, width = size.split('x')
    else:
        length, width = size.split('X')

    quantity = (float(length) + 2 * 2) * (float(width) + 2 * 2) / 144 / 0.95

    return quantity


# this has been changed
def cgh_cost(edition, size, strechBar):

    if 'x' in size:
        length, width = size.split('x')
    else:
        length, width = size.split('X')

    canvas_cost = ((float(length) + 6) * (float(width) + 6) / 144 / 0.95) * 0.73

    strech_bar_cost = 1 * float(strechBar_cost(edition, size, strechBar))

    total_cost = canvas_cost + strech_bar_cost

    return total_cost


# for CNU, we assume the cost of npl_cost is 0.374
def cnu_cost(edition, size, strechBar):
    npl_cost = 0.374
    return cgh_cost(edition, size, strechBar) + npl_cost


def cnu_g_cost(edition, size, strechBar):
    return cnu_cost(edition, size, strechBar)


# unit_cost is fixed at 0.37 for paper, and we assume we need only 0 strech bar
def pps_cost(size):
    unit_cost_paper = 0.37

    if 'x' in size:
        length, width = size.split('x')
    else:
        length, width = size.split('X')

    total_cost = ((float(length) + 8) * (float(width) + 8) / 144 / 0.95) * unit_cost_paper

    return total_cost


def puf_cost(size):
    return pps_cost(size)


def puf_g_cost(size):
    return puf_cost(size)


# can't return None. if strechBar table is corrupted, the output will cause an error
def strechBar_cost(edition, size,strechBar):
    if edition == 'EE' or edition == 'JE':

        for index, row in strechBar.iterrows():
            if row[0] == 'OTHER' and row[1] == size:
                return row[3]

    elif edition == 'BC':
        for index, row in strechBar.iterrows():
            if row[0] == 'B' and row[1] == size:
                return row[3]
    else:
        for index, row in strechBar.iterrows():
            if row[0] == 'T' and row[1] == size:
                return row[3]


def strechBar_item_number(edition, size,strechBar):
    if edition == 'EE' or edition == 'JE':
        for index, row in strechBar.iterrows():
            if row[0] == 'OTHER' and row[1] == size:
                return row[2]

    elif edition == 'BC':
        for index, row in strechBar.iterrows():
            if row[0] == 'B' and row[1] == size:
                return row[2]
    else:
        for index, row in strechBar.iterrows():
            if row[0] == 'T' and row[1] == size:
                return row[2]
