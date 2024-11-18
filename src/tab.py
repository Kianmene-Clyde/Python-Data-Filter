import json
import copy

from utils import *
from file_loader import *
from file_saver import *


class Tab:
    def __init__(self):

        self.file_path = None
        self.data = None # Liste des dicts -> Les dicts sont les lignes du tableau
        self.columns = None # Liste des colonnes
        self.columns_type = None


    def copy(self):
        tab_copy = Tab()
        tab_copy.data = copy.deepcopy(self.data)
        tab_copy.columns = copy.deepcopy(self.columns)
        tab_copy.columns_type = copy.deepcopy(self.columns_type)
        return tab_copy


    def size(self):
        return len(self.data)

    
    # def print_file_path(self):
    #     print(self.file_path)
        

    # def print_columns_type(self):
    #     print(self.columns_type)

    
    def show(self):

        data_dict = self.data 
        columns = self.columns
        
        cell_width = 12
        
        header = "|".join(column.center(cell_width) for column in columns)
        
        print(header)
        print("-" * len(header))
        
        for line in data_dict:
            
            list_cell_values = []
            for column in columns:
                cell_value = str(line[column])
                                 
                if(len(cell_value)>cell_width):
                    cell_value = cell_value[:cell_width-3]+"..."
    
                cell_value = cell_value.ljust(cell_width)
                list_cell_values.append(cell_value)
                    
            row ="|".join(list_cell_values)
            
            print(row)


    
    
    def save(self,filename,path,file_type):
        filename=f"{filename}.{file_type}"
        
        if file_type == 'csv':
            save_csv(self.data,path,filename)

        elif file_type == 'json':
            save_json(self.data,path,filename)

    
    def load(self,file_path): # Load un nouveau Tab depuis in fichier
        self.file_path = file_path

        file_type = get_file_type(file_path)
        
        if(file_type == 'csv'):
            data = load_csv(file_path)

        elif file_type == 'json':
            data = load_json(file_path)

            
        else:
            print(f"{file_type} is'nt supported")

        
        self.columns_type = get_column_types(data)
        self.columns = list(self.columns_type.keys())
                    
        self.data = data
                


    
    # def add_line(self, **kwargs):
    #     if not all(key in self.columns for key in kwargs.keys()):
    #         print("ERROR")
    #     else:
    #         line_dict = {column:None for column in self.columns}
    #         for key, value in kwargs.items():
    #             line_dict[key] = value

    #         self.data.append(line_dict)
    #         self.size += 1
            
    #     return self
        

    
    def add_columns(self,*new_columns):

        new_columns = list(set(new_columns)-set(self.columns))
        
        self.columns += new_columns
        
        for i in range (0,self.size()):
            
            for column in new_columns:
                self.data[i][column] = None
                
        return self
        

    def remove_columns(self,*columns):

        columns = list(set(columns)&set(self.columns))

        for column in columns:
            self.columns.remove(column)

        
        for i in range (0,self.size()):
            for column in columns:
                self.data[i].pop(column)
        return self

    
    def convert_column_type(self, column, type):
        
        if(type=="int"):
            self.columns_type[column]={"int"}
            for i,row in enumerate(self.data):
                try:
                    self.data[i][column] = int(row[column])
                except Exception:
                    self.data[i][column] = None
                    
        elif(type=="float"):
            self.columns_type[column]={"float"}
            for i,row in enumerate(self.data):
                try:
                    self.data[i][column] = float(row[column])
                except Exception:
                    self.data[i][column] = None
                    
        if(type=="str"):
            self.columns_type[column]={"str"}
            for i,row in enumerate(self.data):
                try:
                    self.data[i][column] = str(row[column])
                except Exception:
                    self.data[i][column] = None
        return self
    
        
    def statistics(self):
        stats = {column:{} for column in self.columns}
        sample = self.data[0]

        for column,type in self.columns_type.items():
            value = sample[column]
            if type == "int" or type == "float":
                stats[column]["Min"]= value
                stats[column]["Max"]= value
                stats[column]["Mean"]= value

            if type == "str":
                stats[column]["Min"]= value
                stats[column]["Max"]= value
                stats[column]["Most Frequent"]= [value]
                
        count = 0
        
        for row in self.data:
            count += 1
            for column,type in self.columns_type.items():
                value = row[column]
                
                try:
                    if type == "int" or type == "float":
                        
                        if(value < stats[column]["Min"]):
                            stats[column]["Min"]= value    
    
                        if(value > stats[column]["Max"]):
                            stats[column]["Max"]= value
    
                        stats[column]["Mean"] += value
                        
        
                    if type == "str" and value!=None:
                        
                        if(len(value) < len(stats[column]["Min"])):
                            stats[column]["Min"]= value    
    
                        if(len(value) > len(stats[column]["Max"])):
                            stats[column]["Max"]= value
                        
                        stats[column]["Most Frequent"].append(value)

                except TypeError:
                    pass
                    
        for column,type in self.columns_type.items():
            if type == "int" or type == "float":
                stats[column]["Mean"] = round(stats[column]["Mean"]/count,2)
                
            if type == "str":
                list = stats[column]["Most Frequent"]
                stats[column]["Most Frequent"] = max(set(list),key=list.count)

        print(json.dumps(stats, indent=4))


    
    def sort(self,column,reverse=False):
        infini = float('inf')
        if reverse:
            infini = float('-inf')

        # self.data = sorted(self.data,key=lambda x: sum_ord(str(x[column])) if x[column] is not None else infini, reverse = reverse)
        
        if(str in self.columns_type[column]):
            self.data = sorted(self.data,key=lambda x: sum_ord(str(x[column])) if x[column] is not None else infini, reverse = reverse)
            
        else:
            self.data = sorted(self.data,key=lambda x: x[column] if x[column] is not None else infini, reverse = reverse)            
        return self

    

    def filter(self,column,rel,value):
        
        sub_tab = Tab()
        
        sub_tab.columns = self.columns
        sub_tab.columns_type = self.columns_type
        sub_tab.data = []

        
        if(int in self.columns_type[column] or float in self.columns_type[column]):
            if(rel=="IS EQUAL"):
                for row in self.data:
                    # print(row[column])
                    if(row[column] == value):
                        sub_tab.data.append(row)
    
            if(rel=="IS GREATER THAN"):
                
                for row in self.data:
                    try:
                        if(row[column] > value):
                            sub_tab.data.append(row)
                    except TypeError:
                        pass
    
            if(rel=="IS GREATER THAN OR EQUAL"):
                for row in self.data:
                    try:
                        if(row[column] >= value):
                            sub_tab.data.append(row)
                    except TypeError:
                        pass
    
            if(rel=="IS LESS THAN"):
                for row in self.data:
                    try:
                        if(row[column] < value):
                            sub_tab.data.append(row)
                    except TypeError:
                        pass
                        
            if(rel=="IS LESS THAN OR EQUAL"):
                for row in self.data:
                    try:
                        if(row[column] <= value):
                            sub_tab.data.append(row)
                    except TypeError:
                        pass

        # Si la colonne est string
        elif(str in self.columns_type[column]):
            if(rel=="IS EQUAL"):
                
                for row in self.data:
                    if(row[column] == value):
                        sub_tab.data.append(row)
    
            if(rel=="IS GREATER THAN"):
                for row in self.data:
                    try:
                        if(sum_ord(row[column]) > value):
                            sub_tab.data.append(row)
                    except TypeError:
                        pass
    
            if(rel=="IS GREATER OR EQUAL THAN"):
                for row in self.data:
                    try:
                        if(sum_ord(row[column]) >= value):
                            sub_tab.data.append(row)
                    except TypeError:
                        pass
    
            if(rel=="IS LESS THAN"):
                for row in self.data:
                    try:
                        if(sum_ord(row[column]) < value):
                            sub_tab.data.append(row)
                    except TypeError:
                        pass
                        
            if(rel=="IS LESS OR EQUAL THAN"):
                for row in self.data:
                    try:
                        if(sum_ord(row[column]) <= value):
                            sub_tab.data.append(row)
                    except TypeError:
                        pass       
                    
        return sub_tab
