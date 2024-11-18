import csv
import json
import yaml

import xml.etree.ElementTree as ET

def save_csv(dict_data, path, filename):
    
    with open(f"{path}/{filename}", mode='w', newline='') as file_csv:
        
        columns = dict_data[0].keys()
        
        writer = csv.DictWriter(file_csv, fieldnames=columns)
        writer.writeheader()

        writer.writerows(dict_data)

    print(f"Les données ont été enregistrées dans {path}.")

def save_json(dict_data, path, filename):
    
    with open(f"{path}/{filename}", 'w') as file_json:
        json.dump(dict_data, file_json, indent=2)

    print(f"Les données ont été enregistrées dans {path}.")

def save_yaml(dict_data, path, filename):
    with open(f"{path}/{filename}", 'w') as file_yaml:
        yaml.dump(dict_data, file_yaml)

    print(f"Les données ont été enregistrées dans {path}.")

def save_xml(dict_data, path, filename):
    data = ET.Element("data")
    for line in dict_data:
        child = ET.SubElement(data, "child")
        for key, value in line.items():
            sub_child = ET.SubElement(child, key)
            sub_child.text = str(value)

    tree = ET.ElementTree(data)
    with open(f"{path}/{filename}", "wb") as file_xml:
        tree.write(file_xml)
    print(f"Les données ont été enregistrées dans {path}.")

    