import pandas as pd
from io import StringIO

class Manager:
    def __init__(self) -> None:
        db = pd.DataFrame([], columns=[])
        module = []
        listofscopefields = []
        pass
    
    def init_db(self, listofcolumns = []):
        """
        Initializes a new, empty Database, that you can fill with your LSH needs.

        Args:
            listofcolumns (list, optional): Pass a List of Names, to intialize Database with predefined Column Names. Defaults to [].
        """
        self.db = pd.DataFrame([], columns=listofcolumns)

    def create_db(self, csvtype : list | str):
        """
        Creates a database based on a CSV, this CSV can be passed as a CSV file or as a CSV string.

        Args:
            csvtype (list | str): A CSV can be passed as a CSV file or as a CSV string.
        """
        li = []
        module = []
        if type(csvtype) == list:
            for file in csvtype:
                dbp = pd.read_csv(file, index_col=None, header=0)
                dbp["LSH_module"] = file
                module.append(file)
                li.append(dbp)
            db = pd.concat(li, axis=0, ignore_index=True)
        elif type(csvtype) == str:
            csvStringIO = StringIO(csvtype)
            db = pd.read_csv(csvStringIO, index_col=None, header=0)
            db["LSH_module"] = "StringImport"
            module.append("StringImport")
        self.module = module
        self.db = db

    def add_data_by_str(self, listofdata : list):
        """
        Insert data as CSV string into your database, the transferred data will be integrated into the fields of the database one after the other.

        Args:
            listofdata (list): CSV data can be transferred as a string in a list.
        """
        lendb = len(self.db.index)
        self.db.loc[lendb] = listofdata

    def append_modules_to_db(self, listofcsvpaths: list):
        """
        Inserts new modules (other external, separate CSV files) into the database.

        Args:
            listofcsvpaths (list): A list of the paths to the external CSV files is required.
        """
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
        """
        Deletes external, integrated modules from the database.

        Args:
            listofmodules (list): A list of module names to be removed from the database is required.
        """
        for module in listofmodules:
            self.db = self.db[self.db["LSH_module"].str.contains(module) == False]

    def define_scope(self, listofscopefields : list):
        """
        Sets the search scope in which LSH (Locality-Sensitive Hashing) is executed.

        Args:
            listofscopefields (list): A list of the fields that shall be queried during LSH execution
        """
        self.db['text'] = self.db[listofscopefields].astype(str).agg(' '.join, axis=1)
        self.listofscopefield = listofscopefields

    def save_model_as_csv(self):
        """
        Saves the current database as a CSV in a string.

        Returns:
            str: A CSV in a string.
        """
        return self.db.to_csv()
    
    def validate_db_internal(self):
        """
        Validates the current database for the requirements of an LSH execution.

        Raises:
            BrokenPipeError: No search area has been defined for the LSH request. 
            BrokenPipeError: No search area has been defined for the LSH request. 
        """
        try:
            if self.listofscopefield == []:
                raise BrokenPipeError("You have not marked any fields as scope, have you used the define_scope function?")
        except:
            raise BrokenPipeError("You have not marked any fields as scope, have you used the define_scope function?")
        
    def validate_db(self):
        """
        Validates the current database for the requirements of an LSH execution, but with Interface.

        Raises:
            BrokenPipeError: No search area has been defined for the LSH request
            BrokenPipeError: No search area has been defined for the LSH request
        """
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
        """
        Prints the current Database.
        """
        print(self.db)

h = Manager()
h.init_db()
h.create_db("ID,Name\n 1,ABC")
h.append_modules_to_db(["Base/c.csv"])
h.print_db()
h.define_scope(["ID", "Name"])
print(h.listofscopefield)
h.print_db()
h.validate_db()