import os   #Manipulação de arquivo
import numpy as np  #Manipulação de arrays
import re as regex  #Expressões regulares (split)

def main():
    readFile()
        
def readFile():
    path = "..\\files\\instances.txt"
    with open(path, "r") as file:
        #Lê o tamanho da matriz quandrada que será montada para representar o grafo
        numeroTarefas = int(file.readline())

        #Cria a matriz quadrada de tamanho tasksNum
        matrizTarefas = np.zeros((numeroTarefas,numeroTarefas), dtype=int)

        #Cria a lista de precedência
        precedencia = []

        #Lê o "grafo" do arquivo e transforma em uma matriz
        for i in range(0, numeroTarefas):
            matrizTarefas[i, numeroTarefas] = int(file.readline().split()[0])
        
        #Relações de precedência
        n1,n2 = 0
        while n1 != -1 and n2!= -1:
            par = regex.split(r',|\n', file.readline())

            if(n1 != -1 and n2 != -1):
                n1 = int(par[0])
                n2 = int(par[1])
                precedencia.append((n1,n2))
                
    return matrizTarefas, precedencia

if __name__ == "__main__":
    main()
