import csv
import json
import yaml
import xml.etree.ElementTree as ET
from itertools import zip_longest

def load_csv(path):
    with open(path,'r') as csvfile:
    
        dict_data = []
        
        reader = csv.reader(csvfile, delimiter=',')
    
        fields = next(reader)
        
        for row in reader:
            dict_row = {}

            for i,f in enumerate(fields):
                value = row[i]
                try:
                    value = int(row[i])
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                dict_row[f] = value
                
            dict_data.append(dict_row)
            
    return dict_data

def load_json(path):
    with open(path, 'r') as file_json:
        data = json.load(file_json)
        
    return data

def load_yaml(path):
    with open(path, 'r') as file_yaml:
        data = yaml.safe_load(file_yaml)

    return data

def get_xml_data_from_file(main_elem):
    data = []
    if len(main_elem) <= 0:
        data_dict = {}
        for child in main_elem.iter():
            data_dict[child.tag] = child.text
        data.append(data_dict)
        return data

    for child in main_elem:
        data_dict = {}
        for elem in child.iter():
            if elem.tag != child.tag:
                data_dict[elem.tag] = elem.text
        data.append(data_dict)

    return data

def load_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()

    data = get_xml_data_from_file(root)

    return data
