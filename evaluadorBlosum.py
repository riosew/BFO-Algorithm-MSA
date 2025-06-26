# import blosum as bl

# class evaluadorBlosum():
    
#     def __init__(self):
#         matrix = bl.BLOSUM(62)
        
#         self.matrix = matrix
        
#     def showMatrix(self):
#         print(self.matrix)
        
#     def getScore(self, A, B):
#         #si alguno de los dos es un gap
#         if A == "-" or B == "-":
#             return -3
#         score = self.matrix[A][B]
#         return score
    
    
#     pass




import blosum as bl

class evaluadorBlosum():
    
    def __init__(self):
        matrix = bl.BLOSUM(62)
        self.matrix = matrix

        # Obtener todos los valores únicos de la matriz
        valores = []
        for a in matrix:
            for b in matrix[a]:
                valores.append(matrix[a][b])
        
        self.min_score = min(valores)
        self.max_score = max(valores)

    def showMatrix(self):
        print(self.matrix)

    def getScore(self, A, B):
        if A == "-" or B == "-":
            return 0.0  # Asignamos 0 en caso de gap

        raw_score = self.matrix[A][B]

        # Normalización lineal a [0, 1]
        scaled_score = (raw_score - self.min_score) / (self.max_score - self.min_score)
        return scaled_score
