import blosum as bl

class evaluadorBlosum():
    
    def __init__(self):
        matrix = bl.BLOSUM(62)
        
        self.matrix = matrix
        
    def showMatrix(self):
        print(self.matrix)
        
    def getScore(self, A, B):
        #si alguno de los dos es un gap
        if A == "-" or B == "-":
            return -0.1
        score = self.matrix[A][B]
        return score
    
    
    pass




