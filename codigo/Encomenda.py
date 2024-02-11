class Encomenda:
    def __init__(self, rua_destino, peso, volume, preco, prazo_entrega):
        self.rua_destino = rua_destino
        self.peso = peso
        self.volume = volume
        self.preco = preco
        self.prazo_entrega = prazo_entrega

    def __lt__(self, other):
        return self.peso < other.peso

    def __str__(self):
        return f"Encomenda: Destino - {self.rua_destino}, Peso - {self.peso} , Volume - {self.volume}, Preco - {self.preco}, Prazo de Entrega - {self.prazo_entrega}"