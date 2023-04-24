import time
from .lshforest import MinHashLSHForest
from .minhash import MinHash
from .preprocess import preprocess
import numpy as np

def get_forest(data, perms):
    start_time = time.time()
    
    minhash = []
    
    for text in data['text']:
        tokens = preprocess(text)
        m = MinHash(num_perm=perms)
        for s in tokens:
            m.update(s.encode('utf8'))
        minhash.append(m)
        
    forest = MinHashLSHForest(num_perm=perms)
    
    for i,m in enumerate(minhash):
        forest.add(i,m)
        
    forest.index()
    
    print('It took %s seconds to build forest.' %(time.time()-start_time))
    
    return forest

def predict(text, database, perms, num_results, forest):
    start_time = time.time()
    
    tokens = preprocess(text)
    m = MinHash(num_perm=perms)
    for s in tokens:
        m.update(s.encode('utf8'))
        
    idx_array = np.array(forest.query(m, num_results))
    if len(idx_array) == 0:
        return None # if your query is empty, return none
    
    result = database.iloc[idx_array]

    jaccardval = []
    for r in range(len(idx_array)):
        n = MinHash(num_perm=perms)
        tokens = preprocess(result.iloc[r]["text"])
        for s in tokens:
            n.update(s.encode('utf8'))
        jaccardval.append(m.jaccard(n))
    result["jaccard_value"] = jaccardval
    print('It took %s seconds to query forest.' %(time.time()-start_time))
    
    return result