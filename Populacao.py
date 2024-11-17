# populacao.py
import random
from Individuo import Individuo

class Populacao:
    def __init__(self, tamanho, geracao_atual, taxa_mutacao):
        self.tamanho = tamanho
        self.geracao_atual = geracao_atual
        self.taxa_mutacao = taxa_mutacao
        self.individuos = []
        self.proximo_id = 0

    def inicializar(self):
        """Cria uma população inicial de indivíduos aleatórios."""
        self.individuos = [self._gerar_individuo() for _ in range(self.tamanho)]

    def _gerar_individuo(self):
        """Gera um indivíduo aleatório."""
        individuo = Individuo(self.proximo_id, self.geracao_atual)
        self.proximo_id += 1
        return individuo

    def selecionar_pais(self):
        """Seleciona dois indivíduos da população proporcionalmente ao fitness."""
        fitness_total = sum(ind.fitness for ind in self.individuos)
        probabilidades = [ind.fitness / fitness_total for ind in self.individuos]
        return random.choices(self.individuos, weights=probabilidades, k=2)

    def crossover(self, pai1, pai2):
        """Realiza o crossover entre dois indivíduos, gerando dois filhos."""
        ponto_corte = random.randint(1, len(pai1.genes) - 1)
        filho1_genes = pai1.genes[:ponto_corte] + pai2.genes[ponto_corte:]
        filho2_genes = pai2.genes[:ponto_corte] + pai1.genes[ponto_corte:]
        filho1 = Individuo(self.proximo_id, self.geracao_atual + 1, filho1_genes)
        self.proximo_id += 1
        filho2 = Individuo(self.proximo_id, self.geracao_atual + 1, filho2_genes)
        self.proximo_id += 1
        return filho1, filho2

    def mutacao(self, individuo):
        """Aplica mutação ao indivíduo com base na taxa de mutação."""
        if random.random() < self.taxa_mutacao:
            indice = random.randint(0, len(individuo.genes) - 1)
            individuo.genes[indice] = random.randint(1, 8)
            individuo.calcular_fitness()

    def nova_geracao(self):
        """Cria a próxima geração usando seleção, crossover e mutação."""
        nova_populacao = sorted(self.individuos, key=lambda ind: ind.fitness, reverse=True)[:self.tamanho]

        while len(nova_populacao) < self.tamanho:
            pai1, pai2 = self.selecionar_pais()
            filho1, filho2 = self.crossover(pai1, pai2)
            self.mutacao(filho1)
            self.mutacao(filho2)
            nova_populacao.extend([filho1, filho2])

        self.individuos = nova_populacao
        self.geracao_atual += 1