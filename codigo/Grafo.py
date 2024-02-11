import math
from copy import deepcopy
from queue import Queue
from Encomenda import Encomenda
from Estafeta import Estafeta
import networkx as nx  # biblioteca de tratamento de grafos necessária para desnhar graficamente o grafo
import matplotlib.pyplot as plt  # idem
from Nodo import Nodo

class Grafo:

    def __init__(self, directed=False):
        self.m_nodes = []
        self.m_directed = directed
        self.m_graph = {}  # dicionario para armazenar os nodos e arestas
        self.m_h = {}  # dicionario para armazenar as heuristicas para cada nodo -< pesquisa informada
        self.m_h2 = {}
        self.dicBFS = {} # dicionarios para guardar caminhos e custos entre nodes usando uma procura
        self.dicDFS = {}
        self.dicAstar = {}
        self.dicGreedy = {}
    #############
    #    escrever o grafo como string
    #############
    def __str__(self):
        out = ""
        for key in self.m_graph.keys():
            out = out + "node" + str(key) + ": " + str(self.m_graph[key]) + "\n"
        return out

    ################################
    #   encontrar nodo pelo nome
    ################################

    def get_node_by_name(self, name):
        search_node = Nodo(name)
        for node in self.m_nodes:
            if node == search_node:
                return node
        return None

    ##############################3
    #   imprimir arestas
    ############################333333

    def imprime_aresta(self):
        listaA = ""
        lista = self.m_graph.keys()
        for nodo in lista:
            for (nodo2, custo) in self.m_graph[nodo]:
                listaA = listaA + nodo + " ->" + nodo2 + " custo:" + str(custo) + "\n"
        return listaA

    ################
    #   adicionar   aresta no grafo
    ######################

    def add_edge(self, node1, node2, weight):
        n1 = Nodo(node1)
        n2 = Nodo(node2)
        if (n1 not in self.m_nodes):
            n1_id = len(self.m_nodes)  # numeração sequencial
            n1.setId(n1_id)
            self.m_nodes.append(n1)
            self.m_graph[node1] = []

        if (n2 not in self.m_nodes):
            n2_id = len(self.m_nodes)  # numeração sequencial
            n2.setId(n2_id)
            self.m_nodes.append(n2)
            self.m_graph[node2] = []

        self.m_graph[node1].append((node2, weight))  # poderia ser n1 para trabalhar com nodos no grafo

        if not self.m_directed:
            self.m_graph[node2].append((node1, weight))

    #############################
    # devolver nodos
    ##########################

    def getNodes(self):
        return self.m_nodes

    #######################
    #    devolver o custo de uma aresta
    ##############3

    def get_arc_cost(self, node1, node2):
        custoT = math.inf
        a = self.m_graph[node1]  # lista de arestas para aquele nodo
        for (nodo, custo) in a:
            if nodo == node2:
                custoT = custo

        return custoT

    ##############################
    #  dado um caminho calcula o seu custo
    ###############################

    def calcula_custo(self, caminho):
        # caminho é uma lista de nodos
        teste = caminho
        custo = 0
        i = 0
        while i + 1 < len(teste):
            custo = custo + self.get_arc_cost(teste[i], teste[i + 1])
            i = i + 1
        return custo

    ################################################################################
    #     procura DFS
    ####################################################################################

    def procura_DFS(self, start, end, path=[], visited=set()):
        path.append(start)
        visited.add(start)

        if start == end:
            # calcular o custo do caminho funçao calcula custo.
            custoT = self.calcula_custo(path)
            return (visited, path, custoT)
        for (adjacente, peso) in self.m_graph[start]:
            if adjacente not in visited:
                resultado = self.procura_DFS(adjacente, end, path, visited)
                if resultado is not None:
                    return resultado
        path.pop()  # se nao encontra remover o que está no caminho......
        return None

    def entregar_entregas_DFS3(self, startNode, estafeta, paths, custoTotal, path_total):
        # inicia um set para guardar as localizações onde devemos passar (ruas das encomendas)
        nodesToFind = set()
        # itera as encomendas de um estafeta e preenche os nodesToFind
        for enc in estafeta.encomendas:
            nodesToFind.add(enc.rua_destino)
        # se o startNode se encontrar na lista de nodesToFind ele retira-o uma vez que ja lá está
        if startNode in nodesToFind:
            nodesToFind.remove(startNode)
        # se não existirem nodesToFind quer dizer que todas as encomendas já foram entregues
        if not nodesToFind:
            for e in estafeta.encomendas:
                if e.rua_destino == startNode:
                    # encomenda esta no sitio de entrega
                    print(f"Encomenda Chegou ao Destino: {e.rua_destino}")
                    # calcular tempo de entrega da encomenda
                    distancia = custoTotal
                    prazo = e.prazo_entrega
                    velocidade = estafeta.transporte_velocidade
                    tempo_entrega = distancia/velocidade
                    # ve se a encomenda está atrasada e atribui a respetiva avaliação conforme o tempo de entrega
                    if prazo > tempo_entrega:
                        print("Entrega Chegou a Tempo!")
                        # se a encomenda chegar antes de metade do prazo de entrega atribui nota 5
                        if prazo > tempo_entrega/2:
                            avaliacao = 5
                        # se chegar a tempo mas não em metade do prazo atribui 3
                        else:
                            avaliacao = 3
                    if prazo < tempo_entrega:
                        print("Entrega Não Chegou a Tempo!")
                        # se chegar fora do prazo de entrega atribui nota 1
                        avaliacao = 1
                    # atualiza a avaliação do estafeta
                    estafeta.avaliacao_total += avaliacao
                    estafeta.nr_avaliacoes += 1
                    # escreve em ficheiro a entrega da encomenda
                    with open('Entregas.txt','a') as arquivo:
                        arquivo.write(f"Rua Destino: {e.rua_destino}; Peso: {e.peso}kg; Volume: {e.volume}cm2; Preco: {e.preco}; Avaliacao: {avaliacao}; Meio de Transporte: {estafeta.transporte}; Prazo de Entrega: {prazo} minutos; Tempo de entrega: {tempo_entrega} minutos; Id do Estafeta : {estafeta.id}; Classificacao do Estafeta: {estafeta.avaliacao_total/estafeta.nr_avaliacoes}.\n")
                    # remove a encomenda da lista de encomendas do estafeta
                    estafeta.encomendas.remove(e)
                    # atualiza a velocidade do transporte
                    estafeta.transporte_peso_atual -= e.peso
                    if estafeta.transporte == "carro":
                        estafeta.transporte_velocidade = ((50 - (0.1 * estafeta.transporte_peso_atual)) * 1000) / 60
                    if estafeta.transporte == "mota":
                        estafeta.transporte_velocidade = ((35 - (0.5 * estafeta.transporte_peso_atual)) * 1000) / 60
                    if estafeta.transporte == "bicicleta":
                        estafeta.transporte_velocidade = ((10 - (0.6 * estafeta.transporte_peso_atual)) * 1000) / 60
            # dá print à path do caminho mais rápido
            print(f"PATH: {paths}")
            # dá print ao custo total do caminho mais rápido
            print(f"CUSTO TOTAL: {custoTotal}")
            # cria uma variavel que vai conter todos os nós visitados
            # isto foi feito visto que path_total era uma lista de sets e listas e nós queriamos apenas uma lista como return
            lista_resultante = []
            # itera sobre os elementos da lista original
            for elemento in path_total:
                # se o elemento for um conjunto, adiciona os seus elementos à lista resultante
                if isinstance(elemento, set):
                    lista_resultante.extend(list(elemento))
                # se o elemento for uma lista, adiciona os seus elementos à lista resultante
                elif isinstance(elemento, list):
                    lista_resultante.extend(elemento)
            # dá print a todos os nós visitados durante a execução do programa
            print(f"NODOS VISITADOS: {lista_resultante}")
        else:
            # cria variavel para guardar nodos visitados
            visited = []
            # itera todos os nodes em nodesToFind
            for node in nodesToFind:
                # e se não existir informação sobre o custo e a path para chegar entre o startNode e o nodeToFind usando o algoritmo em questão ele faz essa pesquisa e guarda a informação correspondente
                if (startNode, node) not in self.dicDFS:
                    v, pt, custo = self.procura_DFS(startNode, node, [], set())
                    self.dicDFS[(startNode, node)] = (pt, custo)
                    visited.append(v)
                # se já houver essa informação guarda a variavel visited como lista vazia uma vez que nao foi preciso visitar nenhum node
                else:
                    visited = []
            # cria variaveis
            menorCusto = float('inf')
            melhorPath = []
            nextNode = None
            # itera o dicionario e ve qual o nodeToFind e o path para lá chegar que representam menor custo, esse será o node que será visitado a seguir
            for chave, valor in self.dicDFS.items():
                sn, fn = chave
                pa, c = valor
                if sn == startNode and fn in nodesToFind and c < menorCusto:
                    nextNode = fn
                    melhorPath = pa
                    menorCusto = c
            paths.append(melhorPath)
            path_total.append(visited)
            custoTotal += menorCusto
            # itera a lista de encomendas de um estafeta
            for e in estafeta.encomendas:
                # se a rua da encomenda for o node onde estamos atualmente
                if e.rua_destino == startNode:
                    # dá print que a encomenda esta no sitio de entrega
                    print(f"Encomenda Chegou ao Destino: {e.rua_destino}")
                    # calcular tempo de entrega da encomenda e atribui a classificação ao estafeta associada
                    distancia = custoTotal
                    prazo = e.prazo_entrega
                    velocidade = estafeta.transporte_velocidade
                    tempo_entrega = distancia/velocidade
                    # ver se a encomenda esta atrasada
                    if prazo > tempo_entrega:
                        print("Entrega chegou a tempo!")
                        # se a encomenda chegar antes de metade do prazo de entrega atribui nota 5
                        if prazo > tempo_entrega/2:
                            avaliacao = 5
                        # se chegar a tempo mas não em metade do prazo atribui 3
                        else:
                            avaliacao = 3
                    if prazo < tempo_entrega:
                        print("Entrega não chegou a tempo!")
                        # se chegar fora do prazo de entrega atribui nota 1
                        avaliacao = 1
                    # atualiza a avaliação do estafeta
                    estafeta.avaliacao_total += avaliacao
                    estafeta.nr_avaliacoes += 1
                    # escreve em ficheiro a entrega da encomenda
                    with open('Entregas.txt','a') as arquivo:
                        arquivo.write(f"Rua Destino: {e.rua_destino}; Peso: {e.peso}kg; Volume: {e.volume}cm2; Preco: {e.preco}; Avaliacao: {avaliacao}; Meio de Transporte: {estafeta.transporte}; Prazo de Entrega: {prazo} minutos; Tempo de entrega: {tempo_entrega} minutos; Id do Estafeta : {estafeta.id}; Classificacao do Estafeta: {estafeta.avaliacao_total/estafeta.nr_avaliacoes}.\n")
                    # remove a encomenda da lista de encomendas do estafeta uma vez que já foi entregue
                    estafeta.encomendas.remove(e)
                    # atualiza a  velocidade do transporte uma vez que há menos peso
                    estafeta.transporte_peso_atual -= e.peso
                    if estafeta.transporte == "carro":
                        estafeta.transporte_velocidade = ((50 - (0.1 * estafeta.transporte_peso_atual)) * 1000) / 60
                    if estafeta.transporte == "mota":
                        estafeta.transporte_velocidade = ((35 - (0.5 * estafeta.transporte_peso_atual)) * 1000) / 60
                    if estafeta.transporte == "bicicleta":
                        estafeta.transporte_velocidade = ((10 - (0.6 * estafeta.transporte_peso_atual)) * 1000) / 60
            # chama outra vez o método uma vez que ainda há encomendas a serem entregues, desta vez com o next node, que é o node com menor custo para ser encontrado
            self.entregar_entregas_DFS3(nextNode, estafeta, paths, custoTotal, path_total)
        # dá return a dizer que todas as entregas daquele estafeta foram bem sucedidas
        return "Entregas Bem Sucedidas!\n\n"

    #####################################################
    # Procura BFS
    ######################################################

    def procura_BFS(self, start, end):
        # definir nodos visitados para evitar ciclos
        visited = set()
        fila = Queue()
        custo = 0
        # adicionar o nodo inicial à fila e aos visitados
        fila.put(start)
        visited.add(start)

        # garantir que o start node nao tem pais...
        parent = dict()
        parent[start] = None

        path_found = False
        while not fila.empty() and path_found == False:
            nodo_atual = fila.get()
            if nodo_atual == end:
                path_found = True
            else:
                for (adjacente, peso) in self.m_graph[nodo_atual]:
                    if adjacente not in visited:
                        fila.put(adjacente)
                        parent[adjacente] = nodo_atual
                        visited.add(adjacente)

        # reconstruir o caminho

        path = []
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
            # funçao calcula custo caminho
            custo = self.calcula_custo(path)
        return (visited,path, custo)


    def entregar_entregas_BFS3(self, startNode, estafeta, paths, custoTotal, path_total):
        # inicia um set para guardar as localizações onde devemos passar (ruas das encomendas)
        nodesToFind = set()
        # itera as encomendas de um estafeta e preenche os nodesToFind
        for enc in estafeta.encomendas:
            nodesToFind.add(enc.rua_destino)
        # se o startNode se encontrar na lista de nodesToFind ele retira-o uma vez que ja lá está
        if startNode in nodesToFind:
            nodesToFind.remove(startNode)
        # se não existirem nodesToFind quer dizer que todas as encomendas já foram entregues
        if not nodesToFind:
            for e in estafeta.encomendas:
                if e.rua_destino == startNode:
                    # encomenda esta no sitio de entrega
                    print(f"Encomenda Chegou ao Destino: {e.rua_destino}")
                    # calcular tempo de entrega da encomenda
                    distancia = custoTotal
                    prazo = e.prazo_entrega
                    velocidade = estafeta.transporte_velocidade
                    tempo_entrega = distancia/velocidade
                    # ve se a encomenda está atrasada e atribui a respetiva avaliação conforme o tempo de entrega
                    if prazo > tempo_entrega:
                        print("Entrega Chegou a Tempo!")
                        # se a encomenda chegar antes de metade do prazo de entrega atribui nota 5
                        if prazo > tempo_entrega/2:
                            avaliacao = 5
                        # se chegar a tempo mas não em metade do prazo atribui 3
                        else:
                            avaliacao = 3
                    if prazo < tempo_entrega:
                        print("Entrega Não Chegou a Tempo!")
                        # se chegar fora do prazo de entrega atribui nota 1
                        avaliacao = 1
                    # atualiza a avaliação do estafeta
                    estafeta.avaliacao_total += avaliacao
                    estafeta.nr_avaliacoes += 1
                    # escreve em ficheiro a entrega da encomenda
                    with open('Entregas.txt','a') as arquivo:
                        arquivo.write(f"Rua Destino: {e.rua_destino}; Peso: {e.peso}kg; Volume: {e.volume}cm2; Preco: {e.preco}; Avaliacao: {avaliacao}; Meio de Transporte: {estafeta.transporte}; Prazo de Entrega: {prazo} minutos; Tempo de entrega: {tempo_entrega} minutos; Id do Estafeta : {estafeta.id}; Classificacao do Estafeta: {estafeta.avaliacao_total/estafeta.nr_avaliacoes}.\n")
                    # remove a encomenda da lista de encomendas do estafeta
                    estafeta.encomendas.remove(e)
                    # atualiza a velocidade do transporte
                    estafeta.transporte_peso_atual -= e.peso
                    if estafeta.transporte == "carro":
                        estafeta.transporte_velocidade = ((50 - (0.1 * estafeta.transporte_peso_atual)) * 1000) / 60
                    if estafeta.transporte == "mota":
                        estafeta.transporte_velocidade = ((35 - (0.5 * estafeta.transporte_peso_atual)) * 1000) / 60
                    if estafeta.transporte == "bicicleta":
                        estafeta.transporte_velocidade = ((10 - (0.6 * estafeta.transporte_peso_atual)) * 1000) / 60
            # dá print à path do caminho mais rápido
            print(f"PATH: {paths}")
            # dá print ao custo total do caminho mais rápido
            print(f"CUSTO TOTAL: {custoTotal}")
            # cria uma variavel que vai conter todos os nós visitados
            # isto foi feito visto que path_total era uma lista de sets e listas e nós queriamos apenas uma lista como return
            lista_resultante = []
            # itera sobre os elementos da lista original
            for elemento in path_total:
                # se o elemento for um conjunto, adiciona os seus elementos à lista resultante
                if isinstance(elemento, set):
                    lista_resultante.extend(list(elemento))
                # se o elemento for uma lista, adiciona os seus elementos à lista resultante
                elif isinstance(elemento, list):
                    lista_resultante.extend(elemento)
            # dá print a todos os nós visitados durante a execução do programa
            print(f"NODOS VISITADOS: {lista_resultante}")
        else:
            # cria variavel para guardar nodos visitados
            visited = []
            # itera todos os nodes em nodesToFind
            for node in nodesToFind:
                # e se não existir informação sobre o custo e a path para chegar entre o startNode e o nodeToFind usando o algoritmo em questão ele faz essa pesquisa e guarda a informação correspondente
                if (startNode, node) not in self.dicBFS:
                    v, pt, custo = self.procura_BFS(startNode, node)
                    self.dicBFS[(startNode, node)] = (pt, custo)
                    visited.append(v)
                # se já houver essa informação guarda a variavel visited como lista vazia uma vez que nao foi preciso visitar nenhum node
                else:
                    visited = []
            # cria variaveis
            menorCusto = float('inf')
            melhorPath = []
            nextNode = None
            # itera o dicionario e ve qual o nodeToFind e o path para lá chegar que representam menor custo, esse será o node que será visitado a seguir
            for chave, valor in self.dicBFS.items():
                sn, fn = chave
                pa, c = valor
                if sn == startNode and fn in nodesToFind and c < menorCusto:
                    nextNode = fn
                    melhorPath = pa
                    menorCusto = c
            paths.append(melhorPath)
            path_total.append(visited)
            custoTotal += menorCusto
            # itera a lista de encomendas de um estafeta
            for e in estafeta.encomendas:
                # se a rua da encomenda for o node onde estamos atualmente
                if e.rua_destino == startNode:
                    # dá print que a encomenda esta no sitio de entrega
                    print(f"Encomenda Chegou ao Destino: {e.rua_destino}")
                    # calcular tempo de entrega da encomenda e atribui a classificação ao estafeta associada
                    distancia = custoTotal
                    prazo = e.prazo_entrega
                    velocidade = estafeta.transporte_velocidade
                    tempo_entrega = distancia/velocidade
                    # ver se a encomenda esta atrasada
                    if prazo > tempo_entrega:
                        print("Entrega chegou a tempo!")
                        # se a encomenda chegar antes de metade do prazo de entrega atribui nota 5
                        if prazo > tempo_entrega/2:
                            avaliacao = 5
                        # se chegar a tempo mas não em metade do prazo atribui 3
                        else:
                            avaliacao = 3
                    if prazo < tempo_entrega:
                        print("Entrega não chegou a tempo!")
                        # se chegar fora do prazo de entrega atribui nota 1
                        avaliacao = 1
                    # atualiza a avaliação do estafeta
                    estafeta.avaliacao_total += avaliacao
                    estafeta.nr_avaliacoes += 1
                    # escreve em ficheiro a entrega da encomenda
                    with open('Entregas.txt','a') as arquivo:
                        arquivo.write(f"Rua Destino: {e.rua_destino}; Peso: {e.peso}kg; Volume: {e.volume}cm2; Preco: {e.preco}; Avaliacao: {avaliacao}; Meio de Transporte: {estafeta.transporte}; Prazo de Entrega: {prazo} minutos; Tempo de entrega: {tempo_entrega} minutos; Id do Estafeta : {estafeta.id}; Classificacao do Estafeta: {estafeta.avaliacao_total/estafeta.nr_avaliacoes}.\n")
                    # remove a encomenda da lista de encomendas do estafeta uma vez que já foi entregue
                    estafeta.encomendas.remove(e)
                    # atualiza a  velocidade do transporte uma vez que há menos peso
                    estafeta.transporte_peso_atual -= e.peso
                    if estafeta.transporte == "carro":
                        estafeta.transporte_velocidade = ((50 - (0.1 * estafeta.transporte_peso_atual)) * 1000) / 60
                    if estafeta.transporte == "mota":
                        estafeta.transporte_velocidade = ((35 - (0.5 * estafeta.transporte_peso_atual)) * 1000) / 60
                    if estafeta.transporte == "bicicleta":
                        estafeta.transporte_velocidade = ((10 - (0.6 * estafeta.transporte_peso_atual)) * 1000) / 60
            # chama outra vez o método uma vez que ainda há encomendas a serem entregues, desta vez com o next node, que é o node com menor custo para ser encontrado
            self.entregar_entregas_BFS3(nextNode, estafeta, paths, custoTotal, path_total)
        # dá return a dizer que todas as entregas daquele estafeta foram bem sucedidas
        return "Entregas Bem Sucedidas!\n\n"


    ###################################################
    # Função   getneighbours, devolve vizinhos de um nó
    ####################################################

    def getNeighbours(self, nodo):
        lista = []
        for (adjacente, peso) in self.m_graph[nodo]:
            lista.append((adjacente, peso))
        return lista

    ###########################
    # desenha grafo  modo grafico
    #########################

    def desenha(self):
        ##criar lista de vertices
        lista_v = self.m_nodes
        g = nx.Graph()
        for nodo in lista_v:
            n = nodo.getName()
            g.add_node(n)
            for (adjacente, peso) in self.m_graph[n]:
                g.add_edge(n, adjacente, weight=peso)

        pos = nx.spring_layout(g)
        nx.draw_networkx(g, pos, with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

        plt.draw()
        plt.show()

    ####################################33
    #    add_heuristica   -> define heuristica para cada nodo
    ################################

    def add_heuristica2(self, ni, nf, estima):
        self.m_h2[(ni,nf)] = estima


    ##########################################3
    #
    def calcula_est(self, estima):
        l = list(estima.keys())
        min_estima = estima[l[0]]
        node = l[0]
        for k, v in estima.items():
            if v < min_estima:
                min_estima = v
                node = k
        return node


    ###################################3
    # devolve heuristica do nodo
    ####################################

    def getH(self, start, nodo):
        for chave, valor in self.m_h2.items():
            ni, nf = chave
            h = valor
            #print(f"ni:{ni} nf:{nf} h:{h}")
            if ni == start and nf == nodo:
                return h
        else:
            return 1500


    ##########################################
    #    A*
    ##########################################
    def procura_aStar(self, start, end):
        # open_list is a list of nodes which have been visited, but who's neighbors
        # haven't all been inspected, starts off with the start node
        # closed_list is a list of nodes which have been visited
        # and who's neighbors have been inspected
        open_list = {start}
        closed_list = set([])

        # g contains current distances from start_node to all other nodes
        # the default value (if it's not found in the map) is +infinity
        g = {}  ##  g é apra substiruir pelo peso  ???

        g[start] = 0

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[start] = start
        n = None
        while len(open_list) > 0:
            # find a node with the lowest value of f() - evaluation function
            calc_heurist = {}
            flag = 0
            for v in open_list:
                if n == None:
                    n = v
                else:
                    flag = 1
                    #print(self.getH(start,v))
                    #print(f"VALOR DA HEURISTICA ENTRE {start} E {v} È {self.getH(start,v)}")
                    calc_heurist[v] = g[v] + self.getH(start,v)
            if flag == 1:
                min_estima = self.calcula_est(calc_heurist)
                n = min_estima
            if n == None:
                print('Path does not exist!')
                return None

            # if the current node is the stop_node
            # then we begin reconstructin the path from it to the start_node
            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                #print('Path found: {}'.format(reconst_path))
                merged_list = open_list.union(closed_list)
                return (merged_list,reconst_path, self.calcula_custo(reconst_path))

            # for all neighbors of the current node do
            for (m, weight) in self.getNeighbours(n):  # definir função getneighbours  tem de ter um par nodo peso
                # if the current node isn't in both open_list and closed_list
                # add it to open_list and note n as it's parent
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            # remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None


    def entregar_entregas_aStar(self, startNode, nodesToFind, paths, custoTotal):
        # calcular custo e path de todos os nodes finais ate ao inicial
        if not nodesToFind:
            print (f"PATHS: {paths}")
            print (f"CUSTO: {custoTotal}")
            self.dicAstar.clear()
        else:
            for node in nodesToFind:
                #pat, cs = self.procura_aStar(startNode,node)
                result = self.procura_aStar(startNode, node)
                if result is not None:
                    pat, cs = result
                    self.dicAstar[(startNode,node)]= (pat,cs)
            # ver qual o node com menor custo
            menorCusto = float('inf')
            melhorPath = []
            nextNode = None
            for chave,valor in self.dicAstar.items():
                s, f = chave
                pa, c = valor
                if s == startNode and f in nodesToFind and c < menorCusto:
                    nextNode= f
                    melhorPath = pa
                    menorCusto = c
            paths.append(melhorPath)
            custoTotal += menorCusto
            remainingNodes = nodesToFind[:]
            if nextNode in remainingNodes:
                remainingNodes.remove(nextNode)
            self.entregar_entregas_aStar(nextNode,remainingNodes,paths,custoTotal)

    def entregar_entregas_aStar3(self, startNode, estafeta, paths, custoTotal, path_total):
        # inicia um set para guardar as localizações onde devemos passar (ruas das encomendas)
        nodesToFind = set()
        # itera as encomendas de um estafeta e preenche os nodesToFind
        for enc in estafeta.encomendas:
            nodesToFind.add(enc.rua_destino)
        # se o startNode se encontrar na lista de nodesToFind ele retira-o uma vez que ja lá está
        if startNode in nodesToFind:
            nodesToFind.remove(startNode)
        # se não existirem nodesToFind quer dizer que todas as encomendas já foram entregues
        if not nodesToFind:
            for e in estafeta.encomendas:
                if e.rua_destino == startNode:
                    # encomenda esta no sitio de entrega
                    print(f"Encomenda Chegou ao Destino: {e.rua_destino}")
                    # calcular tempo de entrega da encomenda
                    distancia = custoTotal
                    prazo = e.prazo_entrega
                    velocidade = estafeta.transporte_velocidade
                    tempo_entrega = distancia/velocidade
                    # ve se a encomenda está atrasada e atribui a respetiva avaliação conforme o tempo de entrega
                    if prazo > tempo_entrega:
                        print("Entrega Chegou a Tempo!")
                        # se a encomenda chegar antes de metade do prazo de entrega atribui nota 5
                        if prazo > tempo_entrega/2:
                            avaliacao = 5
                        # se chegar a tempo mas não em metade do prazo atribui 3
                        else:
                            avaliacao = 3
                    if prazo < tempo_entrega:
                        print("Entrega Não Chegou a Tempo!")
                        # se chegar fora do prazo de entrega atribui nota 1
                        avaliacao = 1
                    # atualiza a avaliação do estafeta
                    estafeta.avaliacao_total += avaliacao
                    estafeta.nr_avaliacoes += 1
                    # escreve em ficheiro a entrega da encomenda
                    with open('Entregas.txt','a') as arquivo:
                        arquivo.write(f"Rua Destino: {e.rua_destino}; Peso: {e.peso}kg; Volume: {e.volume}cm2; Preco: {e.preco}; Avaliacao: {avaliacao}; Meio de Transporte: {estafeta.transporte}; Prazo de Entrega: {prazo} minutos; Tempo de entrega: {tempo_entrega} minutos; Id do Estafeta : {estafeta.id}; Classificacao do Estafeta: {estafeta.avaliacao_total/estafeta.nr_avaliacoes}.\n")
                    # remove a encomenda da lista de encomendas do estafeta
                    estafeta.encomendas.remove(e)
                    # atualiza a velocidade do transporte
                    estafeta.transporte_peso_atual -= e.peso
                    if estafeta.transporte == "carro":
                        estafeta.transporte_velocidade = ((50 - (0.1 * estafeta.transporte_peso_atual)) * 1000) / 60
                    if estafeta.transporte == "mota":
                        estafeta.transporte_velocidade = ((35 - (0.5 * estafeta.transporte_peso_atual)) * 1000) / 60
                    if estafeta.transporte == "bicicleta":
                        estafeta.transporte_velocidade = ((10 - (0.6 * estafeta.transporte_peso_atual)) * 1000) / 60
            # dá print à path do caminho mais rápido
            print(f"PATH: {paths}")
            # dá print ao custo total do caminho mais rápido
            print(f"CUSTO TOTAL: {custoTotal}")
            # cria uma variavel que vai conter todos os nós visitados
            # isto foi feito visto que path_total era uma lista de sets e listas e nós queriamos apenas uma lista como return
            lista_resultante = []
            # itera sobre os elementos da lista original
            for elemento in path_total:
                # se o elemento for um conjunto, adiciona os seus elementos à lista resultante
                if isinstance(elemento, set):
                    lista_resultante.extend(list(elemento))
                # se o elemento for uma lista, adiciona os seus elementos à lista resultante
                elif isinstance(elemento, list):
                    lista_resultante.extend(elemento)
            # dá print a todos os nós visitados durante a execução do programa
            print(f"NODOS VISITADOS: {lista_resultante}")
        else:
            # cria variavel para guardar nodos visitados
            visited = []
            # itera todos os nodes em nodesToFind
            for node in nodesToFind:
                # e se não existir informação sobre o custo e a path para chegar entre o startNode e o nodeToFind usando o algoritmo em questão ele faz essa pesquisa e guarda a informação correspondente
                if (startNode, node) not in self.dicAstar:
                    v, pt, custo = self.procura_aStar(startNode, node)
                    self.dicAstar[(startNode, node)] = (pt, custo)
                    visited.append(v)
                # se já houver essa informação guarda a variavel visited como lista vazia uma vez que nao foi preciso visitar nenhum node
                else:
                    visited = []
            # cria variaveis
            menorCusto = float('inf')
            melhorPath = []
            nextNode = None
            # itera o dicionario e ve qual o nodeToFind e o path para lá chegar que representam menor custo, esse será o node que será visitado a seguir
            for chave, valor in self.dicAstar.items():
                sn, fn = chave
                pa, c = valor
                if sn == startNode and fn in nodesToFind and c < menorCusto:
                    nextNode = fn
                    melhorPath = pa
                    menorCusto = c
            paths.append(melhorPath)
            path_total.append(visited)
            custoTotal += menorCusto
            # itera a lista de encomendas de um estafeta
            for e in estafeta.encomendas:
                # se a rua da encomenda for o node onde estamos atualmente
                if e.rua_destino == startNode:
                    # dá print que a encomenda esta no sitio de entrega
                    print(f"Encomenda Chegou ao Destino: {e.rua_destino}")
                    # calcular tempo de entrega da encomenda e atribui a classificação ao estafeta associada
                    distancia = custoTotal
                    prazo = e.prazo_entrega
                    velocidade = estafeta.transporte_velocidade
                    tempo_entrega = distancia/velocidade
                    # ver se a encomenda esta atrasada
                    if prazo > tempo_entrega:
                        print("Entrega chegou a tempo!")
                        # se a encomenda chegar antes de metade do prazo de entrega atribui nota 5
                        if prazo > tempo_entrega/2:
                            avaliacao = 5
                        # se chegar a tempo mas não em metade do prazo atribui 3
                        else:
                            avaliacao = 3
                    if prazo < tempo_entrega:
                        print("Entrega não chegou a tempo!")
                        # se chegar fora do prazo de entrega atribui nota 1
                        avaliacao = 1
                    # atualiza a avaliação do estafeta
                    estafeta.avaliacao_total += avaliacao
                    estafeta.nr_avaliacoes += 1
                    # escreve em ficheiro a entrega da encomenda
                    with open('Entregas.txt','a') as arquivo:
                        arquivo.write(f"Rua Destino: {e.rua_destino}; Peso: {e.peso}kg; Volume: {e.volume}cm2; Preco: {e.preco}; Avaliacao: {avaliacao}; Meio de Transporte: {estafeta.transporte}; Prazo de Entrega: {prazo} minutos; Tempo de entrega: {tempo_entrega} minutos; Id do Estafeta : {estafeta.id}; Classificacao do Estafeta: {estafeta.avaliacao_total/estafeta.nr_avaliacoes}.\n")
                    # remove a encomenda da lista de encomendas do estafeta uma vez que já foi entregue
                    estafeta.encomendas.remove(e)
                    # atualiza a  velocidade do transporte uma vez que há menos peso
                    estafeta.transporte_peso_atual -= e.peso
                    if estafeta.transporte == "carro":
                        estafeta.transporte_velocidade = ((50 - (0.1 * estafeta.transporte_peso_atual)) * 1000) / 60
                    if estafeta.transporte == "mota":
                        estafeta.transporte_velocidade = ((35 - (0.5 * estafeta.transporte_peso_atual)) * 1000) / 60
                    if estafeta.transporte == "bicicleta":
                        estafeta.transporte_velocidade = ((10 - (0.6 * estafeta.transporte_peso_atual)) * 1000) / 60
            # chama outra vez o método uma vez que ainda há encomendas a serem entregues, desta vez com o next node, que é o node com menor custo para ser encontrado
            self.entregar_entregas_aStar3(nextNode, estafeta, paths, custoTotal, path_total)
        # dá return a dizer que todas as entregas daquele estafeta foram bem sucedidas
        return "Entregas Bem Sucedidas!\n\n"


    ##########################################
    #   Greedy
    ##########################################

    def greedy(self, start, end):
        # open_list é uma lista de nodos visitados, mas com vizinhos
        # que ainda não foram todos visitados, começa com o  start
        # closed_list é uma lista de nodos visitados
        # e todos os seus vizinhos também já o foram
        open_list = set([start])
        closed_list = set([])

        # parents é um dicionário que mantém o antecessor de um nodo
        # começa com start
        parents = {}
        parents[start] = start

        while len(open_list) > 0:
            n = None

            # encontraf nodo com a menor heuristica
            for v in open_list:
                if n == None or self.m_h2[start,v] < self.m_h2[start,n]:
                    n = v

            if n == None:
                print('Path does not exist!')
                return None

            # se o nodo corrente é o destino
            # reconstruir o caminho a partir desse nodo até ao start
            # seguindo o antecessor
            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()
                merged_list = open_list.union(closed_list)
                return (merged_list, reconst_path, self.calcula_custo(reconst_path))

            # para todos os vizinhos  do nodo corrente
            for (m, weight) in self.getNeighbours(n):
                # Se o nodo corrente nao esta na open nem na closed list
                # adiciona-lo à open_list e marcar o antecessor
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n

            # remover n da open_list e adiciona-lo à closed_list
            # porque todos os seus vizinhos foram inspecionados
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None

    def entregar_entregas_greedy(self, startNode, nodesToFind, paths, custoTotal):
        # calcular custo e path de todos os nodes finais ate ao inicial
        if not nodesToFind:
            print (f"PATHS: {paths}")
            print (f"CUSTO: {custoTotal}")
            self.dicGreedy.clear()
        else:
            for node in nodesToFind:
                pat, cs = self.greedy(startNode,node)
                self.dicGreedy[(startNode,node)]= (pat,cs)
            # ver qual o node com menor custo
            menorCusto = float('inf')
            melhorPath = []
            nextNode = None
            for chave,valor in self.dicGreedy.items():
                s, f = chave
                pa, c = valor
                if s == startNode and f in nodesToFind and c < menorCusto:
                    nextNode= f
                    melhorPath = pa
                    menorCusto = c
            paths.append(melhorPath)
            custoTotal += menorCusto
            remainingNodes = nodesToFind[:]
            if nextNode in remainingNodes:
                remainingNodes.remove(nextNode)
            self.entregar_entregas_greedy(nextNode,remainingNodes,paths,custoTotal)

    def entregar_entregas_greedy3(self, startNode, estafeta, paths, custoTotal, path_total):
        # inicia um set para guardar as localizações onde devemos passar (ruas das encomendas)
        nodesToFind = set()
        # itera as encomendas de um estafeta e preenche os nodesToFind
        for enc in estafeta.encomendas:
            nodesToFind.add(enc.rua_destino)
        # se o startNode se encontrar na lista de nodesToFind ele retira-o uma vez que ja lá está
        if startNode in nodesToFind:
            nodesToFind.remove(startNode)
        # se não existirem nodesToFind quer dizer que todas as encomendas já foram entregues
        if not nodesToFind:
            for e in estafeta.encomendas:
                if e.rua_destino == startNode:
                    # encomenda esta no sitio de entrega
                    print(f"Encomenda Chegou ao Destino: {e.rua_destino}")
                    # calcular tempo de entrega da encomenda
                    distancia = custoTotal
                    prazo = e.prazo_entrega
                    velocidade = estafeta.transporte_velocidade
                    tempo_entrega = distancia/velocidade
                    # ve se a encomenda está atrasada e atribui a respetiva avaliação conforme o tempo de entrega
                    if prazo > tempo_entrega:
                        print("Entrega Chegou a Tempo!")
                        # se a encomenda chegar antes de metade do prazo de entrega atribui nota 5
                        if prazo > tempo_entrega/2:
                            avaliacao = 5
                        # se chegar a tempo mas não em metade do prazo atribui 3
                        else:
                            avaliacao = 3
                    if prazo < tempo_entrega:
                        print("Entrega Não Chegou a Tempo!")
                        # se chegar fora do prazo de entrega atribui nota 1
                        avaliacao = 1
                    # atualiza a avaliação do estafeta
                    estafeta.avaliacao_total += avaliacao
                    estafeta.nr_avaliacoes += 1
                    # escreve em ficheiro a entrega da encomenda
                    with open('Entregas.txt','a') as arquivo:
                        arquivo.write(f"Rua Destino: {e.rua_destino}; Peso: {e.peso}kg; Volume: {e.volume}cm2; Preco: {e.preco}; Avaliacao: {avaliacao}; Meio de Transporte: {estafeta.transporte}; Prazo de Entrega: {prazo} minutos; Tempo de entrega: {tempo_entrega} minutos; Id do Estafeta : {estafeta.id}; Classificacao do Estafeta: {estafeta.avaliacao_total/estafeta.nr_avaliacoes}.\n")
                    # remove a encomenda da lista de encomendas do estafeta
                    estafeta.encomendas.remove(e)
                    # atualiza a velocidade do transporte
                    estafeta.transporte_peso_atual -= e.peso
                    if estafeta.transporte == "carro":
                        estafeta.transporte_velocidade = ((50 - (0.1 * estafeta.transporte_peso_atual)) * 1000) / 60
                    if estafeta.transporte == "mota":
                        estafeta.transporte_velocidade = ((35 - (0.5 * estafeta.transporte_peso_atual)) * 1000) / 60
                    if estafeta.transporte == "bicicleta":
                        estafeta.transporte_velocidade = ((10 - (0.6 * estafeta.transporte_peso_atual)) * 1000) / 60
            # dá print à path do caminho mais rápido
            print(f"PATH: {paths}")
            # dá print ao custo total do caminho mais rápido
            print(f"CUSTO TOTAL: {custoTotal}")
            # cria uma variavel que vai conter todos os nós visitados
            # isto foi feito visto que path_total era uma lista de sets e listas e nós queriamos apenas uma lista como return
            lista_resultante = []
            # itera sobre os elementos da lista original
            for elemento in path_total:
                # se o elemento for um conjunto, adiciona os seus elementos à lista resultante
                if isinstance(elemento, set):
                    lista_resultante.extend(list(elemento))
                # se o elemento for uma lista, adiciona os seus elementos à lista resultante
                elif isinstance(elemento, list):
                    lista_resultante.extend(elemento)
            # dá print a todos os nós visitados durante a execução do programa
            print(f"NODOS VISITADOS: {lista_resultante}")
        else:
            # cria variavel para guardar nodos visitados
            visited = []
            # itera todos os nodes em nodesToFind
            for node in nodesToFind:
                # e se não existir informação sobre o custo e a path para chegar entre o startNode e o nodeToFind usando o algoritmo em questão ele faz essa pesquisa e guarda a informação correspondente
                if (startNode, node) not in self.dicGreedy:
                    v, pt, custo = self.greedy(startNode, node)
                    self.dicGreedy[(startNode, node)] = (pt, custo)
                    visited.append(v)
                # se já houver essa informação guarda a variavel visited como lista vazia uma vez que nao foi preciso visitar nenhum node
                else:
                    visited = []
            # cria variaveis
            menorCusto = float('inf')
            melhorPath = []
            nextNode = None
            # itera o dicionario e ve qual o nodeToFind e o path para lá chegar que representam menor custo, esse será o node que será visitado a seguir
            for chave, valor in self.dicGreedy.items():
                sn, fn = chave
                pa, c = valor
                if sn == startNode and fn in nodesToFind and c < menorCusto:
                    nextNode = fn
                    melhorPath = pa
                    menorCusto = c
            paths.append(melhorPath)
            path_total.append(visited)
            custoTotal += menorCusto
            # itera a lista de encomendas de um estafeta
            for e in estafeta.encomendas:
                # se a rua da encomenda for o node onde estamos atualmente
                if e.rua_destino == startNode:
                    # dá print que a encomenda esta no sitio de entrega
                    print(f"Encomenda Chegou ao Destino: {e.rua_destino}")
                    # calcular tempo de entrega da encomenda e atribui a classificação ao estafeta associada
                    distancia = custoTotal
                    prazo = e.prazo_entrega
                    velocidade = estafeta.transporte_velocidade
                    tempo_entrega = distancia/velocidade
                    # ver se a encomenda esta atrasada
                    if prazo > tempo_entrega:
                        print("Entrega chegou a tempo!")
                        # se a encomenda chegar antes de metade do prazo de entrega atribui nota 5
                        if prazo > tempo_entrega/2:
                            avaliacao = 5
                        # se chegar a tempo mas não em metade do prazo atribui 3
                        else:
                            avaliacao = 3
                    if prazo < tempo_entrega:
                        print("Entrega não chegou a tempo!")
                        # se chegar fora do prazo de entrega atribui nota 1
                        avaliacao = 1
                    # atualiza a avaliação do estafeta
                    estafeta.avaliacao_total += avaliacao
                    estafeta.nr_avaliacoes += 1
                    # escreve em ficheiro a entrega da encomenda
                    with open('Entregas.txt','a') as arquivo:
                        arquivo.write(f"Rua Destino: {e.rua_destino}; Peso: {e.peso}kg; Volume: {e.volume}cm2; Preco: {e.preco}; Avaliacao: {avaliacao}; Meio de Transporte: {estafeta.transporte}; Prazo de Entrega: {prazo} minutos; Tempo de entrega: {tempo_entrega} minutos; Id do Estafeta : {estafeta.id}; Classificacao do Estafeta: {estafeta.avaliacao_total/estafeta.nr_avaliacoes}.\n")
                    # remove a encomenda da lista de encomendas do estafeta uma vez que já foi entregue
                    estafeta.encomendas.remove(e)
                    # atualiza a  velocidade do transporte uma vez que há menos peso
                    estafeta.transporte_peso_atual -= e.peso
                    if estafeta.transporte == "carro":
                        estafeta.transporte_velocidade = ((50 - (0.1 * estafeta.transporte_peso_atual)) * 1000) / 60
                    if estafeta.transporte == "mota":
                        estafeta.transporte_velocidade = ((35 - (0.5 * estafeta.transporte_peso_atual)) * 1000) / 60
                    if estafeta.transporte == "bicicleta":
                        estafeta.transporte_velocidade = ((10 - (0.6 * estafeta.transporte_peso_atual)) * 1000) / 60
            # chama outra vez o método uma vez que ainda há encomendas a serem entregues, desta vez com o next node, que é o node com menor custo para ser encontrado
            self.entregar_entregas_greedy3(nextNode, estafeta, paths, custoTotal, path_total)
        # dá return a dizer que todas as entregas daquele estafeta foram bem sucedidas
        return "Entregas Bem Sucedidas!\n\n"