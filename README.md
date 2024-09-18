**Otimização de Entregas com Inteligência Artificial**

Este projeto foi desenvolvido como parte da disciplina de Inteligência Artificial da Universidade do Minho. O objetivo é otimizar o processo de entrega de encomendas usando diferentes algoritmos de busca.

**Descrição do Projeto**

O projeto simula o processo de entrega de encomendas para a empresa "Health Planet". Ele utiliza um grafo para representar a cidade, onde os pontos são locais de entrega e as arestas são os caminhos entre eles. O objetivo é encontrar a rota mais eficiente para os estafetas (entregadores) fazerem as entregas.

**Algoritmos Implementados**

    1. DFS (Depth-First Search): Explora todos os caminhos até o final antes de voltar. Pode ser ineficiente e não garante a rota mais curta.
    2. BFS (Breadth-First Search): Explora todos os caminhos nível por nível, garantindo encontrar a rota mais curta, mas pode consumir muita memória.
    3. Gulosa (Greedy): Escolhe sempre o próximo passo com base na menor distância, mas não garante a melhor solução.
    4. A* (A-Star): Combina a distância percorrida e a distância restante para encontrar a rota mais eficiente. Geralmente é o mais eficaz.

**Funcionamento**

Ao iniciar o programa, é apresentado um menu com as seguintes opções:
    -Visualizar o grafo da cidade.
    -Aplicar diferentes algoritmos de busca para encontrar a rota de entrega.
    -Comparar a eficiência dos algoritmos.

**Regras de Entrega**
    -Estafetas de bicicleta têm prioridade para entregas locais e pequenas.
    -Motos são usadas para entregas restantes que não podem ser feitas de bicicleta.
    -Carros são usados para encomendas grandes ou restantes.

**Conclusões**
O projeto foi uma boa oportunidade para aplicar algoritmos de busca a um problema real. O algoritmo A* provou ser o mais eficiente para otimizar as entregas.