from src.file_loader import load_csv

def str_type(chaine):
    if chaine.isdigit():
        return "int"
    try:
        float_value = float(chaine)
        return "float" if '.' in chaine else "int"
    except ValueError:
        return "str"
        


def get_file_type(file_path):
    return file_path.split(".")[-1]


def sum_ord(string):
    return sum(ord(c) for c in string)


def get_column_types(data_list):
    column_types = {}

    for item in data_list:
        for key, value in item.items():
            current_type = type(value)

            if key not in column_types:
                column_types[key] = {current_type}
            else:
                column_types[key].add(current_type)

    return column_types

def list_type_columns(data):
    columns = []
    if not data:
        return columns
    for line in data:
        for key, value in line.items():
            if value and type(value) == str:
                if value[0] == '[' and value[-1] == ']':
                    columns.append(key)
    columns = list(set(columns))

    return columns


def bool_type_columns(data):
    columns = []
    if not data:
        return columns
    for line in data:
        for key, value in line.items():
            if value and type(value) == str:
                if value.lower() == 'true' or value.lower() == 'false':
                    columns.append(key)
    columns = list(set(columns))

    return columns
