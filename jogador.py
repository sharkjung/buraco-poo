class Jogador:
    def __init__(self, nome, id_equipe):
        self.nome = nome
        self.id_equipe = id_equipe
        self.mao = []
        self.has_taken_dead = False
        self.vulnerable = False

    def comprar(self, deck):
        self.mao.append(deck.comprar_carta())

    def discarte(self, carta, deck):
        self.mao.remove(carta)
        deck.lixo.append(carta)
