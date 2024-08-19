import numpy as np  # Manipulação de arrays
import re as regex  # Expressões regulares (split)
import random as rand
import time

#Caso não tenha a biblioteca numpy, executar o comando:
# pip install numpy

def main():
    tempoInicio = time.time()
    matrizTarefas, custos = leInstancias()
    for numMaquinas in range(6, 11):
        solucao = calculaSolucao(numMaquinas, matrizTarefas)
        foSolucao = fo(solucao, custos)
        
        # Aplica o método de refinamento First Improvement
        # solucao, foSolucao = refinamentoFirstImprovement(matrizTarefas, solucao, custos)
        
        ciclos = listaDeCiclos(solucao, custos)
        imprimeSolucao(numMaquinas, solucao, foSolucao, ciclos)

    tempoFim = time.time()
    print('Tempo de execução: ' + str(tempoFim - tempoInicio) + ' segundos')


def leInstancias():

    # Função que lê o arquivo de instâncias e retorna a matriz de tarefas e os custos

    path = "..\\files\\HAHN.IN2"
    with open(path, "r") as file:
        numeroTarefas = int(file.readline().strip())
        matrizTarefas = np.zeros((numeroTarefas, numeroTarefas), dtype=int)
        custos = []

        for i in range(0, numeroTarefas):
            custos.append(int(file.readline().strip().split()[0]))

        while True:
            linha = file.readline().strip()
            if not linha:
                break

            par = regex.split(r',|\n', linha)
            if len(par) < 2:
                break

            n1 = int(par[0])
            n2 = int(par[1])

            if n1 == -1 or n2 == -1:
                break

            matrizTarefas[n1-1][n2-1] = 1

    return matrizTarefas, custos

def divideTarefas(numMaquinas, numTarefas):
    numTatefasPorMaquina = np.zeros(numMaquinas, dtype=int)
    for i in range(0, numTarefas):
        numTatefasPorMaquina[i % numMaquinas] += 1
    np.random.shuffle(numTatefasPorMaquina)
    return numTatefasPorMaquina

def sequencia(numTarefas, matrizTarefas):
    sequencia = []
    matrizAuxiliar = np.copy(matrizTarefas)

    for i in range(0, numTarefas):
        candidatos = []
        for j in range(0, numTarefas):
            if np.sum(matrizAuxiliar[:,j]) == 0:
                candidatos.append(j)
        rand.shuffle(candidatos)
        escolhido = candidatos.pop(0)
        sequencia.append(escolhido)
        for i in range(0, numTarefas):
            if matrizAuxiliar[escolhido][i] == 1:
                matrizAuxiliar[escolhido][i] = 0
        matrizAuxiliar[:,escolhido] = -1
    return sequencia

def calculaSolucao(numMaquinas, matrizTarefas):
    #Calcula a solução inicial

    numTarefas = len(matrizTarefas)
    solucao = []

    numTarefasPorMaquina = divideTarefas(numMaquinas, numTarefas)
    sequenciaTarefas = sequencia(numTarefas, matrizTarefas)

    for maq in range(0, numMaquinas):
        tpm = []
        for t in range(0, int(numTarefasPorMaquina[maq])):
            tpm.append(sequenciaTarefas.pop(0))
        solucao.append(tpm)
    return solucao

def fo(solucao, custos):
    #Calcula qual das máquinas tem o maior somatório de custos

    maiorCiclo = 0
    for i in range(0, len(solucao)):
        ciclo = 0
        for j in range(0, len(solucao[i])):
            tarefa = solucao[i][j]
            custoIndividual = custos[tarefa]
            ciclo += custoIndividual
        if ciclo > maiorCiclo:
            maiorCiclo = ciclo
    return maiorCiclo

def listaDeCiclos(solucao, custos):

    #Criar uma lista com o somatório de custos de cada máquina
    numMaquinas = len(solucao)
    listaCiclos = []

    for i in range(0, numMaquinas):
        ciclo = 0
        for j in range(0, len(solucao[i])):
            tarefa = solucao[i][j]
            custoIndividual = custos[tarefa]
            ciclo += custoIndividual
        listaCiclos.append(ciclo)

    return listaCiclos

def refinamentoFirstImprovement(matrizTarefas, solucao, custos):
    # Número de máquinas
    numMaquinas = len(solucao)
    # Número de tarefas
    numTarefas = len(matrizTarefas)
    # Calcula a função objetivo inicial
    melhorFo = fo(solucao, custos)
    # Obtém a sequência de tarefas que deve ser respeitada
    sequenciaTarefas = sequencia(numTarefas, matrizTarefas)
    
    while True:
        melhorou = False
        # Itera sobre todas as máquinas
        for i in range(numMaquinas):
            # Itera sobre todas as máquinas seguintes para evitar repetição
            for j in range(i + 1, numMaquinas):
                # Itera sobre todas as tarefas da máquina i
                for t1 in range(len(solucao[i])):
                    # Itera sobre todas as tarefas da máquina j
                    for t2 in range(len(solucao[j])):
                        # Cria uma nova solução com a troca de tarefas entre as máquinas i e j
                        novaSolucao = [list(sol) for sol in solucao]
                        novaSolucao[i][t1], novaSolucao[j][t2] = novaSolucao[j][t2], novaSolucao[i][t1]
                        
                        # Verifica se a nova solução respeita a sequência de tarefas
                        novaSequencia = [tarefa for maquina in novaSolucao for tarefa in maquina]
                        if novaSequencia == sequenciaTarefas:
                            # Calcula a nova função objetivo
                            novaFo = fo(novaSolucao, custos)
                            
                            # Se a nova função objetivo for melhor, atualiza a solução e o melhor valor de FO
                            if novaFo < melhorFo:
                                solucao = novaSolucao
                                melhorFo = novaFo
                                melhorou = True
                                break
                    if melhorou:
                        break
                if melhorou:
                    break
            if melhorou:
                break
        # Se não houve melhoria, sai do loop
        if not melhorou:
            break

    return solucao, melhorFo


def imprimeSolucao(numMaquinas, melhorSolucao, melhorFo, listaCiclos):
    #Imprime a solução
    print('Número de máquinas: ' + str(numMaquinas))
    for i in range(0, numMaquinas):
        print('Máquina - ' + str(i+1) + ': ' + str(melhorSolucao[i]) + ' - Custo: ' + str(listaCiclos[i]))
    print('FO: ' + str(melhorFo))
    print('-------------------------------------------------------')

if __name__ == "__main__":
    main()
