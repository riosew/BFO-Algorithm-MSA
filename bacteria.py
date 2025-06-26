import copy
import math
from multiprocessing import Manager, Pool, managers
from pickle import FALSE, TRUE
from evaluadorBlosum import evaluadorBlosum
import numpy
from fastaReader import fastaReader
import random
from copy import copy, deepcopy
import copy
import concurrent.futures
import time


class bacteria():
    

    def __init__(self, numBacterias):
        # manager = Manager()
        manager = Manager()
        self.blosumScore = manager.list(range(numBacterias))
        self.tablaAtract = manager.list(range(numBacterias))
        self.tablaRepel = manager.list(range(numBacterias))
        self.tablaInteraction = manager.list(range(numBacterias))
        self.tablaFitness = manager.list(range(numBacterias))
        self.granListaPares = manager.list(range(numBacterias))
        self.NFE = manager.list(range(numBacterias))

    def resetListas(self, numBacterias):
        manager = Manager()
        self.blosumScore = manager.list(range(numBacterias))
        self.tablaAtract = manager.list(range(numBacterias))
        self.tablaRepel = manager.list(range(numBacterias))
        self.tablaInteraction = manager.list(range(numBacterias))
        self.tablaFitness = manager.list(range(numBacterias))
        self.granListaPares = manager.list(range(numBacterias))
        self.NFE = manager.list(range(numBacterias))
        
        
  
    def cuadra(self, numSec, poblacion):
        #ciclo para recorrer poblacion
        for i in range(len(poblacion)):
            #obtiene las secuencias de la bacteria
            bacterTmp = poblacion[i]
            # print("bacterTmp: ", bacterTmp)
            bacterTmp = list(bacterTmp)
            # print("bacterTmp: ", bacterTmp)
            bacterTmp = bacterTmp[:numSec]
            # obtiene el tamaño de la secuencia más larga
            maxLen = 0
            for j in range(numSec):
                if len(bacterTmp[j]) > maxLen:
                    maxLen = len(bacterTmp[j])
                    #rellena con gaps las secuencias más cortas
                    for t in range(numSec):
                        gap_count = maxLen - len(bacterTmp[t])
                        if gap_count > 0:
                            bacterTmp[t].extend(["-"] * gap_count)
                            #actualiza la poblacion
                            poblacion[i] = tuple(bacterTmp)
                            
            
        
        
        
        



    """metodo que recorre la matriz y elimina las columnas con gaps en todos los elementos"""
    def limpiaColumnas(self):
        i = 0
        while i < len(self.matrix.seqs[0]):
            if self.gapColumn(i):
                self.deleteCulmn(i)
            else:
                i += 1
  
                
            
        """metodo para eliminar un elemento especifico en cada secuencia"""
    def deleteCulmn(self, pos):
        for i in range(len(self.matrix.seqs)):
            self.matrix.seqs[i] = self.matrix.seqs[i][:pos] + self.matrix.seqs[i][pos+1:]



    """metodo para saber si alguna columna de self.matrix tiene  gap en todos los elementos"""
    def gapColumn(self, col):
        for i in range(len(self.matrix.seqs)):
            if self.matrix.seqs[i][col] != "-":
                return False
        return True
    
    

    def tumbo(self, numSec, poblacion, numGaps):
        #inserta un gap en una posicion aleatoria de una secuencia aleatoria
        #recorre la poblacion
        for i in range(len(poblacion)):
            #obtiene las secuencias de la bacteria
            bacterTmp = poblacion[i]
            bacterTmp = list(bacterTmp)
            # bacterTmp = bacterTmp[:numSec]
            #ciclo para insertar gaps
            for j in range(numGaps):
                #selecciona secuencia
                seqnum = random.randint(0, len(bacterTmp)-1)
                #selecciona posicion
                pos = random.randint(0, len(bacterTmp[seqnum]))
                part1 = bacterTmp[seqnum][:pos]
                part2 = bacterTmp[seqnum][pos:]
                temp = part1 + ["-"] + part2
                bacterTmp[seqnum] = temp
                #actualiza la poblacion
                poblacion[i] = tuple(bacterTmp)
                

    #crea un metodo de nado, donde se van a eliminar gaps aleatorios de las secuencias
    def nado(self, numSec, poblacion, numGapsToDelete):
        #recorre la poblacion
        #crea una tupla 
        gapPositions = []
        for i in range(len(poblacion)):
            #obtiene las secuencias de la bacteria
            bacterTmp = poblacion[i]
            bacterTmp = list(bacterTmp)
            #cuenta los gaps en la bacteria
            gapCount = 0
            for j in range(len(bacterTmp)):
                for k in range(len(bacterTmp[j])):
                    if bacterTmp[j][k] == "-":
                        gapPositions.append((j, k))
                       
            #si la tupla tiene longitur mayor a numGapsToDelete
            if len(gapPositions) > numGapsToDelete:
                #elimina gaps aleatorios
                for j in range(numGapsToDelete):
                    #selecciona una posicion aleatoria de la tupla
                    pos = random.randint(0, len(gapPositions)-1)
                    #elimina el gap de la secuencia
                    bacterTmp[gapPositions[pos][0]] = bacterTmp[gapPositions[pos][0]][:gapPositions[pos][1]] + bacterTmp[gapPositions[pos][0]][gapPositions[pos][1]+1:]
                    #elimina la posicion de la tupla
                    gapPositions = gapPositions[:pos] + gapPositions[pos+1:]
                    
            #actualiza la poblacion
            poblacion[i] = tuple(bacterTmp)        
                        
              

       
            
    def creaGranListaPares(self, poblacion):   
        # granListaPares = list(range(len(poblacion)))
        #ciclo para recorrer poblacion
        for i in range(len(poblacion)):  #recorre poblacion
            pares = list()
            bacterTmp = poblacion[i]
            bacterTmp = list(bacterTmp)
            #ciclo para recorrer secuencias
            for j in range(len(bacterTmp)):     #recorre secuencias de bacteria
                column = self.getColumn(bacterTmp, j)
                pares = pares + self.obtener_pares_unicos(column)
            self.granListaPares[i] = pares
            # print("Bacteria: ", i, " Pares: ", pares)
            
        # return self.granListaPares
    


    def evaluaFila(self, fila, num):
        evaluador = evaluadorBlosum()
        score = 0
        for par in fila:
            score += evaluador.getScore(par[0], par[1])
        self.blosumScore[num] = score
    
    def evaluaBlosum(self):
        with Pool() as pool:
            args = [(copy.deepcopy(self.granListaPares[i]), i) for i in range(len(self.granListaPares))]
            pool.starmap(self.evaluaFila, args)


    def getColumn(self, bacterTmp, colNum):
        column = []
        #obtiene las secuencias de la bacteria
        # bacterTmp = poblacion[bactNum]
        # bacterTmp = list(bacterTmp)
        #obtiene el caracter de cada secuencia en la columna
        for i in range(len(bacterTmp)):
            column.append(bacterTmp[i][colNum])
        return column
            
        
            
    

    def obtener_pares_unicos(self, columna):
        pares_unicos = set()
        for i in range(len(columna)):
            for j in range(i+1, len(columna)):
                par = tuple(sorted([columna[i], columna[j]]))
                pares_unicos.add(par)
        return list(pares_unicos)  

    #------------------------------------------------------------Atract y Repel lineal
    
    def compute_diff_Atract(self, args):
        indexBacteria, otherBlosumScore, self.blosumScore, d, w = args
        diff = (self.blosumScore[indexBacteria] - otherBlosumScore) ** 2.0
        # print("self Blsm: ",self.blosumScore[indexBacteria], " OtherBlsm: ", otherBlosumScore )
        self.NFE[indexBacteria] += 1
        diff = d * numpy.exp(w * diff)
        # print("diff: ",diff, " selfBlosum: ", self.blosumScore[indexBacteria], " otherBlsm: ", otherBlosumScore)
        return diff

    def compute_diff_Repel(self, args):
        indexBacteria, otherBlosumScore, self.blosumScore, d, w = args
        diff = (self.blosumScore[indexBacteria] - otherBlosumScore) ** 2.0
        # print("self Blsm: ",self.blosumScore[indexBacteria], " OtherBlsm: ", otherBlosumScore )
        self.NFE[indexBacteria] += 1
        diff = d * numpy.exp(w * diff)
        # print("diff: ",diff, " selfBlosum: ", self.blosumScore[indexBacteria], " otherBlsm: ", otherBlosumScore)
        return diff


    # def compute_diff(self, args):
    #     indexBacteria, otherBlosumScore, self.blosumScore, d, w = args
    #     diff = (self.blosumScore[indexBacteria] - otherBlosumScore) ** 2.0
    #     # print("self Blsm: ",self.blosumScore[indexBacteria], " OtherBlsm: ", otherBlosumScore )
    #     self.NFE[indexBacteria] += 1
    #     diff = d * numpy.exp(w * diff)
    #     print("diff: ",diff, " selfBlosum: ", self.blosumScore[indexBacteria], " otherBlsm: ", otherBlosumScore)
    #     return diff
        

    # def compute_cell_interaction(self, indexBacteria, d, w, atracTrue):
    #     with Pool() as pool:
    #         args = [(indexBacteria, otherBlosumScore, deepcopy(self.blosumScore), d, w) for otherBlosumScore in deepcopy(self.blosumScore)]
    #         results = pool.map(self.compute_diff, args)
    #         pool.close()  # Close the pool to prevent any more tasks from being submitted
    #         pool.join()   # Wait for the worker processes to exit
    
    #     total = sum(results)
    
    #     if atracTrue:
    #         self.tablaAtract[indexBacteria] = total
    #     else:
    #         self.tablaRepel[indexBacteria] = total
    #     results = None
    #     total = None
        

    def compute_cell_interaction_Atract(self, indexBacteria, d, w, atracTrue):
        with Pool() as pool:
            args = [(indexBacteria, otherBlosumScore, deepcopy(self.blosumScore), d, w) for otherBlosumScore in deepcopy(self.blosumScore)]
            results = pool.map(self.compute_diff_Atract, args)
            pool.close()  # Close the pool to prevent any more tasks from being submitted
            pool.join()   # Wait for the worker processes to exit
    
        total = sum(results)
    
        if atracTrue:
            self.tablaAtract[indexBacteria] = total
        else:
            self.tablaRepel[indexBacteria] = total
        results = None
        total = None

    def compute_cell_interaction_Repel(self, indexBacteria, d, w, atracTrue):
        with Pool() as pool:
            args = [(indexBacteria, otherBlosumScore, deepcopy(self.blosumScore), d, w) for otherBlosumScore in deepcopy(self.blosumScore)]
            results = pool.map(self.compute_diff_Repel, args)
            pool.close()  # Close the pool to prevent any more tasks from being submitted
            pool.join()   # Wait for the worker processes to exit
    
        total = sum(results)
    
        if atracTrue== TRUE:
            self.tablaAtract[indexBacteria] = total
        if atracTrue == FALSE:
            self.tablaRepel[indexBacteria] = total
        results = None
        total = None



  
    def creaTablaAtract(self, poblacion, d, w):                   #lineal
        for indexBacteria in range(len(poblacion)):
            self.compute_cell_interaction_Atract(indexBacteria,d, w, TRUE)
            # print("invocando indexBacteria numero: ", indexBacteria)
        # print("tablaAtract: ", self.tablaAtract)

    def creaTablaRepel(self, poblacion, d, w):                   #lineal
        for indexBacteria in range(len(poblacion)):
            self.compute_cell_interaction_Repel(indexBacteria,d, w, FALSE)
            # print("invocando indexBacteria numero: ", indexBacteria)
        # print("tablaAtract: ", self.tablaAtract)
    
    def creaTablasAtractRepel(self, poblacion, dAttr, wAttr, dRepel, wRepel):
        #invoca ambos metodos en paralelo
        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     executor.submit(self.creaTablaAtract, poblacion, dAttr, wAttr)
        #     executor.submit(self.creaTablaRepel, poblacion, dRepel, wRepel)
        
        self.creaTablaRepel(poblacion, dRepel, wRepel)
        self.creaTablaAtract(poblacion, dAttr, wAttr)
 


            #-----------------------------------------------------------
            
    def creaTablaInteraction(self):
        #llena la tabla con la suma de atract y repel
        for i in range(len(self.tablaAtract)):
            self.tablaInteraction[i] = self.tablaAtract[i] + self.tablaRepel[i]

    def creaTablaFitness(self):
        #llena la tabla con la suma de interaction y blosumScore
        for i in range(len(self.tablaInteraction)):
            valorBlsm = self.blosumScore[i]
            valorInteract = self.tablaInteraction[i]
            #suma ambos valores
            valorFitness =  valorBlsm + valorInteract
            
            self.tablaFitness[i] = valorFitness
    
    def getNFE(self):
        #return sum(self.NFE)
        return len(self.tablaFitness)
        
        
    def obtieneBest(self, parametros, globalNFE, outPath, start_time):
        bestIdx = 0
        for i in range(len(self.tablaFitness)):
            if self.tablaFitness[i] > self.tablaFitness[bestIdx]:
                bestIdx = i
        #obtiene el tiempo hasta ahora
        # elapsed_time = time.time() - start_time    
        # corridaNum, dAttr, wAttr, hRep, wRep, numSec, tumbo, nado, numRandomBacteria, numeroDeBacterias, iteraciones = parametros
        # print("corridaNum, "+ str(corridaNum)+ ", dAttr:,", dAttr, ",wAttr:,", wAttr, ",hRep:,", hRep, ",wRep:,", wRep, ",numSec:,", numSec, ",tumbo:,", tumbo, ",nado:,", nado, ",numRandomBacteria:,", numRandomBacteria, ",numeroDeBacterias:,", numeroDeBacterias, ",iteraciones:,", iteraciones, ",Best:,", bestIdx, ",Fitness:,", self.tablaFitness[bestIdx], ",BlosumScore,",  self.blosumScore[bestIdx], ",Interaction:,", self.tablaInteraction[bestIdx], ",atract: ,", self.tablaAtract[bestIdx], ",repel: ,",self.tablaRepel[bestIdx], ",NFE:,", globalNFE, ",tiempo:,", elapsed_time)


        #imprime lo mismo en outPath
        # f = open(outPath, "a")
        # f.write("corridaNum, "+ str(corridaNum)+ ", Best: ," + str(bestIdx) + " ,Fitness: ," + str(self.tablaFitness[bestIdx]) + " ,BlosumScore: ," + str(self.blosumScore[bestIdx]) + " ,Interaction: ," + str(self.tablaInteraction[bestIdx]) + " ,NFE: ," + str(globalNFE) + "\n")
        
        
        return bestIdx, self.tablaFitness[bestIdx]

    # def replaceWorst(self, poblacion, best):
    #     worst = 0
    #     for i in range(len(self.tablaFitness)):
    #         if self.tablaFitness[i] < self.tablaFitness[worst]:
    #             worst = i
    #     # print("Worst: ", worst,  "Blosum ",self.blosumScore[worst], "Fitness: ", self.tablaFitness[worst], "BlosumScore: ", self.blosumScore[worst], "Atract: ", self.tablaAtract[worst], "Repel: ", self.tablaRepel[worst], "Interaction: ", self.tablaInteraction[worst])
    #     #reemplaza la bacteria peor por una copia de la mejor
    #     poblacion[worst] = copy.deepcopy(poblacion[best])
        
    def replace3Worst(self, poblacion, numReplacer):
        # Ordena los índices según el fitness (de mayor a menor)
        fitness_indices = sorted(range(len(self.tablaFitness)), key=lambda i: self.tablaFitness[i], reverse=True)

        # Asegura que el número de reemplazos no exceda el tamaño de la población
        numReplacer = min(numReplacer, len(poblacion))

        mejores = fitness_indices[:numReplacer]
        peores = fitness_indices[-numReplacer:]

        for i in range(numReplacer):
            poblacion[peores[i]] = copy.deepcopy(poblacion[mejores[i]]) 
