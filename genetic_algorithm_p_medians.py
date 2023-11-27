import random
import math
from ManipuladorArquivo import ManipuladorArquivo


def decisao(probabilidade):
    return random.random() < probabilidade


class GeneticAlgorithm:
    def __init__(
        self,
        n,
        I,
        m,
        J,
        p,
        distancias,
        n_populacao_inicial=10,
        taxa_elitismo=0.15,
        tamanho_populacao=20,
        taxa_cruzamento=0.4,
        taxa_mutacao=0.1,
        n_geracoes=300,
    ):
        self.n = n  # numero de clientes
        self.I = I  # conjunto de clientes
        self.m = m  # numero de facilidades
        self.J = J  # conjunto das facilidades candidatas
        self.p = p  # numero de facilidades a serem abertas
        self.distancias = (
            distancias  # matriz de distancias entre a facilidade j e o cliente i
        )
        self.facilidades = []
        self.melhor_solucao = None
        self.custo_atual = 0
        self.custo_solucao = 0
        self.n_populacao_inicial = n_populacao_inicial
        self.taxa_elitismo = taxa_elitismo
        self.tamanho_populacao = tamanho_populacao
        self.taxa_cruzamento = taxa_cruzamento
        self.taxa_mutacao = taxa_mutacao
        self.n_geracoes = n_geracoes
        self.populacao = self.gerar_populacao_inicial()

    def gerar_populacao_inicial(self):
        # gerar uma populacao inicial aleatoria
        populacao = []
        for i in range(self.n_populacao_inicial):
            populacao.append(random.sample(range(self.m), self.m)[: self.p])
        return populacao

    def define_atendimento(self, facilidades):
        # definir o atendimento de cada cliente
        # cada cliente deve ser atendido pela facilidade mais proxima
        # cada cliente e atendido por apenas uma facilidade
        xij = [None] * self.n
        facilidades_abertas = facilidades[: self.p]
        for i in range(self.n):
            menor_distancia = float("inf")
            for j in facilidades_abertas:
                if self.distancias[j][i] < menor_distancia:
                    menor_distancia = self.distancias[j][i]
                    xij[i] = j
        return xij

    def fitness(self, s):
        # para cada cliente, somar a distancia entre ele e a facilidade que o atende
        # a funcao objetivo e maximizar a soma das distancias da distancia minima entre cada facilidade e cada cliente
        xij = self.define_atendimento(s)
        custo = 0
        for i, j in enumerate(xij):
            custo += self.distancias[j][i]
        return custo

    def classificar_individuos(self):
        self.populacao.sort(key=self.fitness, reverse=True)

    def selecionar_individuos(self):
        tamanho_elite = int(len(self.populacao) * self.taxa_elitismo)
        populacao_restante = self.populacao[tamanho_elite:]
        populacao_selecionada = self.populacao[:tamanho_elite]
        taxa_de_selecao = 0.6
        while len(populacao_selecionada) < self.tamanho_populacao:
            for individuo in populacao_restante:
                if decisao(taxa_de_selecao):
                    populacao_selecionada.append(individuo)
                    taxa_de_selecao = taxa_de_selecao * 0.80
        self.populacao = populacao_selecionada

    def cruzar_individuos(self):
        pass

    def fazer_mutacao(self):
        pass

    def executar(self):
        pass


if __name__ == "__main__":
    ma = ManipuladorArquivo("pmed40.txt.table.p56.B")
    distancias = ma.obter_distancias_facilidades()
    n = ma.obter_n_clients()
    I = ma.obter_clientes()
    m = ma.obter_m_facilities()
    J = ma.obter_facilidades()
    p = ma.obter_p_desired_facilities()
    ga = GeneticAlgorithm(n, I, m, J, p, distancias)
    ga.classificar_individuos()
    print(ga.populacao)
