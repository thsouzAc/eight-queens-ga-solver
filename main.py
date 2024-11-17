from AlgoritmoGenetico import AlgoritmoGenetico

def main():
    # Configurações do Algoritmo Genético
    tamanho_populacao = 100
    max_geracoes = 1000
    taxa_mutacao = 0.05

    algoritmo = AlgoritmoGenetico(tamanho_populacao, max_geracoes, taxa_mutacao)
    melhor_solucao = algoritmo.executar()

    print(f"Melhor solução encontrada (Geração {melhor_solucao.geracao}, ID {melhor_solucao.id}):")
    print(f"Genes: {melhor_solucao.genes}")
    print(f"Fitness: {melhor_solucao.fitness}")

# Executar a função main
if __name__ == "__main__":
    main()