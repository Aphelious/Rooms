import random


# def get_shape():
#     '''Build a dictionary that represents the shape of a room between 3 and 5 rows, and between 3 and 5 columns.
#        Example shape: {'A': [-2, -1, 0, 1, 2], 
#                        'B': [-2, -1, 0, 1], 
#                        'C':     [-1, 0, 1], 
#                        'D': [-2, -1, 0, 1, 2]}'''
    
#     shape = dict()
#     for row in range(random.randint(4,6)):
#         col_num = random.randint(3,5)
#         cols = [-1,0,1]
#         if col_num == 4:
#             cols.append(random.choice([-2,2]))
#         elif col_num == 5:
#             cols.extend([-2,2])
#         if row == 1:
#             shape.update({"A":sorted(cols)})
#         if row == 2:
#             shape.update({"B":sorted(cols)})
#         if row == 3:
#             shape.update({"C":sorted(cols)})
#         if row == 4:
#             shape.update({"D":sorted(cols)})
#         if row == 5:
#             shape.update({"E":sorted(cols)})
#     return shape


def get_shape():
    '''Build a list of lists that represents the shape of a room between 3 and 5 rows, and between 3 and 5 columns.
       Example shape: [[-2, -1, 0, 1, 2], 
                       [-2, -1, 0, 1], 
                           [-1, 0, 1], 
                       [-2, -1, 0, 1, 2]]'''
    
    shape = list()
    for row in range(random.randint(4,6)):
        col_num = random.randint(3,5)
        cols = [-1,0,1]
        if col_num == 4:
            cols.append(random.choice([-2,2]))
        elif col_num == 5:
            cols.extend([-2,2])
        if row == 1:
            shape.append(sorted(cols))
        if row == 2:
            shape.append(sorted(cols))
        if row == 3:
            shape.append(sorted(cols))
        if row == 4:
            shape.append(sorted(cols))
        if row == 5:
            shape.append(sorted(cols))
    return shape


def get_space(shape: dict) -> dict:
    rows_list = [x for x in shape.keys()]
    random_row = random.choice(rows_list)
    cols_list = [x for x in shape[random_row]]
    random_col = random.choice(cols_list)
    space ={random_row: random_col}
    return space


def get_random_space(shape):
    row_index = random.randint(0, len(shape) - 1)  # Select a random index for the row
    row = shape[row_index]  # Get the selected row
    space = random.choice(row)  # Select a random space from the chosen row
    return row_index, space


def get_wall_space(shape) -> dict:
    '''Takes in instance and returns a space that represents an outermost space
       in the room ie: along a wall where a entrance/exit door would be. '''
    
    rows_list = [x for x in shape.keys()]
    random_row = random.choice(rows_list)
    exterior_cols_list = [x for x in shape[random_row] if shape[random_row].index(x) in (0, -1)]
    random_col = random.choice(exterior_cols_list)
    wall_space = {random_row: random_col}
    # self.check_space(wall_space)
    # self.set_occupied_space(wall_space)
    return wall_space


# shape = get_shape()
# print(shape)
# row, col = get_random_space(shape)
# print (f'{row}, {col}')

# space = get_space(shape)
# print(space)

# wall_space = get_wall_space(shape)
# print(wall_space)

# def get_string_repr_space(space):
#     '''Takes in a space dictionary and returns a string representation of that space to be used for '''
    
#     rows = list(space.keys())
#     row = rows[0]
#     col = str(space[row])
#     string_space = f'{row}{col}'
#     return string_space

# print(get_string_repr_space({"A":1}))
print((1,2) in [(1,3), (1,2)])
