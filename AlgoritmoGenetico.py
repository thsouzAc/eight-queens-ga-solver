from Populacao import Populacao

class AlgoritmoGenetico:
    def __init__(self, tamanho_populacao, max_geracoes, taxa_mutacao):
        self.tamanho_populacao = tamanho_populacao
        self.max_geracoes = max_geracoes
        self.taxa_mutacao = taxa_mutacao

    def executar(self):
        populacao = Populacao(self.tamanho_populacao, 0, self.taxa_mutacao)
        populacao.inicializar()

        for _ in range(self.max_geracoes):
            populacao.nova_geracao()

        melhor_individuo = max(populacao.individuos, key=lambda ind: ind.fitness)
        return melhor_individuo