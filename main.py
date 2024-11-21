import random

# acompanhar o número de execuções do algoritmo

def get_execution_count():
    try:
        with open("execution_count.txt", "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

# incrementa e salva o número de execuções

def increment_execution_count():
    count = get_execution_count() + 1
    with open("execution_count.txt", "w") as f:
        f.write(str(count))
    return count

# salva informações do melhor indivíduo em um arquivo

def salvar_melhor_individuo(individuo, execucao):
    with open("melhor_individuo.txt", "a") as f:  # modo "a" para anexar ao arquivo
        f.write(f"Execução: {execucao}\n")
        f.write(f"ID: {individuo.id}, Geração: {individuo.geracao}, Genes: {individuo.genes}, Fitness: {individuo.fitness}\n")
        f.write("-" * 40 + "\n")

# se o genes não for fornecido, é gerado aleatoriamente.

class Individuo:
    def __init__(self, id, geracao, genes=None):
        self.id = id
        self.geracao = geracao
        self.genes = genes if genes else [random.randint(1, 8) for _ in range(8)]
        self.fitness = self.calcular_fitness()

    def calcular_fitness(self):

        """
        calcula o fitness do indivíduo, onde o número de pares de rainhas que não estão se atacando,
        ou seja o máximo possível é 28 onde é a combinações de 8 rainha, C(8, 2)).
        """

        nao_atacando = 28
        for i in range(len(self.genes)):
            for j in range(i + 1, len(self.genes)):

                # verifica se as rainhas estão se atacando
                
                if self.genes[i] == self.genes[j] or abs(self.genes[i] - self.genes[j]) == abs(i - j):
                    nao_atacando -= 1
        return nao_atacando

# retorna a representação em string do indivíduo para ser exibido.

    def __repr__(self):
        return f"Individuo(id={self.id}, geracao={self.geracao}, genes={self.genes}, fitness={self.fitness})"

# seleciona um indivíduo da população com probabilidade proporcional ao valor fitness.
def selecao_por_roleta(populacao):

    total_fitness = sum(ind.fitness for ind in populacao)
    pick = random.uniform(0, total_fitness)
    atual = 0
    for ind in populacao:
        atual += ind.fitness
        if atual >= pick:
            return ind


def crossover(pai1, pai2, id_filho, geracao):

    ponto_de_corte = random.randint(1, 7)
    genes_filho1 = pai1.genes[:ponto_de_corte] + pai2.genes[ponto_de_corte:]
    genes_filho2 = pai2.genes[:ponto_de_corte] + pai1.genes[ponto_de_corte:]
    return Individuo(id=id_filho, geracao=geracao, genes=genes_filho1), \
           Individuo(id=id_filho + 1, geracao=geracao, genes=genes_filho2)


def mutacao(individuo, taxa_mutacao):

    if random.random() < taxa_mutacao:
        posicao = random.randint(0, 7)
        novo_valor = random.randint(1, 8)
        individuo.genes[posicao] = novo_valor
        individuo.fitness = individuo.calcular_fitness()


def algoritmo_genetico(tampop, itmax, txmut):
  
    execucao = increment_execution_count()
    populacao = [Individuo(id=i, geracao=0) for i in range(tampop)]
    id_atual = tampop

    for iteracao in range(itmax):

        # população é ordenada de forma decrescente
        populacao = sorted(populacao, key=lambda x: x.fitness, reverse=True)


        melhor_individuo = populacao[0]

        # quando se encontra uma solução otima

        if melhor_individuo.fitness == 28:
            print(f"\nSolução ótima encontrada na execução {execucao}, geração {iteracao}!")
            salvar_melhor_individuo(melhor_individuo, execucao)  # salva em arquivo txt
            return populacao

        nova_populacao = []

        # seleciona os melhores 

        nova_populacao.extend(populacao[:tampop])

        while len(nova_populacao) < 2 * tampop:
            pai1 = selecao_por_roleta(populacao)
            pai2 = selecao_por_roleta(populacao)
            filho1, filho2 = crossover(pai1, pai2, id_atual, iteracao + 1)
            id_atual += 2
            mutacao(filho1, txmut)
            mutacao(filho2, txmut)
            nova_populacao.extend([filho1, filho2])

        # substituição da população pela proxima geração
        populacao = sorted(nova_populacao, key=lambda x: x.fitness, reverse=True)[:tampop]

    print(f"\nNúmero máximo de iterações atingido na execução {execucao}. Melhor solução:")
    salvar_melhor_individuo(populacao[0], execucao)  # aqui, salvamos o individuo mesmo sem uma solução otima, onde fitness < 28
    return populacao


# parâmetros do algoritmo

tampop = 200  
itmax = 100  
txmut = 0.2  

populacao_final = algoritmo_genetico(tampop, itmax, txmut)

melhor_individuo = populacao_final[0]
print("\nMelhor solução encontrada:")
print(melhor_individuo)
