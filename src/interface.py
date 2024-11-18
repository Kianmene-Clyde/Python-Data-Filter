import tkinter as tk
from tkinter import ttk,simpledialog

from src.tab import Tab


# Fonction bouton load new table de la table
def load_table(c_tab=None):
    
    #New tab
    tab = Tab()
    
    if(c_tab is None):
        user_input = simpledialog.askstring("Load new table", "Enter your file path :")
        
        if user_input is not None:
            # Chargemant de Tab
            tab.load(user_input)
    else:
        tab = c_tab

    
    #tab copy
    original_tab = tab.copy()
    
    #Liste des modifications
    modifications = []
    curr_mod = 0
    
    root = tk.Tk()
    root.title(tab.file_path)


    # Treeview pour faire des tableaux
    tree = ttk.Treeview(root)
    
    def modification_changes():
        nonlocal curr_mod
        nonlocal modifications
        modifications = modifications[:curr_mod+1]
        modifications.append(tab.copy())
        curr_mod+=1
        
    modification_changes()
    
    def add_column():
        nonlocal tab
        nonlocal curr_mod
        nonlocal modifications

        def apply_add():
            nonlocal tab
            nonlocal curr_mod
            nonlocal modifications

            column = variable_column.get()
            
            for item in tree.get_children():
                tree.delete(item)
            
            tab = tab.add_columns(column)
            # tab.show()
            
            tree["columns"] = tab.columns
            
            # Mettez à jour votre tableau avec les nouvelles dimensions
            tree.update_idletasks()

            for col in columns:
                tree.column(col, anchor="center")
                tree.heading(col, text=col, anchor="center")
            
            for item in tab.data:
                values = [item[col] for col in tab.columns]
                tree.insert("", "end", values=values)
                
            # modification_changes()
            # modifications[-1].show()

            root.destroy()
            
        
        root = tk.Tk()
        root.title("Column")

        # variables
        variable_column = ttk.Entry(root)
        variable_column.grid(row=2, column=1, padx=10,pady=5)

        # Bouton add
        button_sort = ttk.Button(root, text="Add", command=apply_add)
        button_sort.grid(row=3, column=0, columnspan=2, pady=10)    


    
    def remove_column():
        nonlocal tab
        nonlocal curr_mod
        nonlocal modifications

        def apply_remove():
            nonlocal tab
            nonlocal curr_mod
            nonlocal modifications

            column = variable_column.get()
            
            for item in tree.get_children():
                tree.delete(item)
            
            tab = tab.remove_columns(column)

            tree.column(column, width=0, stretch=tk.NO)
            tree.heading(column, text="")
            
            # Mettez à jour votre tableau avec les nouvelles dimensions
            tree.update_idletasks()
            
            for item in tab.data:
                values = [item[col] for col in tab.columns]
                tree.insert("", "end", values=values)
                
            modification_changes()
            root.destroy()
            
    
        root = tk.Tk()
        root.title("Remove column")

        # variables
        variable_column = tk.StringVar(root)
        
        # Menu déroulant colonnes
        label_column = ttk.Label(root, text="Column")
        tmp = [""]+tab.columns
        menu_column = ttk.OptionMenu(root, variable_column, *tmp)
    
        label_column.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        menu_column.grid(row=0, column=1, padx=10, pady=5)
        # user_input = simpledialog.askstring("Sort table", "On :")
    
        # Bouton remove
        button_sort = ttk.Button(root, text="Remove", command=apply_remove)
        button_sort.grid(row=3, column=0, columnspan=2, pady=10)
            
        
    
    def reset():
        nonlocal tab
        nonlocal curr_mod
        nonlocal modifications
        
        for item in tree.get_children():
            tree.delete(item)

        for item in original_tab.data:
            values = [item[col] for col in columns]
            tree.insert("", "end", values=values)
            
        tab = curr_mod[0]
        modification_changes()

        
    def sort_table():
        nonlocal tab
        nonlocal curr_mod
        nonlocal modifications
        # nonlocal modifications
        
        def apply_sort():
            # modifications[0].show()
            nonlocal tab
            nonlocal curr_mod
            nonlocal modifications
            # Effacer le tableau (tree)
            for item in tree.get_children():
                tree.delete(item)

            column = variable_column.get()
            reverse = variable_reverse.get() == "Yes" 
            sorted_tab = tab.sort(column=column,reverse=reverse)
            
            for item in sorted_tab.data:
                values = [item[col] for col in columns]
                tree.insert("", "end", values=values)

            tab = sorted_tab

            # Modifications sauvegarde
            modification_changes()



        root = tk.Tk()
        root.title("Sort")
        
        # variables
        variable_column = tk.StringVar(root)
        variable_reverse = tk.StringVar(root)
        
        # Menu déroulant colonnes
        label_column = ttk.Label(root, text="Column")
        tmp = [""]+tab.columns
        menu_column = ttk.OptionMenu(root, variable_column, *tmp)

        # Menu déroulant colonnes
        label_reverse = ttk.Label(root, text="Reverse")
        tmp_reverse = ["","No","Yes"]
        menu_column_reverse = ttk.OptionMenu(root, variable_reverse, *tmp_reverse)
    
        label_column.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        menu_column.grid(row=0, column=1, padx=10, pady=5)

        label_reverse.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        menu_column_reverse.grid(row=1, column=1, padx=10, pady=5)
    
        # Bouton sort
        button_sort = ttk.Button(root, text="Sort", command=apply_sort)
        button_sort.grid(row=3, column=0, columnspan=2, pady=10)

        

    
    # Fonction bouton filter de la table
    def filter_table():
        nonlocal tab         
        nonlocal modifications
        nonlocal curr_mod
        
        
        def apply_filter():
            nonlocal tab
            nonlocal modifications
            nonlocal curr_mod
            
            for item in tree.get_children():
                tree.delete(item)
            
            column = variable_column.get()
            rel = variable_filter.get()
            value = variable_value.get()      


            if(rel=="IS EQUAL" and str in tab.columns_type[column]):
                print("HERE")
                filter_tab = tab.filter(column=column,rel=rel,value=value)
            else:
                filter_tab = tab.filter(column=column,rel=rel,value=int(value))
            # root.destroy()
            # load_table(c_tab = filter_tab)
            for item in filter_tab.data:
                values = [item[col] for col in columns]
                tree.insert("", "end", values=values)
                
            tab = filter_tab

            
            # Modifications sauvegarde
            modification_changes()

                
        root = tk.Tk()
        root.title("Filter")
        
        
        # variables
        variable_column = tk.StringVar(root)
        variable_filter = tk.StringVar(root)
        variable_value = tk.StringVar(root)
        
    
        # Menu déroulant colonnes
        label_column = ttk.Label(root, text="Column")
        tmp = [""]+tab.columns
        menu_column = ttk.OptionMenu(root, variable_column, *tmp)
    
    
        label_column.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        menu_column.grid(row=0, column=1, padx=10, pady=5)
        
        # Menu déroulant filtres
        filters = ["","IS EQUAL","IS GREATER THAN","IS GREATER THAN OR EQUAL","IS LESS THAN","IS LESS THAN OR EQUAL"]
        
        label_filter = ttk.Label(root, text="Filter:")
        menu_filter = ttk.OptionMenu(root, variable_filter, *filters)
        label_filter.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        menu_filter.grid(row=1, column=1, padx=10, pady=5)
        
        # value
        label_value = ttk.Label(root, text="Value:")
        variable_value = ttk.Entry(root)
        label_value.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        variable_value.grid(row=2, column=1, padx=10, pady=5)
        
        # Bouton filter
        button_filter = ttk.Button(root, text="Filter", command=apply_filter)
        button_filter.grid(row=3, column=0, columnspan=2, pady=10)

            
    def convert_type():
        nonlocal tab
        nonlocal curr_mod
        nonlocal modifications
        # nonlocal modifications
        
        def apply_convert():
            # modifications[0].show()
            nonlocal tab
            nonlocal curr_mod
            nonlocal modifications
            # Effacer le tableau (tree)
            for item in tree.get_children():
                tree.delete(item)

            column = variable_column.get()
            type = variable_type.get()
            
            convert_tab = tab.convert_column_type(column=column,type=type)
            
            for item in convert_tab.data:
                values = [item[col] for col in columns]
                tree.insert("", "end", values=values)

            tab = convert_tab

            # Modifications sauvegarde
            modification_changes()



        root = tk.Tk()
        root.title("Sort")
        
        # variables
        variable_column = tk.StringVar(root)
        variable_type = tk.StringVar(root)
        
        # Menu déroulant colonnes
        label_column = ttk.Label(root, text="Column")
        tmp = [""]+tab.columns
        menu_column = ttk.OptionMenu(root, variable_column, *tmp)

        # Menu déroulant colonnes
        label_type = ttk.Label(root, text="Type")
        tmp_type = ["","int","float","str"]
        menu_column_type = ttk.OptionMenu(root, variable_type, *tmp_type)
    
        label_column.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        menu_column.grid(row=0, column=1, padx=10, pady=5)

        label_type.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        menu_column_type.grid(row=1, column=1, padx=10, pady=5)
    
        # Bouton convert
        button_sort = ttk.Button(root, text="Convert", command=apply_convert)
        button_sort.grid(row=3, column=0, columnspan=2, pady=10)

    
    def undo_redo(incr):
        nonlocal tab
        nonlocal modifications
        nonlocal curr_mod
        
        
        if(0<=curr_mod+incr<len(modifications)):
            
            for item in tree.get_children():
                tree.delete(item)

            curr_mod += incr

            to_delete_col = [col for col in tab.columns if col not in modifications[curr_mod].columns]
            
            for column in to_delete_col:
                tab = tab.remove_columns(column)
                tree.column(column, width=0, stretch=tk.NO)
                tree.heading(column, text="")
                
                # Mettez à jour votre tableau avec les nouvelles dimensions
                tree.update_idletasks()


            
            tab = modifications[curr_mod]

            print(curr_mod)
            print(modifications[curr_mod].columns)
            
            tree["columns"] = tab.columns
            
            # Mettez à jour votre tableau avec les nouvelles dimensions
            tree.update_idletasks()

            for col in columns:
                tree.column(col, anchor="center")
                tree.heading(col, text=col, anchor="center")

            
            for item in tab.data:
                values = [item[col] for col in columns]
                tree.insert("", "end", values=values) 
    
    
    # Fonction bouton sauvegarde de la table
    def save_table():
        nonlocal tab
        
        def save():
            nonlocal tab
            
            path = entry_path.get()
            filename = entry_filename.get()
            file_type = variable_type.get()
        
            if path and filename and file_type:
                result_string = f"{path}/{filename}.{file_type}"
                print(result_string)
                tab.save(filename,path,file_type)
                root.destroy()
            else:
                print("Veuillez remplir tous les champs.")
        
        # Creation fenetre
        root = tk.Tk()
        root.title("Save table")
        
        # les champs d entrées
        label_path = ttk.Label(root, text="Path:")
        entry_path = ttk.Entry(root)
        
        label_filename = ttk.Label(root, text="File name:")
        entry_filename = ttk.Entry(root)
        
        # label_type = ttk.Label(root, text="Type:")
        # entry_type = ttk.Entry(root)
    
        # Menu déroulant type
        type = ["","csv","json"]
        
        variable_type = tk.StringVar(root)
        label_type = ttk.Label(root, text="Type:")
        menu_type = ttk.OptionMenu(root, variable_type, *type)
        
        
        # Bouton save
        button_save = ttk.Button(root, text="Save", command=lambda : save(tab))
        
        # Grille de bouton
        label_path.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        entry_path.grid(row=0, column=1, padx=10, pady=5)
        
        label_filename.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        entry_filename.grid(row=1, column=1, padx=10, pady=5)
        
        label_type.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        menu_type.grid(row=2, column=1, padx=10, pady=5)
        
        button_save.grid(row=3, column=0, columnspan=2, pady=10)

    
    button_load = ttk.Button(root, text="Load new table", command=load_table)
    button_add_column = ttk.Button(root, text="Add column", command=add_column)
    button_remove_column = ttk.Button(root, text="Remove column", command=remove_column)
    button_filter = ttk.Button(root, text="Filter", command=lambda : filter_table())
    button_save = ttk.Button(root, text="Save table", command=lambda: save_table())
    button_sort_table = ttk.Button(root, text="Sort Table", command=lambda: sort_table())
    button_convert_type = ttk.Button(root, text="Convert Type", command=lambda: convert_type())
    button_reset = ttk.Button(root, text="Reset", command=lambda : reset())
    button_undo = ttk.Button(root, text="Undo", command=lambda : undo_redo(-1))
    button_redo = ttk.Button(root, text="Redo", command=lambda : undo_redo(1))
    

    button_load.grid(row=0, column=1)
    button_save.grid(row=0, column=2)
    button_add_column.grid(row=0, column=3)
    button_remove_column.grid(row=0, column=4)
    button_filter.grid(row=0, column=5)
    button_sort_table.grid(row=0, column = 6)
    button_convert_type.grid(row=0,column=7)
    button_reset.grid(row=0,column=8)
    button_undo.grid(row=0,column=9)
    button_redo.grid(row=0,column=10)
    
    columns = tab.columns
    
    def tree_config():
        nonlocal tree
        nonlocal columns
        # scroll barre
        horizontal_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=horizontal_scrollbar.set)
            
            
        # les colonnes
        
        tree["columns"] = columns
            
        for col in columns:
            tree.column(col, anchor="center")
            tree.heading(col, text=col, anchor="center")
            
        # les lignes
        for item in tab.data:
            values = [item[col] for col in columns]
            tree.insert("", "end", values=values)
            
        # treeview config
        tree.grid(row=1, column=0, columnspan=20, padx=10, pady=10, sticky="nsew")
        horizontal_scrollbar.grid(row=2, column=0, columnspan=4, sticky="ew")
        
        
        # truc de redimenssionnement
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        
    tree_config()
    
    root.mainloop()


# lancement de l'interface
def launch():
    root = tk.Tk()
    root.geometry("400x400")
    root.title("Data Filter")
    root.resizable(height=True,width=True)
    
    title_label = ttk.Label(root, text="Data Filter", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=5)
    
    button = ttk.Button(root, text="Load table", command=load_table)
    button.pack(padx=10, pady=10)
    
    root.mainloop()