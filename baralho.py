import random
from cartas import Carta

class Deck:
    def __init__(self):
        self.cartas = self.criar_deck()
        random.shuffle(self.cartas)
        self.lixo = []
        self.mortos = [[], []]

    def criar_deck(self):
        suits = ['S', 'H', 'D', 'C']
        ranks = [str(n) for n in range(2, 11)] + list('JQKA')
        return [Carta(rank, suit) for _ in range(2) for suit in suits for rank in ranks]

    def distribuir_cartas(self, jogadores):
        for _ in range(11):
            for jogador in jogadores:
                jogador.mao.append(self.cartas.pop())
        for i in range(2):
            for _ in range(11):
                self.mortos[i].append(self.cartas.pop())

    def comprar_carta(self):
        if not self.cartas:
            self.cartas = self.lixo[::-1]
            self.lixo = []
            random.shuffle(self.cartas)
        return self.cartas.pop() if self.cartas else None
