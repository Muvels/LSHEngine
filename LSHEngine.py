import utils
from utils import LSHFuncs
from utils.huffman import huffman as bin_codec
from ModelManager import LSHClientDB as DB_Client
class Engine:
    def __init__(self) -> None:
        storage = ''
        model = DB_Client.Manager()
        perms = 128
        num_recommendations = 5
        ismodelloaded = False
        forest = []
        pass
    
    def GO(self):
        self.model = DB_Client.Manager()
        self.perms = 128
        self.num_recommendations = 5

    def train_forest(self): 
        trained = LSHFuncs.get_forest(self.model.db, self.perms)
        self.forest = trained
        return trained
    
    def recommendations(self, text, num_recommendations = None, as_df: bool = True):
        if num_recommendations != None:
            recommendations = utils.LSHFuncs.predict(text, self.model.db, self.perms, num_recommendations, self.forest)
        else:
            recommendations = utils.LSHFuncs.predict(text, self.model.db, self.perms, self.num_recommendations, self.forest)
        if as_df == False:
            return recommendations
        else:
            recommendations = recommendations.to_frame()
            return recommendations
    
    def save_model_to_bin(self,path_to_bin: str):
        self.storage = self.model.save_model_as_csv()
        bin_codec.Compress.compress_from_storage(path_to_bin, self.storage)
    
    def load(self,path_to_bin: str, define_current_scope : list = [], include_BaseModel: bool = False):
        if not include_BaseModel:
            self.storage = bin_codec.decompress_to_var(path_to_bin).process_to_var()
            self.model.create_db(self.storage)
            if define_current_scope != []:
                self.model.define_scope(define_current_scope)
                self.model.validate_db_internal()
            self.ismodelloaded = True
        else:
            raise NotImplementedError('Basemodel will be added with ModelManager in Future Release of LSHEngine')
    
    def include_custom_manager(self, ManagerClass):
        self.model = ManagerClass
    
    def define_current_scope(self,listofscopefields):
        self.model.define_scope(listofscopefields)

    def printcurrentmodel(self):
        print(self.storage)
    
    def is_model_loaded(self):
        return self.ismodelloaded



b = DB_Client.Manager()
b.init_db()
b.create_db(["unittests/a.csv", "unittests/b.csv"])
b.define_scope(["ID","Name"])

h = Engine()
h.GO()
h.include_custom_manager(b)
h.save_model_to_bin("abc.bin")
#h.load("abc.bin")
#h.define_current_scope(["ID", "Name"])
h.printcurrentmodel()
h.train_forest()
query = h.recommendations("2")
print(query)

