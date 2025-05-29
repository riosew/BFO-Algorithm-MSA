from copy import copy
from multiprocessing import Manager, Pool
import time
from bacteria import bacteria
import numpy
import copy

from fastaReader import fastaReader

if __name__ == "__main__":
#crea un ciclo para repetir la corrida entera
    for corridaNum in range(1, 31):
        #print("corrida ", corridaNum)
    



        numeroDeBacterias = 6
        numRandomBacteria = 0
        iteraciones = 12
        tumbo = 12                                            #numero de gaps a insertar 
        nado = 0
        secuencias = list()
        #path de salida csv
        outPath = "C:\\secuenciasBFOA\\out.csv"
  
    
        secuencias = fastaReader().seqs
        names = fastaReader().names
    
    
        #hace todas las secuencias listas de caracteres
        for i in range(len(secuencias)):
            #elimina saltos de linea
            secuencias[i] = list(secuencias[i])
        

        globalNFE = 0                            #numero de evaluaciones de la funcion objetivo

        dAttr= 0.1 #0.1
        wAttr= 0.002 #0.2
        hRep=dAttr
        wRep= 0.002    #10 default   phase 1: 0.001 phase 2: 0.002
    
   
        manager = Manager()
        numSec = len(secuencias)
        # print("numSec: ", numSec)
    
        poblacion = manager.list(range(numeroDeBacterias))
        names = manager.list(names)
        NFE = manager.list(range(numeroDeBacterias))
        parametros =  corridaNum, dAttr, wAttr, hRep, wRep, numSec, tumbo, nado, numRandomBacteria, numeroDeBacterias, iteraciones
    
        # print(secuencias)



        def poblacionInicial():    #lineal
            #crece la poblacion al numero de bacterias
            for i in range(numeroDeBacterias):
                bacterium = []
                for j in range(numSec):
                    bacterium.append(secuencias[j])
                poblacion[i] = list(bacterium)
           
   
        def printPoblacion():
            for i in range(numeroDeBacterias):
                print(poblacion[i])
            
    

        #---------------------------------------------------------------------------------------------------------
        operadorBacterial = bacteria(numeroDeBacterias)    
        veryBest = [None, None, None] #indice, fitness, secuencias
    
        #registra el tiempo de inicio
        start_time = time.time()
    
        # print("poblacion inicial ...")
        poblacionInicial() 
        # print("poblacion inicial creada - Tumbo ...")
    

        for it in range(iteraciones):
        
            operadorBacterial.tumbo(numSec, poblacion, tumbo)
            # print("Tumbo Realizado - Cuadrando ...")
            operadorBacterial.nado(numSec, poblacion, nado)
            #nado hecho
            operadorBacterial.cuadra(numSec, poblacion)
            # print("poblacion inicial cuadrada - Creando granLista de Pares...")
            operadorBacterial.creaGranListaPares(poblacion)
            # print("granList: creada - Evaluando Blosum Parallel")
            operadorBacterial.evaluaBlosum()  #paralelo
            # print("blosum evaluado - creando Tablas Atract Parallel...")

            operadorBacterial.creaTablasAtractRepel(poblacion, dAttr, wAttr,hRep, wRep)


            operadorBacterial.creaTablaInteraction()
            # print("tabla Interaction creada - creando tabla Fitness")
            operadorBacterial.creaTablaFitness()
            # print("tabla Fitness creada ")
            globalNFE += operadorBacterial.getNFE()
            bestIdx, bestFitness = operadorBacterial.obtieneBest(parametros, globalNFE, outPath, start_time)
        
            if (veryBest[0] == None) or (bestFitness > veryBest[1]): #Remplaza el mejor 
                veryBest[0] = bestIdx
                veryBest[1] = bestFitness
                veryBest[2] = copy.deepcopy(poblacion[bestIdx])
            operadorBacterial.replaceWorst(poblacion, veryBest[0])
            operadorBacterial.resetListas(numeroDeBacterias)

    # print("Very Best: ", veryBest)
    #imprime el tiempo de ejecucion
    # print("--- %s seconds ---" % (time.time() - start_time))
    #imprime el tiempo de ejecucion en outPath
    # f = open(outPath, "a")
    # f.write(",,,,,,,,,,time ," + str(time.time() - start_time))



