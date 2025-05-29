import numpy
from multiprocessing import Manager

class fastaReader():
    

    def __init__(self):
        self.path = "C:\\secuenciasBFOA\\multifasta.fasta"  #valida si el path existe (para el caso de estar en CNS o PC local)
        try:
            f = open(self.path, "r")
            f.close()
            
        except: self.path = "multifasta.fasta"    #CNS
        
        
        self.seqs = list()
        self.names = list()
        self.read()
    
    
    def read(self):
        f = open(self.path, "r")
        lines = f.readlines()
        f.close()
        seq = ""
        for line in lines:
            if line[0] == ">":
                self.names.append(line[1:].strip())
                if seq != "":
                    self.seqs.append(seq)
                seq = ""
            else:
                seq += line.strip()
        self.seqs.append(seq)
    
    
    