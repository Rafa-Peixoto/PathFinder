from Encomenda import Encomenda

class Estafeta:
    def __init__(self, id, transporte, avaliacao_total, nr_avaliacoes, encomendas):
        self.id = id
        self.transporte = transporte
        self.transporte_peso_atual = 0.0
        self.transporte_velocidade = 0.0
        self.avaliacao_total = avaliacao_total
        self.nr_avaliacoes = nr_avaliacoes
        self.encomendas = []

    def __lt__(self, other):
        return self.id < other.id