import utils
from utils.huffman import huffman as bin_codec
class Engine:
    def __init__(self) -> None:
        storage = ''
        ismodelloaded = False
        pass

    def train_forest(): 
        trained = utils.LSHFuncs.get_forest()
        return trained
    
    def recommendations(as_df: bool):
        recommendations = utils.LSHFuncs.predict()
        if as_df == False:
            return recommendations
        else:
            recommendations = recommendations.to_frame()
            return recommendations
    
    def save_model_to_bin(self,path_to_bin: str):
        bin_codec.Compress.compress_from_storage(path_to_bin, self.storage)
    
    def load(self,path_to_bin: str, include_BaseModel=False):
        if not include_BaseModel:
            self.storage = bin_codec.decompress_to_var(path_to_bin).process_to_var()
            self.ismodelloaded = True
        else:
            raise ReferenceError('Basemodel will be added with ModelManager in Future Release of LSHEngine')
    def printcurrentmodel(self):
        print(self.storage)
    
    def is_model_loaded(self):
        return self.ismodelloaded

h = Engine()
h.load("abc.bin")
h.save_model_to_bin("abc.bin")

