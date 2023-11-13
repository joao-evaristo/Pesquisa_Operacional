import random
from ManipuladorArquivo import ManipuladorArquivo
import math


class SimulatedAnnealing:
    def __init__(
        self,
        n,
        I,
        m,
        J,
        p,
        distancias,
        temperatura_inicial=1000,
        numero_iteracoes=1000,
        numero_vizinhos=5,
    ):
        self.n = n  # numero de clientes
        self.I = I  # conjunto de clientes
        self.m = m  # numero de facilidades
        self.J = J  # conjunto das facilidades candidatas
        self.p = p  # numero de facilidades a serem abertas
        self.distancias = (
            distancias  # matriz de distancias entre a facilidade j e o cliente i
        )
        self.facilidades_abertas = []
        self.melhor_solucao = None
        self.custo_atual = 0
        self.custo_solucao = 0
        self.temperatura_inicial = temperatura_inicial
        self.temperatura = self.temperatura_inicial
        self.numero_iteracoes = numero_iteracoes
        self.numero_vizinhos = numero_vizinhos

    def gerar_solucao_inicial(self):
        # usar estrategia gulosa
        # pegar as facilidades, cujo a soma das distancias para os clientes seja a maior
        # e que ainda nao foram abertas
        facilidades_ordenadas = sorted(
            enumerate(self.distancias), key=lambda x: sum(x[1]), reverse=True
        )
        indices_p_primeiras = [item[0] for item in facilidades_ordenadas[:p]]
        # as facilidades abertas estarao da seguinte forma:
        # facilidades_abertas = [0, 1, 0, 0, 0, 1 ....] onde 1 significa que a facilidade esta aberta
        facilidades_abertas = [1 if i in indices_p_primeiras else 0 for i in range(m)]
        return facilidades_abertas

    def define_atendimento(self, facilidades_abertas):
        # definir o atendimento de cada cliente
        # cada cliente deve ser atendido pela facilidade mais proxima
        # cada cliente e atendido por apenas uma facilidade
        xij = [None] * n
        for i in range(n):
            menor_distancia = float("inf")
            for j in range(m):
                if facilidades_abertas[j] == 1:
                    distancia_i_j = self.distancias[j][i]
                    if distancia_i_j < menor_distancia:
                        menor_distancia = distancia_i_j
                        xij[i] = j
        return xij

    def funcao_objetivo(self, s):
        # para cada cliente, somar a distancia entre ele e a facilidade que o atende
        # a funcao objetivo e maximizar a soma das distancias da distancia minima entre cada facilidade e cada cliente
        xij = self.define_atendimento(s)
        custo = 0
        for i, j in enumerate(xij):
            custo -= self.distancias[j][i]
        return custo

    def vizinhanca(self):
        # gerar uma vizinhanca da solucao atual
        # trocar uma facilidade aberta por uma fechada
        # ou vice versa
        facilidades_abertas = self.facilidades_abertas.copy()
        n_alteracoes = random.randint(1, m)
        posicoes_alteradas = random.sample(range(m), n_alteracoes)
        for posicao_alterada in posicoes_alteradas:
            facilidades_abertas[posicao_alterada] = (
                1 if facilidades_abertas[posicao_alterada] == 0 else 0
            )
        return facilidades_abertas

    def aceita_melhora(self, custo_vizinho):
        # aceitar a solucao vizinha se ela for melhor
        # ou se ela for pior, mas a probabilidade de aceitar for maior que um numero aleatorio entre 0 e 1
        if custo_vizinho < self.custo_atual:
            print(f"Custo = {custo_vizinho}")
            return True
        else:
            # utiliza o criterio de metropolis
            delta = custo_vizinho - self.custo_atual
            return random.random() < math.exp(-delta / self.temperatura)

    def atualiza_temperatura(self, iteracao):
        # atualiza a temperatura
        # utiliza o fast simulated annealing
        self.temperatura = self.temperatura_inicial / (iteracao + 1)

    def executa(self):
        facilidades_abertas = self.gerar_solucao_inicial()
        self.facilidades_abertas = facilidades_abertas
        self.melhor_solucao = facilidades_abertas
        self.custo_atual = self.funcao_objetivo(facilidades_abertas)
        self.custo_solucao = self.custo_atual
        print(self.custo_atual)
        for i in range(self.numero_iteracoes):
            melhor_vizinho = None
            custo_melhor_vizinho = float("inf")
            for _ in range(self.numero_vizinhos):
                vizinho = self.vizinhanca()
                if self.funcao_objetivo(vizinho) < custo_melhor_vizinho:
                    melhor_vizinho = vizinho
                    custo_melhor_vizinho = self.funcao_objetivo(vizinho)
            if self.aceita_melhora(custo_melhor_vizinho):
                self.facilidades_abertas = melhor_vizinho
                self.custo_atual = custo_melhor_vizinho
                if custo_melhor_vizinho < self.funcao_objetivo(self.melhor_solucao):
                    self.melhor_solucao = melhor_vizinho
                    self.custo_solucao = custo_melhor_vizinho
            self.atualiza_temperatura(i)
        print("*" * 50)
        print(f"Melhor solucao: \n{self.melhor_solucao}")
        print(f"Custo da melhor solucao: {self.custo_solucao}")
        print("*" * 50)
