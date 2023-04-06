import pandas as pd

class Manager:
    def __init__(self) -> None:
        db = pd.DataFrame([], columns=[])
        module = []
        listofscopefields = []
        pass
    
    def init_db(self, listofcolumns = []):
        self.db = pd.DataFrame([], columns=listofcolumns)

    def create_db(self, listofcsvpaths : list):
        li = []
        module = []
        for file in listofcsvpaths:
            dbp = pd.read_csv(file, index_col=None, header=0)
            dbp["LSH_module"] = file
            module.append(file)
            li.append(dbp)
        db = pd.concat(li, axis=0, ignore_index=True)
        self.module = module
        self.db = db

    def add_data_by_str(self, listofdata : list):
        lendb = len(self.db.index)
        self.db.loc[lendb] = listofdata

    def append_modules_to_db(self, listofcsvpaths: list):
        li = []
        li.append(self.db)
        for file in listofcsvpaths:
            dbp = pd.read_csv(file, index_col=None, header=0)
            dbp["LSH_module"] = file
            self.module.append(file)
            li.append(dbp)
        db = pd.concat(li, axis=0, ignore_index=True)
        self.db = db
    
    def remove_modules_from_db(self, listofmodules : list):
        for module in listofmodules:
            self.db = self.db[self.db["LSH_module"].str.contains(module) == False]

    def define_scope(self, listofscopefields : list):
        self.db['text'] = self.db[listofscopefields].astype(str).agg(' '.join, axis=1)
        self.listofscopefield = listofscopefields

    def validate_db(self):
        label = "Start checking the database"
        currlen = ['=' for x in range(len(label))]
        print(''.join(currlen))
        print(label)
        print(''.join(currlen))
        label = "Following Modules found:"
        print(label)
        print(' '.join(self.module))
        print(''.join(currlen))
        try:
            if self.listofscopefield == []:
                raise BrokenPipeError("You have not marked any fields as scope, have you used the define_scope function?")
            else:
                label = "The follwoing Fields are used as Scope:"
                print(label)
                print(', '.join(self.listofscopefield))
        except:
            raise BrokenPipeError("You have not marked any fields as scope, have you used the define_scope function?")
        print(''.join(currlen))
        label = "The database check is completed successfully"
        print(label)

    def print_db(self):
        print(self.db)

h = Manager()
h.init_db()
h.create_db(["Base/a.csv", "Base/b.csv"])
h.append_modules_to_db(["Base/c.csv"])
h.print_db()
h.define_scope(["ID", "Name"])
print(h.listofscopefield)
h.print_db()
h.validate_db()