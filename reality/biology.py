import numpy as np
import math
import pickle
from settings import *

def gene_expression(size):
    '''
    How genes express to phenotype.
    I choose here a bimodal distribution so each gen either contribute a lot (~1) or very few (~0) to each trait.
    '''
    # sample = np.concatenate((np.random.normal(0., 0.1, int(math.ceil(size/2))),
    #                 np.random.normal(1., 0.1, int(math.floor(size/2)))))
    sample = np.random.beta(0.1, 0.1, size)
    np.random.shuffle(sample)
    return sample

class Genetics:
    '''
    Class of genetics. Define the relation, once and for all, between genes and phenotype
    '''

    def __init__(self):
        
        self.w = {}
        for trait in TRAITS:
            self.w[trait] = gene_expression(GEN_SIZE)      

    def __eq__(self, other): 
        if not isinstance(other, Genetics):
            # don't attempt to compare against unrelated types
            return NotImplemented
        check = True
        for trait in TRAITS:
            check = check and np.array_equal(self.w[trait], other.w[trait])
        return check
        

class Biology:

    def __init__(self, genetics = Genetics(), gestationtime=90, name='homo-virtualis'):            
        self.gestationtime = gestationtime        
        self.genetics = genetics
        self.meiosis_variation = 0.1 # mean value of Poisson distribution for nr of genes suffering mutation
        self.name = name

    def __eq__(self, other): 
        if not isinstance(other, Biology):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.name == other.name and self.gestationtime == other.gestationtime and \
                self.genetics == other.genetics and self.meiosis_variation == other.meiosis_variation


    def get_info(self):
        #return f'gestation time: {self.gestationtime} \n genetics: {self.genetics.w} \n meiosis_variation: {self.meiosis_variation}'  
        #return f'The species is characterized by a genetics, gestation time: {self.gestationtime}, meiosis_variation: {self.meiosis_variation}'  
        return f'The species {self.name} is characterized by a genetics and meiosis_variation: {self.meiosis_variation}'  

    def save(self):
        filename = f'./data/biologies/{self.name}.pickle'
        with open(filename, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    def load(self, name):
        with open(f'./data/biologies/{name}.pickle', 'rb') as f:
            self = pickle.load(f)      
        return self        

biology = Biology()

