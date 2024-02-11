from Estafeta import Estafeta
from Encomenda import Encomenda
from Grafo import Grafo
import copy
def main():

    ## parse às encomendas
    with open('Encomendas.txt', 'r') as arquivo:
        linhas = arquivo.readlines()
    # variavel que vai guardar a lista de encomendas
    lista_encomendas = []
    for linha in linhas:
        tokens = linha.split(';')
        rua_destino = tokens[0]
        peso = float(tokens[1])
        volume = float(tokens[2])
        preco = float(tokens[3])
        prazo_entrega = int(tokens[4])
        encomenda = Encomenda(rua_destino,peso,volume,preco,prazo_entrega)
        lista_encomendas.append(encomenda)
    print("ENCOMENDAS: ")
    for encomenda in lista_encomendas:
        print(f"Destino: {encomenda.rua_destino}, Peso: {encomenda.peso}, Volume: {encomenda.volume}, Preço: {encomenda.preco}, Prazo de Entrega: {encomenda.prazo_entrega}")

    ## parse aos estafetas
    with open('Estafetas.txt', 'r') as arquivo:
        linhas = arquivo.readlines()
    # variavel que vai guardar a lista de encomendas
    lista_estafetas = []
    for linha in linhas:
        tokens = linha.split(';')
        id = int(tokens[0])
        transporte = tokens[1]
        sum_avaliacoes = float(tokens[2])
        nr_avaliacoes = int(tokens[3])
        estafeta = Estafeta(id,transporte,sum_avaliacoes,nr_avaliacoes,[])
        lista_estafetas.append(estafeta)
    print("ESTAFETAS: ")
    for estafeta in lista_estafetas:
        print(
            f"Id: {estafeta.id}, Transporte: {estafeta.transporte}")

    lista_encomendas.sort()

    # Atribuir encomendas às bicicletas
    for estafeta in lista_estafetas:
        if estafeta.transporte == "bicicleta":
            encomendas_a_remover = []  # Lista auxiliar para armazenar encomendas a serem removidas
            for encomenda in lista_encomendas:
                if "Mogege" in encomenda.rua_destino and estafeta.transporte_peso_atual + encomenda.peso <= 5:
                    estafeta.transporte_peso_atual += encomenda.peso
                    estafeta.encomendas.append(copy.copy(encomenda))
                    # multiplica por 1000 e divide por 60 para passar de km/h para metros/minuto
                    estafeta.transporte_velocidade = ((10 - (0.6 * estafeta.transporte_peso_atual)) * 1000) / 60
                    encomendas_a_remover.append(encomenda)
                    print(f"ENCOMENDA: {encomenda.rua_destino} ADICIONADA A ESTAFETA {estafeta.id} (BICICLETA)")
            # remove as encomendas que já foram atribuídas da lista de encomendas disponíveis
            for encomenda in encomendas_a_remover:
                lista_encomendas.remove(encomenda)

    # Atribuir encomendas às motas
    for estafeta in lista_estafetas:
        if estafeta.transporte == "mota":
            encomendas_a_remover = []  # Lista auxiliar para armazenar encomendas a serem removidas
            for encomenda in lista_encomendas:
                if estafeta.transporte_peso_atual + encomenda.peso <= 20:
                    estafeta.transporte_peso_atual += encomenda.peso
                    estafeta.encomendas.append(encomenda)
                    # multiplica por 1000 e divide por 60 para passar de km/h para metros/minuto
                    estafeta.transporte_velocidade = ((35 - (0.5 * estafeta.transporte_peso_atual)) * 1000) / 60
                    encomendas_a_remover.append(encomenda)
                    print(f"ENCOMENDA: {encomenda.rua_destino} ADICIONADA A ESTAFETA {estafeta.id} (MOTA)")
            # remove as encomendas que já foram atribuídas da lista de encomendas disponíveis
            for encomenda in encomendas_a_remover:
                lista_encomendas.remove(encomenda)

    # Atribuir encomendas aos carros
    for estafeta in lista_estafetas:
        if estafeta.transporte == "carro":
            encomendas_a_remover = []  # Lista auxiliar para armazenar encomendas a serem removidas
            for encomenda in lista_encomendas:
                if estafeta.transporte_peso_atual + encomenda.peso <= 100:
                    estafeta.transporte_peso_atual += encomenda.peso
                    estafeta.encomendas.append(encomenda)
                    # multiplica por 1000 e divide por 60 para passar de km/h para metros/minuto
                    estafeta.transporte_velocidade = ((50 - (0.1 * estafeta.transporte_peso_atual)) * 1000) / 60
                    encomendas_a_remover.append(encomenda)
                    print(f"ENCOMENDA: {encomenda.rua_destino} ADICIONADA A ESTAFETA {estafeta.id} (CARRO)")
            # remove as encomendas que já foram atribuídas da lista de encomendas disponíveis
            for encomenda in encomendas_a_remover:
                lista_encomendas.remove(encomenda)

    lista_enc_rest = []
    for enc in lista_encomendas:
        lista_enc_rest.append(str(enc))
    print(f"LISTA DE ENCOMENDAS RESTANTE: {lista_enc_rest}")

    # Mostrar encomendas de cada estafeta
    for estafeta in lista_estafetas:
        lista_enc = []
        for enc in estafeta.encomendas:
            lista_enc.append(str(enc))
        print(f"ESTAFETA: {estafeta.id}, ENCOMENDAS: {lista_enc}")
       
    ##grafo das freguesias da cidade de famalicão
    g = Grafo()

    g.add_edge("Rua do Hospital, Joane","Rua da Paroquia, Pedome", 300)
    g.add_edge("Rua do Cabo, Mogege","Rua da Paroquia, Pedome", 300)
    g.add_edge("Rua de Moises, Pedome","Rua da Paroquia, Pedome", 200)
    g.add_edge("Rua do Cabo, Mogege","Rua de Moises, Pedome", 200)
    g.add_edge("Rua 25 de Abril, Mogege","Rua de Moises, Pedome", 500)
    g.add_edge("Rua 25 de Abril, Mogege","Rua da Fonte Longa, Mogege", 150)
    g.add_edge("Rua do Cabo, Mogege","Rua da Fonte Longa, Mogege", 200)
    g.add_edge("Rua da Ventuzela, Mogege","Rua da Fonte Longa, Mogege", 150)
    g.add_edge("Rua do Carril, Mogege","Rua da Fonte Longa, Mogege", 200)
    g.add_edge("Rua do Carril, Mogege","Rua do Amigo, Joane", 400)
    g.add_edge("Rua Sao Pedro, Joane","Rua do Amigo, Joane", 150)
    g.add_edge("Rua Sao Pedro, Joane","Rua do Hospital, Joane", 200)
    g.add_edge("Rua Sao Pedro, Joane","Rua do Lamego, Joane", 400)
    g.add_edge("Rua de Santo Amaro, Joane","Rua do Lamego, Joane", 150)
    g.add_edge("Rua de Santo Amaro, Joane","Rua do Carril, Mogege", 350)
    g.add_edge("Rua de Santo Amaro, Joane","Rua do Relogio, Vermoim", 450)
    g.add_edge("Rua das Fontainhas, Casteloes","Rua do Relogio, Vermoim", 500)
    g.add_edge("Rua das Fontainhas, Casteloes","Rua de Santo Antonio, Casteloes", 150)
    g.add_edge("Rua do Carvalho, Ruivaes","Rua de Santo Antonio, Casteloes", 250)
    g.add_edge("Rua da Ventuzela, Mogege","Rua de Santo Antonio, Casteloes", 350)
    g.add_edge("Rua do Lobo, Seide","Rua de Santo Antonio, Casteloes", 350)
    g.add_edge("Rua do Monteiro, Casteloes","Rua de Santo Antonio, Casteloes", 200)
    g.add_edge("Rua do Lobo, Seide","Rua 25 de Abril, Mogege", 400)

    # Heuristicas da Rua da Fonte Longa, Mogege
    g.add_heuristica2("Rua da Fonte Longa, Mogege","Rua da Ventuzela, Mogege", 150)
    g.add_heuristica2("Rua da Fonte Longa, Mogege","Rua do Carril, Mogege", 200)
    g.add_heuristica2("Rua da Fonte Longa, Mogege","Rua do Cabo, Mogege", 200)
    g.add_heuristica2("Rua da Fonte Longa, Mogege","Rua 25 de Abril, Mogege", 150)
    g.add_heuristica2("Rua da Fonte Longa, Mogege","Rua do Amigo, Joane", 500)
    g.add_heuristica2("Rua da Fonte Longa, Mogege","Rua de Santo Amaro, Joane", 550)
    g.add_heuristica2("Rua da Fonte Longa, Mogege","Rua do Lamego, Joane", 700)
    g.add_heuristica2("Rua da Fonte Longa, Mogege","Rua Sao Pedro, Joane", 650)
    g.add_heuristica2("Rua da Fonte Longa, Mogege","Rua do Hospital, Joane", 1050)
    g.add_heuristica2("Rua da Fonte Longa, Mogege","Rua da Paroquia, Pedome", 550)
    g.add_heuristica2("Rua da Fonte Longa, Mogege","Rua de Moises, Pedome", 300)
    g.add_heuristica2("Rua da Fonte Longa, Mogege","Rua do Lobo, Seide", 400)
    g.add_heuristica2("Rua da Fonte Longa, Mogege","Rua de Santo Antonio, Casteloes", 450)
    g.add_heuristica2("Rua da Fonte Longa, Mogege","Rua do Monteiro, Casteloes", 700)
    g.add_heuristica2("Rua da Fonte Longa, Mogege","Rua do Carvalho, Ruivaes", 700)
    g.add_heuristica2("Rua da Fonte Longa, Mogege","Rua das Fontainhas, Casteloes", 650)
    g.add_heuristica2("Rua da Fonte Longa, Mogege","Rua do Relogio, Vermoim", 650)

    # Heuristicas da Rua da Ventuzela, Mogege
    g.add_heuristica2("Rua da Ventuzela, Mogege", "Rua da Fonte Longa, Mogege", 150)
    g.add_heuristica2("Rua da Ventuzela, Mogege", "Rua do Carril, Mogege", 250)
    g.add_heuristica2("Rua da Ventuzela, Mogege", "Rua do Cabo, Mogege", 400)
    g.add_heuristica2("Rua da Ventuzela, Mogege", "Rua 25 de Abril, Mogege", 200)
    g.add_heuristica2("Rua da Ventuzela, Mogege", "Rua do Amigo, Joane", 600)
    g.add_heuristica2("Rua da Ventuzela, Mogege", "Rua de Santo Amaro, Joane", 400)
    g.add_heuristica2("Rua da Ventuzela, Mogege", "Rua do Lamego, Joane", 500)
    g.add_heuristica2("Rua da Ventuzela, Mogege", "Rua Sao Pedro, Joane", 700)
    g.add_heuristica2("Rua da Ventuzela, Mogege", "Rua do Hospital, Joane", 950)
    g.add_heuristica2("Rua da Ventuzela, Mogege", "Rua da Paroquia, Pedome", 700)
    g.add_heuristica2("Rua da Ventuzela, Mogege", "Rua de Moises, Pedome", 550)
    g.add_heuristica2("Rua da Ventuzela, Mogege", "Rua do Lobo, Seide", 300)
    g.add_heuristica2("Rua da Ventuzela, Mogege", "Rua de Santo Antonio, Casteloes", 200)
    g.add_heuristica2("Rua da Ventuzela, Mogege", "Rua do Monteiro, Casteloes", 400)
    g.add_heuristica2("Rua da Ventuzela, Mogege", "Rua do Carvalho, Ruivaes", 500)
    g.add_heuristica2("Rua da Ventuzela, Mogege", "Rua das Fontainhas, Casteloes", 350)
    g.add_heuristica2("Rua da Ventuzela, Mogege", "Rua do Relogio, Vermoim", 750)
    
    # Heuristicas da Rua do Carril, Mogege
    g.add_heuristica2("Rua do Carril, Mogege", "Rua da Ventuzela, Mogege", 250)
    g.add_heuristica2("Rua do Carril, Mogege", "Rua da Fonte Longa, Mogege", 200)
    g.add_heuristica2("Rua do Carril, Mogege", "Rua do Cabo, Mogege", 300)
    g.add_heuristica2("Rua do Carril, Mogege", "Rua 25 de Abril, Mogege", 300)
    g.add_heuristica2("Rua do Carril, Mogege", "Rua do Amigo, Joane", 400)
    g.add_heuristica2("Rua do Carril, Mogege", "Rua de Santo Amaro, Joane", 350)
    g.add_heuristica2("Rua do Carril, Mogege", "Rua do Lamego, Joane", 350)
    g.add_heuristica2("Rua do Carril, Mogege", "Rua Sao Pedro, Joane", 400)
    g.add_heuristica2("Rua do Carril, Mogege", "Rua do Hospital, Joane", 650)
    g.add_heuristica2("Rua do Carril, Mogege", "Rua da Paroquia, Pedome", 700)
    g.add_heuristica2("Rua do Carril, Mogege", "Rua de Moises, Pedome", 650)
    g.add_heuristica2("Rua do Carril, Mogege", "Rua do Lobo, Seide", 550)
    g.add_heuristica2("Rua do Carril, Mogege", "Rua de Santo Antonio, Casteloes", 700)
    g.add_heuristica2("Rua do Carril, Mogege", "Rua do Monteiro, Casteloes", 850)
    g.add_heuristica2("Rua do Carril, Mogege", "Rua do Carvalho, Ruivaes", 1000)
    g.add_heuristica2("Rua do Carril, Mogege", "Rua das Fontainhas, Casteloes", 650)
    g.add_heuristica2("Rua do Carril, Mogege", "Rua do Relogio, Vermoim", 650)

    # Heuristicas da Rua do Cabo, Mogege
    g.add_heuristica2("Rua do Cabo, Mogege", "Rua da Ventuzela, Mogege", 400)
    g.add_heuristica2("Rua do Cabo, Mogege", "Rua da Fonte Longa, Mogege", 200)
    g.add_heuristica2("Rua do Cabo, Mogege", "Rua do Carril, Mogege", 300)
    g.add_heuristica2("Rua do Cabo, Mogege", "Rua da Fonte Longa, Mogege", 200)
    g.add_heuristica2("Rua do Cabo, Mogege", "Rua 25 de Abril, Mogege", 250)
    g.add_heuristica2("Rua do Cabo, Mogege", "Rua do Amigo, Joane", 750)
    g.add_heuristica2("Rua do Cabo, Mogege", "Rua de Santo Amaro, Joane", 700)
    g.add_heuristica2("Rua do Cabo, Mogege", "Rua do Lamego, Joane", 850)
    g.add_heuristica2("Rua do Cabo, Mogege", "Rua Sao Pedro, Joane", 900)
    g.add_heuristica2("Rua do Cabo, Mogege", "Rua do Hospital, Joane", 1150)
    g.add_heuristica2("Rua do Cabo, Mogege", "Rua da Paroquia, Pedome", 750)
    g.add_heuristica2("Rua do Cabo, Mogege", "Rua de Moises, Pedome", 500)
    g.add_heuristica2("Rua do Cabo, Mogege", "Rua do Lobo, Seide", 600)
    g.add_heuristica2("Rua do Cabo, Mogege", "Rua de Santo Antonio, Casteloes", 750)
    g.add_heuristica2("Rua do Cabo, Mogege", "Rua do Monteiro, Casteloes", 1000)
    g.add_heuristica2("Rua do Cabo, Mogege", "Rua do Carvalho, Ruivaes", 1050)
    g.add_heuristica2("Rua do Cabo, Mogege", "Rua das Fontainhas, Casteloes", 1000)
    g.add_heuristica2("Rua do Cabo, Mogege", "Rua do Relogio, Vermoim", 950)

    # Heuristicas da Rua 25 de Abril, Mogege
    g.add_heuristica2("Rua 25 de Abril, Mogege", "Rua da Ventuzela, Mogege", 200)
    g.add_heuristica2("Rua 25 de Abril, Mogege", "Rua da Fonte Longa, Mogege", 150)
    g.add_heuristica2("Rua 25 de Abril, Mogege", "Rua do Carril, Mogege", 300)
    g.add_heuristica2("Rua 25 de Abril, Mogege", "Rua do Cabo, Mogege", 250)
    g.add_heuristica2("Rua 25 de Abril, Mogege", "Rua da Fonte Longa, Mogege", 150)
    g.add_heuristica2("Rua 25 de Abril, Mogege", "Rua do Amigo, Joane", 500)
    g.add_heuristica2("Rua 25 de Abril, Mogege", "Rua de Santo Amaro, Joane", 450)
    g.add_heuristica2("Rua 25 de Abril, Mogege", "Rua do Lamego, Joane", 600)
    g.add_heuristica2("Rua 25 de Abril, Mogege", "Rua Sao Pedro, Joane", 550)
    g.add_heuristica2("Rua 25 de Abril, Mogege", "Rua do Hospital, Joane", 800)
    g.add_heuristica2("Rua 25 de Abril, Mogege", "Rua da Paroquia, Pedome", 500)
    g.add_heuristica2("Rua 25 de Abril, Mogege", "Rua de Moises, Pedome", 250)
    g.add_heuristica2("Rua 25 de Abril, Mogege", "Rua do Lobo, Seide", 350)
    g.add_heuristica2("Rua 25 de Abril, Mogege", "Rua de Santo Antonio, Casteloes", 500)
    g.add_heuristica2("Rua 25 de Abril, Mogege", "Rua do Monteiro, Casteloes", 750)
    g.add_heuristica2("Rua 25 de Abril, Mogege", "Rua do Carvalho, Ruivaes", 800)
    g.add_heuristica2("Rua 25 de Abril, Mogege", "Rua das Fontainhas, Casteloes", 750)
    g.add_heuristica2("Rua 25 de Abril, Mogege", "Rua do Relogio, Vermoim", 700)

    # Heuristicas da Rua do Amigo, Joane
    g.add_heuristica2("Rua do Amigo, Joane", "Rua da Ventuzela, Mogege", 600)
    g.add_heuristica2("Rua do Amigo, Joane", "Rua da Fonte Longa, Mogege", 500)
    g.add_heuristica2("Rua do Amigo, Joane", "Rua do Carril, Mogege", 400)
    g.add_heuristica2("Rua do Amigo, Joane", "Rua do Cabo, Mogege", 750)
    g.add_heuristica2("Rua do Amigo, Joane", "Rua 25 de Abril, Mogege", 500)
    g.add_heuristica2("Rua do Amigo, Joane", "Rua de Santo Amaro, Joane", 150)
    g.add_heuristica2("Rua do Amigo, Joane", "Rua do Lamego, Joane", 300)
    g.add_heuristica2("Rua do Amigo, Joane", "Rua Sao Pedro, Joane", 350)
    g.add_heuristica2("Rua do Amigo, Joane", "Rua do Hospital, Joane", 600)
    g.add_heuristica2("Rua do Amigo, Joane", "Rua da Paroquia, Pedome", 300)
    g.add_heuristica2("Rua do Amigo, Joane", "Rua de Moises, Pedome", 550)
    g.add_heuristica2("Rua do Amigo, Joane", "Rua do Lobo, Seide", 750)
    g.add_heuristica2("Rua do Amigo, Joane", "Rua de Santo Antonio, Casteloes", 900)
    g.add_heuristica2("Rua do Amigo, Joane", "Rua do Monteiro, Casteloes", 1150)
    g.add_heuristica2("Rua do Amigo, Joane", "Rua do Carvalho, Ruivaes", 1200)
    g.add_heuristica2("Rua do Amigo, Joane", "Rua das Fontainhas, Casteloes", 1150)
    g.add_heuristica2("Rua do Amigo, Joane", "Rua do Relogio, Vermoim", 1100)

    # Heuristicas da Rua de Santo Amaro, Joane
    g.add_heuristica2("Rua de Santo Amaro, Joane", "Rua da Ventuzela, Mogege", 400)
    g.add_heuristica2("Rua de Santo Amaro, Joane", "Rua da Fonte Longa, Mogege", 550)
    g.add_heuristica2("Rua de Santo Amaro, Joane", "Rua do Carril, Mogege", 350)
    g.add_heuristica2("Rua de Santo Amaro, Joane", "Rua do Cabo, Mogege", 700)
    g.add_heuristica2("Rua de Santo Amaro, Joane", "Rua 25 de Abril, Mogege", 450)
    g.add_heuristica2("Rua de Santo Amaro, Joane", "Rua do Amigo, Joane", 200)
    g.add_heuristica2("Rua de Santo Amaro, Joane", "Rua Sao Pedro, Joane", 150)
    g.add_heuristica2("Rua de Santo Amaro, Joane", "Rua do Lamego, Joane", 450)
    g.add_heuristica2("Rua de Santo Amaro, Joane", "Rua do Hospital, Joane", 250)
    g.add_heuristica2("Rua de Santo Amaro, Joane", "Rua da Paroquia, Pedome", 550)
    g.add_heuristica2("Rua de Santo Amaro, Joane", "Rua de Moises, Pedome", 300)
    g.add_heuristica2("Rua de Santo Amaro, Joane", "Rua do Lobo, Seide", 200)
    g.add_heuristica2("Rua de Santo Amaro, Joane", "Rua de Santo Antonio, Casteloes", 350)
    g.add_heuristica2("Rua de Santo Amaro, Joane", "Rua do Monteiro, Casteloes", 600)
    g.add_heuristica2("Rua de Santo Amaro, Joane", "Rua do Carvalho, Ruivaes", 650)
    g.add_heuristica2("Rua de Santo Amaro, Joane", "Rua das Fontainhas, Casteloes", 600)
    g.add_heuristica2("Rua de Santo Amaro, Joane", "Rua do Relogio, Vermoim", 550)

    # Heuristicas da Rua do Lamego, Joane
    g.add_heuristica2("Rua do Lamego, Joane", "Rua da Ventuzela, Mogege", 500)
    g.add_heuristica2("Rua do Lamego, Joane", "Rua do Carril, Mogege", 350)
    g.add_heuristica2("Rua do Lamego, Joane", "Rua do Cabo, Mogege", 1050)
    g.add_heuristica2("Rua do Lamego, Joane", "Rua 25 de Abril, Mogege", 800)
    g.add_heuristica2("Rua do Lamego, Joane", "Rua do Amigo, Joane", 200)
    g.add_heuristica2("Rua do Lamego, Joane", "Rua de Santo Amaro, Joane", 450)
    g.add_heuristica2("Rua do Lamego, Joane", "Rua da Fonte Longa, Mogege",950)
    g.add_heuristica2("Rua do Lamego, Joane", "Rua Sao Pedro, Joane", 300)
    g.add_heuristica2("Rua do Lamego, Joane", "Rua do Hospital, Joane",200)
    g.add_heuristica2("Rua do Lamego, Joane", "Rua da Paroquia, Pedome",600)
    g.add_heuristica2("Rua do Lamego, Joane", "Rua de Moises, Pedome", 600)
    g.add_heuristica2("Rua do Lamego, Joane", "Rua do Lobo, Seide", 500)
    g.add_heuristica2("Rua do Lamego, Joane", "Rua de Santo Antonio, Casteloes", 600)
    g.add_heuristica2("Rua do Lamego, Joane", "Rua do Monteiro, Casteloes", 650)
    g.add_heuristica2("Rua do Lamego, Joane", "Rua do Carvalho, Ruivaes", 450)
    g.add_heuristica2("Rua do Lamego, Joane", "Rua das Fontainhas, Casteloes", 750)
    g.add_heuristica2("Rua do Lamego, Joane", "Rua do Relogio, Vermoim", 550)

    # Heuristicas da Rua Sao Pedro, Joane
    g.add_heuristica2("Rua Sao Pedro, Joane", "Rua da Ventuzela, Mogege", 700)
    g.add_heuristica2("Rua Sao Pedro, Joane", "Rua da Fonte Longa, Mogege", 650)
    g.add_heuristica2("Rua Sao Pedro, Joane", "Rua do Carril, Mogege", 400)
    g.add_heuristica2("Rua Sao Pedro, Joane", "Rua do Cabo, Mogege", 900)
    g.add_heuristica2("Rua Sao Pedro, Joane", "Rua 25 de Abril, Mogege", 550)
    g.add_heuristica2("Rua Sao Pedro, Joane", "Rua do Amigo, Joane", 350)
    g.add_heuristica2("Rua Sao Pedro, Joane", "Rua de Santo Amaro, Joane", 200)
    g.add_heuristica2("Rua Sao Pedro, Joane", "Rua do Lamego, Joane", 150)
    g.add_heuristica2("Rua Sao Pedro, Joane", "Rua do Hospital, Joane", 250)
    g.add_heuristica2("Rua Sao Pedro, Joane", "Rua da Paroquia, Pedome", 400)
    g.add_heuristica2("Rua Sao Pedro, Joane", "Rua de Moises, Pedome", 350)
    g.add_heuristica2("Rua Sao Pedro, Joane", "Rua do Lobo, Seide", 550)
    g.add_heuristica2("Rua Sao Pedro, Joane", "Rua de Santo Antonio, Casteloes", 700)
    g.add_heuristica2("Rua Sao Pedro, Joane", "Rua do Monteiro, Casteloes", 950)
    g.add_heuristica2("Rua Sao Pedro, Joane", "Rua do Carvalho, Ruivaes", 1000)
    g.add_heuristica2("Rua Sao Pedro, Joane", "Rua das Fontainhas, Casteloes", 950)
    g.add_heuristica2("Rua Sao Pedro, Joane", "Rua do Relogio, Vermoim", 900)

    # Heuristicas da Rua do Hospital, Joane
    g.add_heuristica2("Rua do Hospital, Joane", "Rua da Ventuzela, Mogege", 950)
    g.add_heuristica2("Rua do Hospital, Joane", "Rua do Carril, Mogege", 650)
    g.add_heuristica2("Rua do Hospital, Joane", "Rua do Cabo, Mogege", 400)
    g.add_heuristica2("Rua do Hospital, Joane", "Rua 25 de Abril, Mogege", 350)
    g.add_heuristica2("Rua do Hospital, Joane", "Rua do Amigo, Joane", 200)
    g.add_heuristica2("Rua do Hospital, Joane", "Rua de Santo Amaro, Joane", 250)
    g.add_heuristica2("Rua do Hospital, Joane", "Rua do Lamego, Joane", 300)
    g.add_heuristica2("Rua do Hospital, Joane", "Rua Sao Pedro, Joane", 350)
    g.add_heuristica2("Rua do Hospital, Joane", "Rua da Fonte Longa, Mogege", 450)
    g.add_heuristica2("Rua do Hospital, Joane", "Rua da Paroquia, Pedome", 600)
    g.add_heuristica2("Rua do Hospital, Joane", "Rua de Moises, Pedome", 550)
    g.add_heuristica2("Rua do Hospital, Joane", "Rua do Lobo, Seide", 700)
    g.add_heuristica2("Rua do Hospital, Joane", "Rua de Santo Antonio, Casteloes", 750)
    g.add_heuristica2("Rua do Hospital, Joane", "Rua do Monteiro, Casteloes", 800)
    g.add_heuristica2("Rua do Hospital, Joane", "Rua do Carvalho, Ruivaes", 850)
    g.add_heuristica2("Rua do Hospital, Joane", "Rua das Fontainhas, Casteloes", 900)
    g.add_heuristica2("Rua do Hospital, Joane", "Rua do Relogio, Vermoim", 1000)

    # Heuristicas da Rua da Paroquia, Pedome
    g.add_heuristica2("Rua da Paroquia, Pedome", "Rua da Ventuzela, Mogege", 700)
    g.add_heuristica2("Rua da Paroquia, Pedome", "Rua da Fonte Longa, Mogege", 550)
    g.add_heuristica2("Rua da Paroquia, Pedome", "Rua do Carril, Mogege", 700)
    g.add_heuristica2("Rua da Paroquia, Pedome", "Rua do Cabo, Mogege", 900)
    g.add_heuristica2("Rua da Paroquia, Pedome", "Rua 25 de Abril, Mogege", 550)
    g.add_heuristica2("Rua da Paroquia, Pedome", "Rua do Amigo, Joane", 350)
    g.add_heuristica2("Rua da Paroquia, Pedome", "Rua de Santo Amaro, Joane", 200)
    g.add_heuristica2("Rua da Paroquia, Pedome", "Rua do Lamego, Joane", 150)
    g.add_heuristica2("Rua da Paroquia, Pedome", "Rua do Hospital, Joane", 250)
    g.add_heuristica2("Rua da Paroquia, Pedome", "Rua de Moises, Pedome", 400)
    g.add_heuristica2("Rua da Paroquia, Pedome", "Rua do Lobo, Seide", 600)
    g.add_heuristica2("Rua da Paroquia, Pedome", "Rua de Santo Antonio, Casteloes", 700)
    g.add_heuristica2("Rua da Paroquia, Pedome", "Rua do Monteiro, Casteloes", 950)
    g.add_heuristica2("Rua da Paroquia, Pedome", "Rua do Carvalho, Ruivaes", 1000)
    g.add_heuristica2("Rua da Paroquia, Pedome", "Rua das Fontainhas, Casteloes", 950)
    g.add_heuristica2("Rua da Paroquia, Pedome", "Rua do Relogio, Vermoim", 900)
    g.add_heuristica2("Rua da Paroquia, Pedome", "Rua Sao Pedro, Joane", 400)

    # Heurísticas da Rua de Moises, Pedome
    g.add_heuristica2("Rua de Moises, Pedome", "Rua da Ventuzela, Mogege", 550)
    g.add_heuristica2("Rua de Moises, Pedome", "Rua do Carril, Mogege", 650)
    g.add_heuristica2("Rua de Moises, Pedome", "Rua do Cabo, Mogege", 600)
    g.add_heuristica2("Rua de Moises, Pedome", "Rua 25 de Abril, Mogege", 550)
    g.add_heuristica2("Rua de Moises, Pedome", "Rua do Amigo, Joane", 400)
    g.add_heuristica2("Rua de Moises, Pedome", "Rua de Santo Amaro, Joane", 450)
    g.add_heuristica2("Rua de Moises, Pedome", "Rua do Lamego, Joane", 500)
    g.add_heuristica2("Rua de Moises, Pedome", "Rua Sao Pedro, Joane", 550)
    g.add_heuristica2("Rua de Moises, Pedome", "Rua do Hospital, Joane", 550)
    g.add_heuristica2("Rua de Moises, Pedome", "Rua da Paroquia, Pedome", 100)
    g.add_heuristica2("Rua de Moises, Pedome", "Rua da Fonte Longa, Mogege", 700)
    g.add_heuristica2("Rua de Moises, Pedome", "Rua do Lobo, Seide", 800)
    g.add_heuristica2("Rua de Moises, Pedome", "Rua de Santo Antonio, Casteloes", 850)
    g.add_heuristica2("Rua de Moises, Pedome", "Rua do Monteiro, Casteloes", 900)
    g.add_heuristica2("Rua de Moises, Pedome", "Rua do Carvalho, Ruivaes", 950)
    g.add_heuristica2("Rua de Moises, Pedome", "Rua das Fontainhas, Casteloes", 1000)
    g.add_heuristica2("Rua de Moises, Pedome", "Rua do Relogio, Vermoim", 1100)

    # Heuristicas da Rua do Lobo, Seide
    g.add_heuristica2("Rua do Lobo, Seide", "Rua da Ventuzela, Mogege", 300)
    g.add_heuristica2("Rua do Lobo, Seide", "Rua da Fonte Longa, Mogege", 400)
    g.add_heuristica2("Rua do Lobo, Seide", "Rua do Carril, Mogege", 550)
    g.add_heuristica2("Rua do Lobo, Seide", "Rua do Cabo, Mogege", 600)
    g.add_heuristica2("Rua do Lobo, Seide", "Rua 25 de Abril, Mogege", 350)
    g.add_heuristica2("Rua do Lobo, Seide", "Rua do Amigo, Joane", 750)
    g.add_heuristica2("Rua do Lobo, Seide", "Rua de Santo Amaro, Joane", 200)
    g.add_heuristica2("Rua do Lobo, Seide", "Rua Sao Pedro, Joane", 550)
    g.add_heuristica2("Rua do Lobo, Seide", "Rua da Fonte Longa, Mogege", 400)
    g.add_heuristica2("Rua do Lobo, Seide", "Rua do Hospital, Joane", 500)
    g.add_heuristica2("Rua do Lobo, Seide", "Rua da Paroquia, Pedome", 700)
    g.add_heuristica2("Rua do Lobo, Seide", "Rua de Moises, Pedome", 450)
    g.add_heuristica2("Rua do Lobo, Seide", "Rua de Santo Antonio, Casteloes", 300)
    g.add_heuristica2("Rua do Lobo, Seide", "Rua do Monteiro, Casteloes", 550)
    g.add_heuristica2("Rua do Lobo, Seide", "Rua do Carvalho, Ruivaes", 600)
    g.add_heuristica2("Rua do Lobo, Seide", "Rua das Fontainhas, Casteloes", 550)
    g.add_heuristica2("Rua do Lobo, Seide", "Rua do Relogio, Vermoim", 500)

    # Heuristicas da Rua de Santo Antonio, Casteloes
    g.add_heuristica2("Rua de Santo Antonio, Casteloes", "Rua da Ventuzela, Mogege", 200)
    g.add_heuristica2("Rua de Santo Antonio, Casteloes", "Rua da Fonte Longa, Mogege", 450)
    g.add_heuristica2("Rua de Santo Antonio, Casteloes", "Rua do Carril, Mogege", 700)
    g.add_heuristica2("Rua de Santo Antonio, Casteloes", "Rua do Cabo, Mogege", 750)
    g.add_heuristica2("Rua de Santo Antonio, Casteloes", "Rua 25 de Abril, Mogege", 500)
    g.add_heuristica2("Rua de Santo Antonio, Casteloes", "Rua do Amigo, Joane", 900)
    g.add_heuristica2("Rua de Santo Antonio, Casteloes", "Rua de Santo Amaro, Joane", 350)
    g.add_heuristica2("Rua de Santo Antonio, Casteloes", "Rua Sao Pedro, Joane", 700)
    g.add_heuristica2("Rua de Santo Antonio, Casteloes", "Rua do Lobo, Seide", 300)
    g.add_heuristica2("Rua de Santo Antonio, Casteloes", "Rua do Hospital, Joane", 550)
    g.add_heuristica2("Rua de Santo Antonio, Casteloes", "Rua da Paroquia, Pedome", 800)
    g.add_heuristica2("Rua de Santo Antonio, Casteloes", "Rua de Moises, Pedome", 550)
    g.add_heuristica2("Rua de Santo Antonio, Casteloes", "Rua do Monteiro, Casteloes", 250)
    g.add_heuristica2("Rua de Santo Antonio, Casteloes", "Rua do Carvalho, Ruivaes", 450)
    g.add_heuristica2("Rua de Santo Antonio, Casteloes", "Rua das Fontainhas, Casteloes", 300)
    g.add_heuristica2("Rua de Santo Antonio, Casteloes", "Rua do Relogio, Vermoim", 550)
    g.add_heuristica2("Rua de Santo Antonio, Casteloes", "Rua da Fonte Longa, Mogege", 450)

    # Heuristicas da Rua do Monteiro, Casteloes
    g.add_heuristica2("Rua do Monteiro, Casteloes", "Rua da Ventuzela, Mogege", 400)
    g.add_heuristica2("Rua do Monteiro, Casteloes", "Rua da Fonte Longa, Mogege", 700)
    g.add_heuristica2("Rua do Monteiro, Casteloes", "Rua do Carril, Mogege", 850)
    g.add_heuristica2("Rua do Monteiro, Casteloes", "Rua do Cabo, Mogege", 1000)
    g.add_heuristica2("Rua do Monteiro, Casteloes", "Rua 25 de Abril, Mogege", 750)
    g.add_heuristica2("Rua do Monteiro, Casteloes", "Rua do Amigo, Joane", 1150)
    g.add_heuristica2("Rua do Monteiro, Casteloes", "Rua de Santo Amaro, Joane", 600)
    g.add_heuristica2("Rua do Monteiro, Casteloes", "Rua Sao Pedro, Joane", 950)
    g.add_heuristica2("Rua do Monteiro, Casteloes", "Rua do Lobo, Seide", 550)
    g.add_heuristica2("Rua do Monteiro, Casteloes", "Rua do Hospital, Joane", 250)
    g.add_heuristica2("Rua do Monteiro, Casteloes", "Rua da Paroquia, Pedome", 500)
    g.add_heuristica2("Rua do Monteiro, Casteloes", "Rua de Moises, Pedome", 750)
    g.add_heuristica2("Rua do Monteiro, Casteloes", "Rua do Carvalho, Ruivaes", 850)
    g.add_heuristica2("Rua do Monteiro, Casteloes", "Rua das Fontainhas, Casteloes", 600)
    g.add_heuristica2("Rua do Monteiro, Casteloes", "Rua do Relogio, Vermoim", 850)
    g.add_heuristica2("Rua do Monteiro, Casteloes","Rua de Santo Antonio, Casteloes", 250)
    g.add_heuristica2("Rua do Monteiro, Casteloes", "Rua do Lamego, Joane", 750)

    # Heuristicas da Rua do Carvalho, Ruivaes
    g.add_heuristica2("Rua do Carvalho, Ruivaes", "Rua da Ventuzela, Mogege", 500)
    g.add_heuristica2("Rua do Carvalho, Ruivaes", "Rua da Fonte Longa, Mogege", 700)
    g.add_heuristica2("Rua do Carvalho, Ruivaes", "Rua do Carril, Mogege", 1000)
    g.add_heuristica2("Rua do Carvalho, Ruivaes", "Rua do Cabo, Mogege", 1050)
    g.add_heuristica2("Rua do Carvalho, Ruivaes", "Rua 25 de Abril, Mogege", 800)
    g.add_heuristica2("Rua do Carvalho, Ruivaes", "Rua do Amigo, Joane", 1200)
    g.add_heuristica2("Rua do Carvalho, Ruivaes", "Rua de Santo Amaro, Joane", 650)
    g.add_heuristica2("Rua do Carvalho, Ruivaes", "Rua Sao Pedro, Joane", 1000)
    g.add_heuristica2("Rua do Carvalho, Ruivaes", "Rua do Lobo, Seide", 600)
    g.add_heuristica2("Rua do Carvalho, Ruivaes", "Rua do Hospital, Joane", 700)
    g.add_heuristica2("Rua do Carvalho, Ruivaes", "Rua da Paroquia, Pedome", 950)
    g.add_heuristica2("Rua do Carvalho, Ruivaes", "Rua de Moises, Pedome", 1200)
    g.add_heuristica2("Rua do Carvalho, Ruivaes", "Rua do Monteiro, Casteloes", 850)
    g.add_heuristica2("Rua do Carvalho, Ruivaes", "Rua das Fontainhas, Casteloes", 750)
    g.add_heuristica2("Rua do Carvalho, Ruivaes", "Rua do Relogio, Vermoim", 1000)
    g.add_heuristica2("Rua do Carvalho, Ruivaes","Rua de Santo Antonio, Casteloes", 450)
    g.add_heuristica2("Rua do Carvalho, Ruivaes","Rua do Lamego, Joane", 850)

    # Heuristicas da Rua das Fontainhas, Casteloes
    g.add_heuristica2("Rua das Fontainhas, Casteloes", "Rua da Ventuzela, Mogege", 350)
    g.add_heuristica2("Rua das Fontainhas, Casteloes", "Rua do Carril, Mogege", 650)
    g.add_heuristica2("Rua das Fontainhas, Casteloes", "Rua do Cabo, Mogege",1000)
    g.add_heuristica2("Rua das Fontainhas, Casteloes", "Rua 25 de Abril, Mogege",750)
    g.add_heuristica2("Rua das Fontainhas, Casteloes", "Rua do Amigo, Joane",1150)
    g.add_heuristica2("Rua das Fontainhas, Casteloes", "Rua de Santo Amaro, Joane",600)
    g.add_heuristica2("Rua das Fontainhas, Casteloes", "Rua do Lamego, Joane",750)
    g.add_heuristica2("Rua das Fontainhas, Casteloes", "Rua Sao Pedro, Joane",950)
    g.add_heuristica2("Rua das Fontainhas, Casteloes", "Rua do Hospital, Joane",950)
    g.add_heuristica2("Rua das Fontainhas, Casteloes", "Rua da Paroquia, Pedome",950)
    g.add_heuristica2("Rua das Fontainhas, Casteloes", "Rua de Moises, Pedome",950)
    g.add_heuristica2("Rua das Fontainhas, Casteloes", "Rua do Lobo, Seide",850)
    g.add_heuristica2("Rua das Fontainhas, Casteloes", "Rua de Santo Antonio, Casteloes",150)
    g.add_heuristica2("Rua das Fontainhas, Casteloes", "Rua do Monteiro, Casteloes",200)
    g.add_heuristica2("Rua das Fontainhas, Casteloes", "Rua do Carvalho, Ruivaes",400)
    g.add_heuristica2("Rua das Fontainhas, Casteloes", "Rua da Fonte Longa, Mogege", 650)
    g.add_heuristica2("Rua das Fontainhas, Casteloes", "Rua do Relogio, Vermoim",300)

    # Heuristicas da Rua do Relogio, Vermoim
    g.add_heuristica2("Rua do Relogio, Vermoim", "Rua da Ventuzela, Mogege", 750)
    g.add_heuristica2("Rua do Relogio, Vermoim", "Rua da Fonte Longa, Mogege", 650)
    g.add_heuristica2("Rua do Relogio, Vermoim", "Rua do Carril, Mogege", 650)
    g.add_heuristica2("Rua do Relogio, Vermoim", "Rua do Cabo, Mogege", 600)
    g.add_heuristica2("Rua do Relogio, Vermoim", "Rua 25 de Abril, Mogege", 700)
    g.add_heuristica2("Rua do Relogio, Vermoim", "Rua do Amigo, Joane", 1100)
    g.add_heuristica2("Rua do Relogio, Vermoim", "Rua de Santo Amaro, Joane", 550)
    g.add_heuristica2("Rua do Relogio, Vermoim", "Rua Sao Pedro, Joane", 900)
    g.add_heuristica2("Rua do Relogio, Vermoim", "Rua do Lobo, Seide", 500)
    g.add_heuristica2("Rua do Relogio, Vermoim", "Rua do Hospital, Joane", 650)
    g.add_heuristica2("Rua do Relogio, Vermoim", "Rua da Paroquia, Pedome", 900)
    g.add_heuristica2("Rua do Relogio, Vermoim", "Rua de Moises, Pedome", 1150)
    g.add_heuristica2("Rua do Relogio, Vermoim", "Rua do Monteiro, Casteloes", 850)
    g.add_heuristica2("Rua do Relogio, Vermoim", "Rua do Carvalho, Ruivaes", 1000)
    g.add_heuristica2("Rua do Relogio, Vermoim", "Rua das Fontainhas, Casteloes", 250)
    g.add_heuristica2("Rua do Relogio, Vermoim","Rua de Santo Antonio, Casteloes", 550)
    g.add_heuristica2("Rua do Relogio, Vermoim","Rua do Lamego, Joane",950)

    saida = -1
    while saida != 0:
        # menu
        print("\n\n-------------------MENU---------------------")
        print("1-Imprimir Cidade                           |")
        print("2-Desenhar Cidade                           |")
        print("3-DFS                                       |")
        print("4-BFS                                       |")
        print("5-A*                                        |")
        print("6-Gulosa                                    |")
        print("7-Comparar Todos os Algoritmos de Procura   |")
        print("0-Saír                                      |")
        print("--------------------------------------------")
        saida = int(input("Introduza a sua opcao-> "))

        if saida == 0:
            print("A sair do programa...")

        elif saida == 1:
            print(g.m_graph)
            l = input("prima enter para continuar")

        elif saida == 2:
            g.desenha()

        # DFS
        elif saida == 3:
            for estafeta in lista_estafetas:
                enderecos_encomendas = []
                for encomenda in estafeta.encomendas:
                    enderecos_encomendas.append(encomenda.rua_destino)
                print(f"ENTREGAS A SEREM FEITAS EM: {enderecos_encomendas}")
                path = []
                c = 0
                path_total = []
                print(g.entregar_entregas_DFS3("Rua da Fonte Longa, Mogege",estafeta,path,c,path_total))
            l = input("prima enter para continuar")

        # BFS
        elif saida == 4:
            for estafeta in lista_estafetas:
                enderecos_encomendas = []
                for encomenda in estafeta.encomendas:
                    enderecos_encomendas.append(encomenda.rua_destino)
                print(f"ENTREGAS A SEREM FEITAS EM: {enderecos_encomendas}")
                path = []
                c = 0
                path_total = []
                print(g.entregar_entregas_BFS3("Rua da Fonte Longa, Mogege",estafeta,path,c,path_total))
            l = input("prima enter para continuar")

        # A*
        elif saida == 5:
            for estafeta in lista_estafetas:
                enderecos_encomendas = []
                for encomenda in estafeta.encomendas:
                    enderecos_encomendas.append(encomenda.rua_destino)
                print(f"ENTREGAS A SEREM FEITAS EM: {enderecos_encomendas}")
                path = []
                c = 0
                path_total = []
                print(g.entregar_entregas_aStar3("Rua da Fonte Longa, Mogege", estafeta, path, c, path_total))
            l = input("prima enter para continuar")

        # Gulosa
        elif saida == 6:
            for estafeta in lista_estafetas:
                enderecos_encomendas = []
                for encomenda in estafeta.encomendas:
                    enderecos_encomendas.append(encomenda.rua_destino)
                print(f"ENTREGAS A SEREM FEITAS EM: {enderecos_encomendas}")
                path = []
                c = 0
                path_total = []
                print(g.entregar_entregas_greedy3("Rua da Fonte Longa, Mogege", estafeta, path, c, path_total))
            l = input("prima enter para continuar")

        # comparativo dos 4 algoritmos
        elif saida == 7:
            # 4 copias da lista de encomendas, uma para cada algoritmo de procura
            lista_estafetas_DFS = copy.deepcopy(lista_estafetas)
            lista_estafetas_BFS = copy.deepcopy(lista_estafetas)
            lista_estafetas_aStar = copy.deepcopy(lista_estafetas)
            lista_estafetas_greedy = copy.deepcopy(lista_estafetas)
            print("-------------------------------DISTRIBUIÇÃO DFS-------------------------------\n")
            for estafeta in lista_estafetas_DFS:
                enderecos_encomendas = []
                for encomenda in estafeta.encomendas:
                    enderecos_encomendas.append(encomenda.rua_destino)
                print(f"ENTREGAS A SEREM FEITAS EM: {enderecos_encomendas}")
                path = []
                c = 0
                path_total = []
                print(g.entregar_entregas_DFS3("Rua da Fonte Longa, Mogege",estafeta,path,c,path_total))
            print("-------------------------------DISTRIBUIÇÃO BFS-------------------------------\n")
            for estafeta in lista_estafetas_BFS:
                enderecos_encomendas = []
                for encomenda in estafeta.encomendas:
                    enderecos_encomendas.append(encomenda.rua_destino)
                print(f"ENTREGAS A SEREM FEITAS EM: {enderecos_encomendas}")
                path = []
                c = 0
                path_total = []
                print(g.entregar_entregas_BFS3("Rua da Fonte Longa, Mogege",estafeta,path,c,path_total))
            print("-------------------------------DISTRIBUIÇÃO A*-------------------------------\n")
            for estafeta in lista_estafetas_aStar:
                enderecos_encomendas = []
                for encomenda in estafeta.encomendas:
                    enderecos_encomendas.append(encomenda.rua_destino)
                print(f"ENTREGAS A SEREM FEITAS EM: {enderecos_encomendas}")
                path = []
                c = 0
                path_total = []
                print(g.entregar_entregas_aStar3("Rua da Fonte Longa, Mogege",estafeta,path,c,path_total))
            print("-------------------------------DISTRIBUIÇÃO GULOSA-------------------------------\n")
            for estafeta in lista_estafetas_greedy:
                enderecos_encomendas = []
                for encomenda in estafeta.encomendas:
                    enderecos_encomendas.append(encomenda.rua_destino)
                print(f"ENTREGAS A SEREM FEITAS EM: {enderecos_encomendas}")
                path = []
                c = 0
                path_total = []
                print(g.entregar_entregas_greedy3("Rua da Fonte Longa, Mogege",estafeta,path,c,path_total))
            l = input("prima enter para continuar")

        else:
            print("Não adicionou nada!")
            l = input("Prima enter para continuar!")

if __name__ == "__main__" :
    main()