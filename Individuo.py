import random

class Individuo:
    def __init__(self, id, geracao, genes=None):
        self.id = id
        self.geracao = geracao
        self.genes = genes if genes else [random.randint(1, 8) for _ in range(8)]
        self.fitness = 0
        self.calcular_fitness()

    def calcular_fitness(self):
        nao_atacando = 0
        n = len(self.genes)

        for i in range(n):
            for j in range(i + 1, n):
                if (
                    self.genes[i] != self.genes[j]  # Não estão na mesma linha
                    and abs(self.genes[i] - self.genes[j]) != abs(i - j)  # Não estão na mesma diagonal
                ):
                    nao_atacando += 1

        self.fitness = nao_atacando